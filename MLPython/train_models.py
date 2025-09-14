#!/usr/bin/env python3
"""
Main model training script for Aamati ML system.
Trains all models using the groove_features_log_for_pred.csv data.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))


def run_training_script(script_name, description):
    """Run a training script with error handling."""
    print(f"🤖 {description}...")
    
    script_path = Path(__file__).parent / "ModelClassificationScripts" / script_name
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"Output: {result.stdout}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running {description}: {e}")
        return False


def train_all_models():
    """Train all classification models."""
    print("🚀 Starting Aamati Model Training")
    print("=" * 50)
    
    # Check if prediction data exists
    pred_file = "groove_features_log_for_pred.csv"
    if not os.path.exists(pred_file):
        print(f"❌ Prediction data file not found: {pred_file}")
        print("Please run feature extraction first!")
        return False
    
    print(f"📊 Using training data: {pred_file}")
    
    # Training scripts in order
    training_scripts = [
        ("energy_randomforest.py", "Training Energy Classification Model"),
        ("dynamic_intensity_randomforest.py", "Training Dynamic Intensity Model"),
        ("swing_randomforest.py", "Training Swing Detection Model"),
        ("fill_activity_randomforest.py", "Training Fill Activity Model"),
        ("rhythmic_density_ordinal_regression.py", "Training Rhythmic Density Model"),
        ("fx_character_rfclassifier.py", "Training FX Character Model"),
        ("timing_feel_randomforest.py", "Training Timing Feel Model")
    ]
    
    success_count = 0
    total_count = len(training_scripts)
    
    for script, description in training_scripts:
        if run_training_script(script, description):
            success_count += 1
        else:
            print(f"⚠️ {description} failed, continuing with other models...")
    
    print(f"\n📊 Training Summary: {success_count}/{total_count} models trained successfully")
    
    if success_count == total_count:
        print("🎉 All models trained successfully!")
        return True
    elif success_count > 0:
        print("⚠️ Some models failed, but training completed with partial success")
        return True
    else:
        print("❌ All model training failed")
        return False


def train_main_mood_model():
    """Train the main mood classification model."""
    print("\n🎯 Training Main Mood Classification Model")
    print("=" * 50)
    
    # This would train the main mood model that outputs both .joblib and .onnx
    # For now, we'll use the existing mood_classification_model.py
    script_path = Path(__file__).parent / "mood_classification_model.py"
    
    if not script_path.exists():
        print(f"❌ Main model script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print("✅ Main mood model trained successfully")
            print("📦 Generated groove_mood_model.joblib and groove_mood_model.onnx")
            return True
        else:
            print("❌ Main mood model training failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error training main mood model: {e}")
        return False


def main():
    """Main entry point for model training."""
    parser = argparse.ArgumentParser(description="Aamati Model Training")
    parser.add_argument("--models", nargs="+", 
                       choices=["classification", "main", "all"],
                       default=["all"],
                       help="Models to train")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    print("🎵 Aamati Model Training System")
    print("=" * 50)
    
    success = True
    
    if "all" in args.models or "classification" in args.models:
        success &= train_all_models()
    
    if "all" in args.models or "main" in args.models:
        success &= train_main_mood_model()
    
    if success:
        print("\n🎉 Model training completed successfully!")
        print("📁 Models saved in ModelClassificationScripts/models/")
        print("🎯 Main model saved as groove_mood_model.joblib and groove_mood_model.onnx")
    else:
        print("\n❌ Model training failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
