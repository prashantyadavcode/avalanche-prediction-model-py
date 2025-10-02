#!/usr/bin/env python3
"""
Test script to verify the ML models are working correctly
"""

import pickle
import pandas as pd
import numpy as np
from datetime import datetime

def test_models():
    """Test the loaded models"""
    
    print("🧪 Testing ML models...")
    
    try:
        # Load models
        slab_model = pickle.load(open('web-app/models/slab_model.pkl', 'rb'))
        wet_model = pickle.load(open('web-app/models/wet_model.pkl', 'rb'))
        
        print("✅ Models loaded successfully!")
        print(f"📊 Slab model type: {type(slab_model)}")
        print(f"📊 Wet model type: {type(wet_model)}")
        
        # Generate test features
        now = datetime.now()
        doy = now.timetuple().tm_yday
        
        test_features = {
            'DOY': doy,
            'MONTH': now.month,
            'SNOW_H': 100.0,
            'GRTR_40': 1.0,
            'SNOW_LAST_24': 5.0,
            'W_4DAY_SNOW': 15.0,
            'SNOW_DENSITY': 0.2,
            'REL_DENSITY': 1.0,
            'T_MAX_SUM': 5.0,
            'SETTLE': 2.0,
            'SWE': 10.0,
            'T_MIN_DELTA': 0.0,
            'T_MIN_24': -5.0,
            'T_MAX_24': 10.0,
            'WSP_MAX': 20.0,
            'WSP_SUSTAINED': 15.0,
            'AVY_24_N': 0,
            'AVY_24_DSUM': 0.0,
            'P_SLAB': 0.5,
            'P_WET': 0.3
        }
        
        # Create DataFrame
        feature_df = pd.DataFrame([test_features])
        
        # Make predictions
        slab_prob = slab_model.predict_proba(feature_df)[0][1]
        wet_prob = wet_model.predict_proba(feature_df)[0][1]
        
        print(f"🎯 Test prediction results:")
        print(f"   Slab probability: {slab_prob:.3f}")
        print(f"   Wet probability: {wet_prob:.3f}")
        print(f"   Combined risk: {max(slab_prob, wet_prob):.3f}")
        
        # Test risk level conversion
        combined_prob = max(slab_prob, wet_prob)
        if combined_prob < 0.3:
            risk_level = "low"
        elif combined_prob < 0.5:
            risk_level = "moderate"
        elif combined_prob < 0.7:
            risk_level = "considerable"
        elif combined_prob < 0.9:
            risk_level = "high"
        else:
            risk_level = "extreme"
            
        print(f"   Risk level: {risk_level}")
        
        print("✅ Model test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing models: {e}")
        return False

if __name__ == "__main__":
    test_models()
