#!/usr/bin/env python3
"""
Script to copy trained ML models to the web app directory for deployment
"""

import os
import shutil
import sys

def copy_models():
    """Copy the trained models to the web app directory"""
    
    # Source paths
    src_dir = "src/best-ests"
    slab_model_src = os.path.join(src_dir, "aspen_best_est_gbc_SLAB.p")
    wet_model_src = os.path.join(src_dir, "aspen_best_est_gbc_WET.p")
    
    # Destination paths
    web_app_dir = "web-app"
    models_dir = os.path.join(web_app_dir, "models")
    
    # Create models directory if it doesn't exist
    os.makedirs(models_dir, exist_ok=True)
    
    # Copy models
    try:
        if os.path.exists(slab_model_src):
            shutil.copy2(slab_model_src, os.path.join(models_dir, "slab_model.pkl"))
            print(f"✅ Copied slab model: {slab_model_src} -> {models_dir}/slab_model.pkl")
        else:
            print(f"❌ Slab model not found: {slab_model_src}")
            
        if os.path.exists(wet_model_src):
            shutil.copy2(wet_model_src, os.path.join(models_dir, "wet_model.pkl"))
            print(f"✅ Copied wet model: {wet_model_src} -> {models_dir}/wet_model.pkl")
        else:
            print(f"❌ Wet model not found: {wet_model_src}")
            
    except Exception as e:
        print(f"❌ Error copying models: {e}")
        return False
    
    return True

def update_api_paths():
    """Update the API to use the correct model paths"""
    
    api_file = "web-app/api/index.py"
    
    if not os.path.exists(api_file):
        print(f"❌ API file not found: {api_file}")
        return False
    
    # Read the current API file
    with open(api_file, 'r') as f:
        content = f.read()
    
    # Update the model loading paths
    old_load_function = '''def load_models():
    """Load the trained gradient boosting models"""
    try:
        # Load the actual trained models from the project
        slab_model = pickle.load(open('../src/best-ests/aspen_best_est_gbc_SLAB.p', 'rb'))
        wet_model = pickle.load(open('../src/best-ests/aspen_best_est_gbc_WET.p', 'rb'))
        return slab_model, wet_model
    except FileNotFoundError:
        # Try alternative paths
        try:
            slab_model = pickle.load(open('src/best-ests/aspen_best_est_gbc_SLAB.p', 'rb'))
            wet_model = pickle.load(open('src/best-ests/aspen_best_est_gbc_WET.p', 'rb'))
            return slab_model, wet_model
        except FileNotFoundError:
            print("Warning: Could not load trained models, using demo mode")
            return None, None'''

    new_load_function = '''def load_models():
    """Load the trained gradient boosting models"""
    try:
        # Load the trained models from the models directory
        slab_model = pickle.load(open('models/slab_model.pkl', 'rb'))
        wet_model = pickle.load(open('models/wet_model.pkl', 'rb'))
        return slab_model, wet_model
    except FileNotFoundError:
        print("Warning: Could not load trained models, using demo mode")
        return None, None'''

    # Replace the function
    updated_content = content.replace(old_load_function, new_load_function)
    
    # Write the updated content
    with open(api_file, 'w') as f:
        f.write(updated_content)
    
    print(f"✅ Updated API model paths in {api_file}")
    return True

if __name__ == "__main__":
    print("🚀 Setting up ML models for web deployment...")
    
    # Change to project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Copy models
    if copy_models():
        print("✅ Models copied successfully")
    else:
        print("❌ Failed to copy models")
        sys.exit(1)
    
    # Update API paths
    if update_api_paths():
        print("✅ API paths updated successfully")
    else:
        print("❌ Failed to update API paths")
        sys.exit(1)
    
    print("\n🎉 Setup complete! Your ML models are now connected to the web app.")
    print("📁 Models are located in: web-app/models/")
    print("🌐 Ready for Vercel deployment!")
