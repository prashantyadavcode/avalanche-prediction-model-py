#!/usr/bin/env python3
"""
Avalanche Risk Prediction - Data Transformation Utilities

This module provides utility functions for data transformation, preprocessing,
and feature engineering in the avalanche risk prediction system.

Author: Prashant Yadav
Date: 2024
License: MIT
"""

import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

class AvalancheDataTransformer:
    """
    Data transformation utilities for avalanche risk prediction.
    
    This class provides methods for:
    - Water year calculations
    - Data oversampling techniques
    - SMOTE implementation
    - Data preprocessing utilities
    """
    
    def __init__(self):
        """Initialize the data transformer."""
        self.scaler = StandardScaler()
        
    def calculate_water_year_month(self, month):
        """
        Convert calendar month to water year month.
        
        Water year runs from October 1 to September 30.
        
        Args:
            month (int): Calendar month (1-12)
            
        Returns:
            int: Water year month (1-12)
        """
        if month >= 10:
            return month - 9
        else:
            return month + 3
    
    def calculate_water_year_day(self, day_of_year):
        """
        Convert calendar day of year to water year day.
        
        Args:
            day_of_year (int): Calendar day of year (1-365/366)
            
        Returns:
            int: Water year day (1-365/366)
        """
        if day_of_year >= 273:  # October 1st
            return day_of_year - 273
        else:
            return day_of_year + 92
    
    def set_datetime_index(self, df, date_column):
        """
        Set pandas DataFrame index from datetime column.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            date_column (str): Name of date column
            
        Returns:
            pd.DataFrame: DataFrame with datetime index
        """
        df_copy = df.copy()
        
        # Convert to datetime
        df_copy['dt'] = pd.to_datetime(df_copy[date_column])
        
        # Set index
        df_copy.set_index('dt', inplace=True)
        
        # Drop original columns
        df_copy.drop([date_column], axis=1, inplace=True)
        
        return df_copy
    
    def oversample_data(self, data_df, target_column, n_classes=4):
        """
        Oversample data to balance class distribution.
        
        Args:
            data_df (pd.DataFrame): Input DataFrame
            target_column (str): Name of target column
            n_classes (int): Number of classes to balance
            
        Returns:
            tuple: (oversampled_df, class_counts, oversampling_factors)
        """
        # Split data by class
        class_dfs = []
        for i in range(n_classes + 1):
            class_dfs.append(data_df[data_df[target_column] == i])
        
        # Calculate class counts
        class_counts = {}
        for i in range(n_classes + 1):
            class_counts[i] = data_df[data_df[target_column] == i].shape[0]
        
        # Calculate oversampling factors
        max_count = max(class_counts.values())
        oversampling_factors = {}
        for i in range(n_classes + 1):
            if class_counts[i] > 0:
                oversampling_factors[i] = max_count // class_counts[i]
            else:
                oversampling_factors[i] = 0
        
        # Create oversampled dataset
        oversampled_frames = [data_df]
        
        for i in range(n_classes + 1):
            if oversampling_factors[i] > 1:
                for _ in range(oversampling_factors[i] - 1):
                    oversampled_frames.append(class_dfs[i])
        
        # Concatenate all frames
        oversampled_df = pd.concat(oversampled_frames, axis=0)
        
        # Shuffle the data
        oversampled_df = oversampled_df.sample(frac=1).reset_index(drop=True)
        
        return oversampled_df, class_counts, oversampling_factors
    
    def separate_classes(self, X, y):
        """
        Separate data into positive and negative classes.
        
        Args:
            X (np.ndarray): Feature matrix
            y (np.ndarray): Target vector
            
        Returns:
            tuple: (negative_count, positive_count, X_pos, X_neg, y_pos, y_neg)
        """
        negative_mask = y == 0
        positive_mask = y == 1
        
        negative_count = np.sum(negative_mask)
        positive_count = np.sum(positive_mask)
        
        X_negatives = X[negative_mask]
        X_positives = X[positive_mask]
        y_negatives = y[negative_mask]
        y_positives = y[positive_mask]
        
        return negative_count, positive_count, X_positives, X_negatives, y_positives, y_negatives
    
    def apply_smote(self, X, y, target_proportion=0.5, k_neighbors=None):
        """
        Apply SMOTE (Synthetic Minority Oversampling Technique).
        
        Args:
            X (np.ndarray): Feature matrix
            y (np.ndarray): Target vector
            target_proportion (float): Target proportion of positive class
            k_neighbors (int): Number of neighbors for SMOTE
            
        Returns:
            tuple: (X_smoted, y_smoted)
        """
        # Check if oversampling is needed
        if target_proportion < np.mean(y):
            return X, y
        
        # Set default k
        if k_neighbors is None:
            k_neighbors = int(len(X) ** 0.5)
        
        # Separate classes
        neg_count, pos_count, X_pos, X_neg, y_pos, y_neg = self.separate_classes(X, y)
        
        # Fit KNN on positive class
        knn = KNeighborsClassifier(n_neighbors=k_neighbors)
        knn.fit(X_pos, y_pos)
        
        # Find neighbors
        neighbors = knn.kneighbors(return_distance=False)
        
        # Calculate number of synthetic samples needed
        target_positive_count = int((target_proportion * neg_count) / (1 - target_proportion))
        synthetic_samples_needed = target_positive_count - pos_count
        
        if synthetic_samples_needed <= 0:
            return X, y
        
        # Generate synthetic samples
        synthetic_samples = []
        
        for _ in range(synthetic_samples_needed):
            # Random positive sample
            random_idx = np.random.randint(0, pos_count)
            random_sample = X_pos[random_idx]
            
            # Random neighbor
            random_neighbor_idx = np.random.randint(0, k_neighbors)
            random_neighbor = X_pos[neighbors[random_idx][random_neighbor_idx]]
            
            # Random interpolation factor
            interpolation_factor = np.random.random()
            
            # Create synthetic sample
            synthetic_sample = random_sample + interpolation_factor * (random_neighbor - random_sample)
            synthetic_samples.append(synthetic_sample)
        
        # Combine original and synthetic data
        X_smoted = np.vstack([X, np.array(synthetic_samples)])
        y_smoted = np.concatenate([y, np.ones(synthetic_samples_needed)])
        
        return X_smoted, y_smoted
    
    def scale_features(self, X, fit_scaler=True):
        """
        Scale features using StandardScaler.
        
        Args:
            X (np.ndarray): Feature matrix
            fit_scaler (bool): Whether to fit the scaler
            
        Returns:
            np.ndarray: Scaled feature matrix
        """
        if fit_scaler:
            return self.scaler.fit_transform(X)
        else:
            return self.scaler.transform(X)
    
    def create_lag_features(self, df, columns, lags=[1, 2, 3, 7]):
        """
        Create lag features for time series data.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (list): Columns to create lags for
            lags (list): List of lag periods
            
        Returns:
            pd.DataFrame: DataFrame with lag features
        """
        df_lagged = df.copy()
        
        for col in columns:
            if col in df_lagged.columns:
                for lag in lags:
                    df_lagged[f'{col}_lag_{lag}'] = df_lagged[col].shift(lag)
        
        return df_lagged
    
    def create_rolling_features(self, df, columns, windows=[3, 7, 14]):
        """
        Create rolling window features.
        
        Args:
            df (pd.DataFrame): Input DataFrame
            columns (list): Columns to create rolling features for
            windows (list): List of window sizes
            
        Returns:
            pd.DataFrame: DataFrame with rolling features
        """
        df_rolling = df.copy()
        
        for col in columns:
            if col in df_rolling.columns:
                for window in windows:
                    df_rolling[f'{col}_rolling_mean_{window}'] = df_rolling[col].rolling(window=window).mean()
                    df_rolling[f'{col}_rolling_std_{window}'] = df_rolling[col].rolling(window=window).std()
                    df_rolling[f'{col}_rolling_max_{window}'] = df_rolling[col].rolling(window=window).max()
                    df_rolling[f'{col}_rolling_min_{window}'] = df_rolling[col].rolling(window=window).min()
        
        return df_rolling

def main():
    """Main function to demonstrate data transformation utilities."""
    
    # Initialize transformer
    transformer = AvalancheDataTransformer()
    
    # Example usage
    print("🏔️ Avalanche Data Transformation Utilities")
    print("=" * 50)
    
    # Water year calculations
    print("📅 Water Year Calculations:")
    for month in [1, 6, 10, 12]:
        wy_month = transformer.calculate_water_year_month(month)
        print(f"   Calendar month {month} -> Water year month {wy_month}")
    
    # SMOTE example
    print("\n🔄 SMOTE Example:")
    X = np.random.randn(100, 5)
    y = np.random.choice([0, 1], size=100, p=[0.8, 0.2])
    
    print(f"   Original data shape: {X.shape}")
    print(f"   Original class distribution: {np.bincount(y)}")
    
    X_smoted, y_smoted = transformer.apply_smote(X, y, target_proportion=0.5)
    
    print(f"   SMOTED data shape: {X_smoted.shape}")
    print(f"   SMOTED class distribution: {np.bincount(y_smoted.astype(int))}")
    
    print("\n✅ Data transformation utilities ready!")

if __name__ == "__main__":
    main()