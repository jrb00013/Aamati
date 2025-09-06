#!/usr/bin/env python3
"""
Setup script to copy ML models to the JUCE plugin Resources folder
"""

import os
import shutil
import sys
from pathlib import Path

def setup_ml_models():
    """Copy ML models to the JUCE plugin Resources folder"""
    
    # Get the script directory
    script_dir = Path(__file__).parent
    ml_dir = script_dir / "MLPython"
    resources_dir = script_dir / "Resources"
    
    # Create Resources directory if it doesn't exist
    resources_dir.mkdir(exist_ok=True)
    
    # List of model files to copy
    model_files = [
        "groove_mood_model.onnx",
        "groove_mood_model.pkl"
    ]
    
    # Copy model files
    for model_file in model_files:
        src = ml_dir / model_file
        dst = resources_dir / model_file
        
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✅ Copied {model_file} to Resources folder")
        else:
            print(f"⚠️  Warning: {model_file} not found in MLPython folder")
    
    # Copy additional model files from ModelClassificationScripts/models
    models_dir = ml_dir / "ModelClassificationScripts" / "models"
    if models_dir.exists():
        for model_file in models_dir.glob("*.joblib"):
            dst = resources_dir / model_file.name
            shutil.copy2(model_file, dst)
            print(f"✅ Copied {model_file.name} to Resources folder")
    
    print("\n🎵 ML models setup complete!")
    print("The plugin will look for models in the Resources folder.")
    print("Make sure to build the plugin with the Resources folder included.")

if __name__ == "__main__":
    setup_ml_models()
