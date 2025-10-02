#!/usr/bin/env python3
"""
Avalanche Risk Prediction - Feature Engineering Module

This module implements comprehensive feature engineering for avalanche risk prediction,
including data preprocessing, feature creation, and feature selection.

Author: Prashant Yadav
Date: 2024
License: MIT
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings('ignore')

class AvalancheFeatureEngineer:
    """
    Advanced feature engineering for avalanche risk prediction.
    
    This class implements comprehensive feature engineering including:
    - Data preprocessing and cleaning
    - Temporal feature creation
    - Weather feature engineering
    - Snowpack feature calculation
    - Historical pattern analysis
    """
    
    def __init__(self):
        """Initialize the feature engineer."""
        self.scalers = {}
        self.encoders = {}
        self.feature_names = []
        self.feature_importance = {}
        
    def load_raw_data(self, data_path):
        """
        Load raw data from multiple sources.
        
        Args:
            data_path (str): Path to data directory
            
        Returns:
            dict: Dictionary of loaded datasets
        """
        datasets = {}
        
        try:
            # Load avalanche data
            avalanche_file = os.path.join(data_path, 'avalanche_observations.csv')
            if os.path.exists(avalanche_file):
                datasets['avalanche'] = pd.read_csv(avalanche_file)
                print(f"✅ Loaded avalanche data: {datasets['avalanche'].shape}")
            
            # Load weather data
            weather_file = os.path.join(data_path, 'weather_data.csv')
            if os.path.exists(weather_file):
                datasets['weather'] = pd.read_csv(weather_file)
                print(f"✅ Loaded weather data: {datasets['weather'].shape}")
            
            # Load snowpack data
            snowpack_file = os.path.join(data_path, 'snowpack_data.csv')
            if os.path.exists(snowpack_file):
                datasets['snowpack'] = pd.read_csv(snowpack_file)
                print(f"✅ Loaded snowpack data: {datasets['snowpack'].shape}")
            
            return datasets
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return {}
    
    def clean_data(self, df, data_type='general'):
        """
        Clean and preprocess data.
        
        Args:
            df (pd.DataFrame): Input dataframe
            data_type (str): Type of data for specific cleaning
            
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        df_clean = df.copy()
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        # Handle missing values
        if data_type == 'avalanche':
            # Avalanche-specific cleaning
            df_clean['size'] = df_clean['size'].fillna('Unknown')
            df_clean['type'] = df_clean['type'].fillna('Unknown')
            
        elif data_type == 'weather':
            # Weather-specific cleaning
            numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
            df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
            
        elif data_type == 'snowpack':
            # Snowpack-specific cleaning
            df_clean['snow_depth'] = df_clean['snow_depth'].fillna(0)
            df_clean['snow_water_equivalent'] = df_clean['snow_water_equivalent'].fillna(0)
        
        # Remove outliers using IQR method
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
        
        print(f"✅ Cleaned {data_type} data: {df_clean.shape}")
        return df_clean
    
    def create_temporal_features(self, df):
        """
        Create temporal features from date columns.
        
        Args:
            df (pd.DataFrame): Input dataframe with date column
            
        Returns:
            pd.DataFrame: Dataframe with temporal features
        """
        df_temp = df.copy()
        
        # Ensure date column is datetime
        if 'date' in df_temp.columns:
            df_temp['date'] = pd.to_datetime(df_temp['date'])
            
            # Basic temporal features
            df_temp['year'] = df_temp['date'].dt.year
            df_temp['month'] = df_temp['date'].dt.month
            df_temp['day'] = df_temp['date'].dt.day
            df_temp['day_of_year'] = df_temp['date'].dt.dayofyear
            df_temp['week_of_year'] = df_temp['date'].dt.isocalendar().week
            df_temp['quarter'] = df_temp['date'].dt.quarter
            
            # Water year (October 1 to September 30)
            df_temp['water_year'] = df_temp['date'].dt.year
            df_temp.loc[df_temp['month'] >= 10, 'water_year'] += 1
            df_temp['day_of_water_year'] = df_temp['date'].dt.dayofyear
            df_temp.loc[df_temp['month'] >= 10, 'day_of_water_year'] -= 273
            
            # Seasonal indicators
            df_temp['is_winter'] = df_temp['month'].isin([12, 1, 2])
            df_temp['is_spring'] = df_temp['month'].isin([3, 4, 5])
            df_temp['is_summer'] = df_temp['month'].isin([6, 7, 8])
            df_temp['is_fall'] = df_temp['month'].isin([9, 10, 11])
            
            # Weekend indicator
            df_temp['is_weekend'] = df_temp['date'].dt.weekday >= 5
            
            # Holiday indicators (simplified)
            df_temp['is_holiday'] = (
                (df_temp['month'] == 12) & (df_temp['day'] == 25) |  # Christmas
                (df_temp['month'] == 1) & (df_temp['day'] == 1) |    # New Year
                (df_temp['month'] == 7) & (df_temp['day'] == 4)      # July 4th
            )
        
        print(f"✅ Created temporal features: {df_temp.shape}")
        return df_temp
    
    def engineer_features(self, data_path, output_path='data/processed/'):
        """
        Run the complete feature engineering pipeline.
        
        Args:
            data_path (str): Path to raw data
            output_path (str): Path to save processed data
            
        Returns:
            pd.DataFrame: Engineered feature matrix
        """
        print("🏔️ Starting Feature Engineering Pipeline")
        print("=" * 50)
        
        # Load raw data
        datasets = self.load_raw_data(data_path)
        if not datasets:
            print("❌ No data loaded")
            return None
        
        # Clean data
        cleaned_datasets = {}
        for name, df in datasets.items():
            cleaned_datasets[name] = self.clean_data(df, name)
        
        # Create temporal features
        for name, df in cleaned_datasets.items():
            cleaned_datasets[name] = self.create_temporal_features(df)
        
        # Combine all datasets
        combined_df = None
        for name, df in cleaned_datasets.items():
            if combined_df is None:
                combined_df = df
            else:
                # Merge on date if available
                if 'date' in df.columns and 'date' in combined_df.columns:
                    combined_df = pd.merge(combined_df, df, on='date', how='outer')
                else:
                    combined_df = pd.concat([combined_df, df], axis=1)
        
        # Save processed data
        os.makedirs(output_path, exist_ok=True)
        output_file = os.path.join(output_path, 'engineered_features.csv')
        combined_df.to_csv(output_file, index=False)
        
        print(f"✅ Feature engineering complete: {combined_df.shape}")
        print(f"💾 Saved to: {output_file}")
        
        return combined_df

def main():
    """Main function to run feature engineering."""
    
    # Initialize feature engineer
    engineer = AvalancheFeatureEngineer()
    
    # Run feature engineering pipeline
    features = engineer.engineer_features('data/raw/', 'data/processed/')
    
    if features is not None:
        print("\n🏔️ Feature Engineering Complete!")
        print(f"📊 Final dataset shape: {features.shape}")
        print("📁 Check 'data/processed/' for the engineered features")

if __name__ == "__main__":
    main()
