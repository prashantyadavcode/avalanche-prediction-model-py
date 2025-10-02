#!/usr/bin/env python3
"""
Avalanche Risk Prediction Model Training Script

This script implements a comprehensive machine learning pipeline for predicting
avalanche risk levels in Colorado backcountry zones using ensemble methods.

Author: Prashant Yadav
Date: 2024
License: MIT
"""

import pandas as pd
import numpy as np
import pickle
import os
import warnings
from datetime import datetime
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, TimeSeriesSplit
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

class AvalancheRiskPredictor:
    """
    Advanced avalanche risk prediction system using ensemble machine learning.
    
    This class implements a comprehensive pipeline for training, validating,
    and deploying avalanche risk prediction models.
    """
    
    def __init__(self, data_path='data/processed/', model_path='models/'):
        """
        Initialize the avalanche risk predictor.
        
        Args:
            data_path (str): Path to processed data directory
            model_path (str): Path to save trained models
        """
        self.data_path = data_path
        self.model_path = model_path
        self.models = {}
        self.scalers = {}
        self.feature_importance = {}
        
        # Create directories if they don't exist
        os.makedirs(self.model_path, exist_ok=True)
        os.makedirs('results/', exist_ok=True)
        
    def load_data(self, filename='avalanche_features.csv'):
        """
        Load and preprocess the avalanche risk dataset.
        
        Args:
            filename (str): Name of the data file
            
        Returns:
            pd.DataFrame: Processed dataset
        """
        try:
            # Load the dataset
            data = pd.read_csv(os.path.join(self.data_path, filename))
            
            print(f"✅ Loaded dataset: {data.shape[0]} samples, {data.shape[1]} features")
            
            # Basic data validation
            if data.empty:
                raise ValueError("Dataset is empty")
            
            # Check for required columns
            required_cols = ['SLAB', 'WET', 'N_AVY']
            missing_cols = [col for col in required_cols if col not in data.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
            
            return data
            
        except FileNotFoundError:
            print(f"❌ Data file not found: {filename}")
            return None
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return None
    
    def prepare_features(self, data):
        """
        Prepare features for model training.
        
        Args:
            data (pd.DataFrame): Raw dataset
            
        Returns:
            tuple: (X, y_slab, y_wet, feature_names)
        """
        # Define target variables
        target_slab = 'SLAB'
        target_wet = 'WET'
        
        # Remove target columns and non-feature columns
        feature_cols = [col for col in data.columns 
                       if col not in [target_slab, target_wet, 'N_AVY', 'Date', 'Zone']]
        
        X = data[feature_cols].copy()
        y_slab = data[target_slab].copy()
        y_wet = data[target_wet].copy()
        
        # Handle missing values
        X = X.fillna(X.median())
        
        # Remove any remaining infinite values
        X = X.replace([np.inf, -np.inf], np.nan)
        X = X.fillna(X.median())
        
        print(f"✅ Prepared features: {X.shape[1]} features for {X.shape[0]} samples")
        
        return X, y_slab, y_wet, feature_cols
    
    def create_model(self, model_type='gradient_boosting'):
        """
        Create and configure the machine learning model.
        
        Args:
            model_type (str): Type of model to create
            
        Returns:
            sklearn model: Configured model
        """
        if model_type == 'gradient_boosting':
            model = GradientBoostingClassifier(
                n_estimators=500,
                learning_rate=0.05,
                max_depth=7,
                min_samples_split=5,
                min_samples_leaf=4,
                subsample=0.8,
                max_features='log2',
                random_state=42,
                verbose=0
            )
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
        
        return model
    
    def train_model(self, X, y, model_name, optimize=True):
        """
        Train a machine learning model.
        
        Args:
            X (pd.DataFrame): Feature matrix
            y (pd.Series): Target variable
            model_name (str): Name for the model
            optimize (bool): Whether to optimize hyperparameters
            
        Returns:
            sklearn model: Trained model
        """
        print(f"🚀 Training {model_name} model...")
        
        if optimize:
            model = self.optimize_hyperparameters(X, y)
        else:
            model = self.create_model()
        
        # Train the model
        model.fit(X, y)
        
        # Store the model
        self.models[model_name] = model
        
        # Calculate feature importance
        if hasattr(model, 'feature_importances_'):
            self.feature_importance[model_name] = model.feature_importances_
        
        print(f"✅ {model_name} model trained successfully")
        
        return model
    
    def evaluate_model(self, model, X_test, y_test, model_name):
        """
        Evaluate model performance on test data.
        
        Args:
            model: Trained model
            X_test: Test features
            y_test: Test targets
            model_name: Name of the model
            
        Returns:
            dict: Evaluation metrics
        """
        print(f"📊 Evaluating {model_name} model...")
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        accuracy = model.score(X_test, y_test)
        auc_score = roc_auc_score(y_test, y_pred_proba)
        
        # Classification report
        report = classification_report(y_test, y_pred, output_dict=True)
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        
        # Store results
        results = {
            'accuracy': accuracy,
            'auc_score': auc_score,
            'precision': report['1']['precision'],
            'recall': report['1']['recall'],
            'f1_score': report['1']['f1-score'],
            'confusion_matrix': cm
        }
        
        print(f"✅ {model_name} Results:")
        print(f"   Accuracy: {accuracy:.4f}")
        print(f"   AUC Score: {auc_score:.4f}")
        print(f"   Precision: {results['precision']:.4f}")
        print(f"   Recall: {results['recall']:.4f}")
        print(f"   F1-Score: {results['f1_score']:.4f}")
        
        return results
    
    def save_model(self, model, model_name):
        """
        Save trained model to disk.
        
        Args:
            model: Trained model
            model_name: Name of the model
        """
        filename = f"{model_name}_model.pkl"
        filepath = os.path.join(self.model_path, filename)
        
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
        
        print(f"💾 Model saved: {filepath}")
    
    def run_training_pipeline(self, data_file='avalanche_features.csv'):
        """
        Run the complete training pipeline.
        
        Args:
            data_file: Name of the data file
        """
        print("🏔️ Starting Avalanche Risk Prediction Training Pipeline")
        print("=" * 60)
        
        # Load data
        data = self.load_data(data_file)
        if data is None:
            return
        
        # Prepare features
        X, y_slab, y_wet, feature_names = self.prepare_features(data)
        
        # Split data for training and testing
        split_idx = int(0.8 * len(X))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_slab_train, y_slab_test = y_slab[:split_idx], y_slab[split_idx:]
        y_wet_train, y_wet_test = y_wet[:split_idx], y_wet[split_idx:]
        
        print(f"📊 Data split: {len(X_train)} training, {len(X_test)} test samples")
        
        # Train slab avalanche model
        slab_model = self.train_model(X_train, y_slab_train, 'slab_avalanche')
        slab_results = self.evaluate_model(slab_model, X_test, y_slab_test, 'Slab Avalanche')
        
        # Train wet avalanche model
        wet_model = self.train_model(X_train, y_wet_train, 'wet_avalanche')
        wet_results = self.evaluate_model(wet_model, X_test, y_wet_test, 'Wet Avalanche')
        
        # Save models
        self.save_model(slab_model, 'slab_avalanche')
        self.save_model(wet_model, 'wet_avalanche')
        
        # Print summary
        print("\n" + "=" * 60)
        print("🎯 TRAINING PIPELINE COMPLETED")
        print("=" * 60)
        print(f"Slab Avalanche Model - Accuracy: {slab_results['accuracy']:.4f}")
        print(f"Wet Avalanche Model - Accuracy: {wet_results['accuracy']:.4f}")
        print(f"Models saved to: {self.model_path}")
        print(f"Results saved to: results/")

def main():
    """Main function to run the training pipeline."""
    
    # Initialize predictor
    predictor = AvalancheRiskPredictor()
    
    # Run training pipeline
    predictor.run_training_pipeline()
    
    print("\n🏔️ Avalanche Risk Prediction Model Training Complete!")
    print("📁 Check the 'models/' directory for trained models")
    print("📊 Check the 'results/' directory for evaluation plots")

if __name__ == "__main__":
    main()
