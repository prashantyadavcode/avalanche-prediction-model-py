#!/usr/bin/env python3
"""
Avalanche Risk Prediction - Data Processing Module

This module handles data cleaning, preprocessing, and preparation for the
avalanche risk prediction system.

Author: Prashant Yadav
Date: 2024
License: MIT
"""

import pandas as pd
import numpy as np
import os
import warnings
from datetime import datetime
import sqlite3
from pathlib import Path

warnings.filterwarnings('ignore')

class AvalancheDataProcessor:
    """
    Data processing class for avalanche risk prediction.
    
    This class handles:
    - Data loading from multiple sources
    - Data cleaning and preprocessing
    - Data validation and quality control
    - Data export and storage
    """
    
    def __init__(self, data_dir='data/'):
        """
        Initialize the data processor.
        
        Args:
            data_dir (str): Directory containing data files
        """
        self.data_dir = Path(data_dir)
        self.processed_data = {}
        
    def load_avalanche_data(self, file_path):
        """
        Load avalanche observation data.
        
        Args:
            file_path (str): Path to avalanche data file
            
        Returns:
            pd.DataFrame: Loaded avalanche data
        """
        try:
            # Try different file formats
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.db') or file_path.endswith('.sqlite'):
                conn = sqlite3.connect(file_path)
                df = pd.read_sql_query("SELECT * FROM avalanches", conn)
                conn.close()
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            
            print(f"✅ Loaded avalanche data: {df.shape}")
            return df
            
        except Exception as e:
            print(f"❌ Error loading avalanche data: {e}")
            return None
    
    def load_weather_data(self, file_path):
        """
        Load weather station data.
        
        Args:
            file_path (str): Path to weather data file
            
        Returns:
            pd.DataFrame: Loaded weather data
        """
        try:
            if file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_path}")
            
            print(f"✅ Loaded weather data: {df.shape}")
            return df
            
        except Exception as e:
            print(f"❌ Error loading weather data: {e}")
            return None
    
    def clean_avalanche_data(self, df):
        """
        Clean and preprocess avalanche data.
        
        Args:
            df (pd.DataFrame): Raw avalanche data
            
        Returns:
            pd.DataFrame: Cleaned avalanche data
        """
        df_clean = df.copy()
        
        # Standardize column names
        column_mapping = {
            'Date': 'date',
            'Location': 'location',
            'Size': 'size',
            'Type': 'type',
            'Trigger': 'trigger',
            'Aspect': 'aspect',
            'Elevation': 'elevation'
        }
        
        df_clean = df_clean.rename(columns=column_mapping)
        
        # Convert date column
        if 'date' in df_clean.columns:
            df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
        
        # Clean size column
        if 'size' in df_clean.columns:
            df_clean['size'] = df_clean['size'].str.upper()
            df_clean['size'] = df_clean['size'].fillna('UNKNOWN')
        
        # Clean type column
        if 'type' in df_clean.columns:
            df_clean['type'] = df_clean['type'].str.upper()
            df_clean['type'] = df_clean['type'].fillna('UNKNOWN')
        
        # Clean trigger column
        if 'trigger' in df_clean.columns:
            df_clean['trigger'] = df_clean['trigger'].str.upper()
            df_clean['trigger'] = df_clean['trigger'].fillna('UNKNOWN')
        
        # Remove rows with missing critical data
        df_clean = df_clean.dropna(subset=['date', 'location'])
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        print(f"✅ Cleaned avalanche data: {df_clean.shape}")
        return df_clean
    
    def clean_weather_data(self, df):
        """
        Clean and preprocess weather data.
        
        Args:
            df (pd.DataFrame): Raw weather data
            
        Returns:
            pd.DataFrame: Cleaned weather data
        """
        df_clean = df.copy()
        
        # Standardize column names
        column_mapping = {
            'Date': 'date',
            'Station': 'station',
            'Snow_Depth': 'snow_depth',
            'New_Snow': 'new_snow',
            'Temperature': 'temperature',
            'Wind_Speed': 'wind_speed',
            'Precipitation': 'precipitation'
        }
        
        df_clean = df_clean.rename(columns=column_mapping)
        
        # Convert date column
        if 'date' in df_clean.columns:
            df_clean['date'] = pd.to_datetime(df_clean['date'], errors='coerce')
        
        # Handle numeric columns
        numeric_cols = ['snow_depth', 'new_snow', 'temperature', 'wind_speed', 'precipitation']
        for col in numeric_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Remove outliers
        for col in numeric_cols:
            if col in df_clean.columns:
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
        
        # Fill missing values
        for col in numeric_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna(df_clean[col].median())
        
        print(f"✅ Cleaned weather data: {df_clean.shape}")
        return df_clean
    
    def merge_datasets(self, avalanche_df, weather_df):
        """
        Merge avalanche and weather datasets.
        
        Args:
            avalanche_df (pd.DataFrame): Cleaned avalanche data
            weather_df (pd.DataFrame): Cleaned weather data
            
        Returns:
            pd.DataFrame: Merged dataset
        """
        # Merge on date
        merged_df = pd.merge(avalanche_df, weather_df, on='date', how='left')
        
        # Fill missing weather data
        weather_cols = ['snow_depth', 'new_snow', 'temperature', 'wind_speed', 'precipitation']
        for col in weather_cols:
            if col in merged_df.columns:
                merged_df[col] = merged_df[col].fillna(merged_df[col].median())
        
        print(f"✅ Merged datasets: {merged_df.shape}")
        return merged_df
    
    def create_target_variables(self, df):
        """
        Create target variables for machine learning.
        
        Args:
            df (pd.DataFrame): Input dataset
            
        Returns:
            pd.DataFrame: Dataset with target variables
        """
        df_targets = df.copy()
        
        # Create binary target for slab avalanches
        if 'type' in df_targets.columns:
            df_targets['SLAB'] = (df_targets['type'] == 'SLAB').astype(int)
        else:
            df_targets['SLAB'] = 0
        
        # Create binary target for wet avalanches
        if 'type' in df_targets.columns:
            df_targets['WET'] = (df_targets['type'] == 'WET').astype(int)
        else:
            df_targets['WET'] = 0
        
        # Create count target for total avalanches
        df_targets['N_AVY'] = 1  # Each row represents one avalanche
        
        print(f"✅ Created target variables: {df_targets.shape}")
        return df_targets
    
    def process_all_data(self):
        """
        Process all available data files.
        
        Returns:
            pd.DataFrame: Processed dataset
        """
        print("🏔️ Starting Data Processing Pipeline")
        print("=" * 50)
        
        # Find data files
        data_files = list(self.data_dir.glob('**/*'))
        csv_files = [f for f in data_files if f.suffix == '.csv']
        db_files = [f for f in data_files if f.suffix in ['.db', '.sqlite']]
        
        print(f"📁 Found {len(csv_files)} CSV files and {len(db_files)} database files")
        
        # Process avalanche data
        avalanche_df = None
        for file_path in csv_files:
            if 'avalanche' in file_path.name.lower() or 'avy' in file_path.name.lower():
                avalanche_df = self.load_avalanche_data(str(file_path))
                if avalanche_df is not None:
                    avalanche_df = self.clean_avalanche_data(avalanche_df)
                    break
        
        # Process weather data
        weather_df = None
        for file_path in csv_files:
            if 'weather' in file_path.name.lower() or 'snotel' in file_path.name.lower():
                weather_df = self.load_weather_data(str(file_path))
                if weather_df is not None:
                    weather_df = self.clean_weather_data(weather_df)
                    break
        
        # Merge datasets
        if avalanche_df is not None and weather_df is not None:
            merged_df = self.merge_datasets(avalanche_df, weather_df)
            final_df = self.create_target_variables(merged_df)
        elif avalanche_df is not None:
            final_df = self.create_target_variables(avalanche_df)
        else:
            print("❌ No suitable data files found")
            return None
        
        # Save processed data
        output_path = self.data_dir / 'processed'
        output_path.mkdir(exist_ok=True)
        
        output_file = output_path / 'avalanche_features.csv'
        final_df.to_csv(output_file, index=False)
        
        print(f"✅ Data processing complete: {final_df.shape}")
        print(f"💾 Saved to: {output_file}")
        
        return final_df
    
    def validate_data(self, df):
        """
        Validate processed data quality.
        
        Args:
            df (pd.DataFrame): Processed dataset
            
        Returns:
            dict: Validation results
        """
        validation_results = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'missing_values': df.isnull().sum().sum(),
            'duplicate_rows': df.duplicated().sum(),
            'data_types': df.dtypes.to_dict()
        }
        
        # Check for required columns
        required_cols = ['date', 'SLAB', 'WET', 'N_AVY']
        missing_required = [col for col in required_cols if col not in df.columns]
        validation_results['missing_required_columns'] = missing_required
        
        # Check data ranges
        if 'SLAB' in df.columns:
            validation_results['slab_avalanches'] = df['SLAB'].sum()
        if 'WET' in df.columns:
            validation_results['wet_avalanches'] = df['WET'].sum()
        
        print("📊 Data Validation Results:")
        for key, value in validation_results.items():
            print(f"   {key}: {value}")
        
        return validation_results

def main():
    """Main function to run data processing."""
    
    # Initialize data processor
    processor = AvalancheDataProcessor('data/')
    
    # Process all data
    processed_data = processor.process_all_data()
    
    if processed_data is not None:
        # Validate data
        validation_results = processor.validate_data(processed_data)
        
        print("\n🏔️ Data Processing Complete!")
        print(f"📊 Final dataset shape: {processed_data.shape}")
        print("📁 Check 'data/processed/' for the processed data")

if __name__ == "__main__":
    main()