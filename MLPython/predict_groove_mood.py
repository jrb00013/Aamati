#!/usr/bin/env python3
"""
Predict groove mood using trained models.
This script uses the .joblib models for prediction.
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from joblib import load

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))


def load_prediction_models():
    """Load models for prediction."""
    models = {}
    model_files = {
        'energy_model': 'ModelClassificationScripts/models/energy_random_forest.joblib',
        'dynamic_intensity_model': 'ModelClassificationScripts/models/dynamic_intensity_randomforest.joblib',
        'swing_model': 'ModelClassificationScripts/models/swing_random_forest.joblib',
        'fill_activity_model': 'ModelClassificationScripts/models/fill_activity_randomforest.joblib',
        'rhythm_model': 'ModelClassificationScripts/models/rhythmic_density_ordinal_regression.joblib',
        'fx_model': 'ModelClassificationScripts/models/fx_character_classifier.joblib',
        'timing_feel_model': 'ModelClassificationScripts/models/timing_feel_randomforest.joblib',
        'main_mood_model': 'groove_mood_model.joblib'
    }
    
    for name, path in model_files.items():
        if os.path.exists(path):
            try:
                models[name] = load(path)
                print(f"✅ Loaded {name}")
            except Exception as e:
                print(f"⚠️ Failed to load {name}: {e}")
                models[name] = None
        else:
            print(f"⚠️ Model file not found: {path}")
            models[name] = None
    
    return models


def predict_mood_from_features(features, models):
    """Predict mood from extracted features."""
    if not models['main_mood_model']:
        print("❌ Main mood model not loaded")
        return "unknown"
    
    try:
        # Prepare features for prediction
        # The main model expects specific features
        feature_vector = np.array([[
            features['tempo'],
            features['swing'], 
            features['density'],
            features['dynamic_range'],
            features['energy']
        ]])
        
        # Predict mood
        prediction = models['main_mood_model'].predict(feature_vector)[0]
        
        # Map prediction to mood name
        mood_labels = [
            "chill", "energetic", "suspenseful", "uplifting", "ominous",
            "romantic", "gritty", "dreamy", "frantic", "focused"
        ]
        
        if 0 <= prediction < len(mood_labels):
            return mood_labels[prediction]
        else:
            return "unknown"
            
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return "error"


def predict_from_csv(csv_file, models):
    """Predict moods for all entries in CSV file."""
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        return
    
    print(f"📊 Predicting moods from {csv_file}")
    
    # Read CSV
    df = pd.read_csv(csv_file)
    
    if df.empty:
        print("⚠️ CSV file is empty")
        return
    
    print(f"📈 Found {len(df)} entries to process")
    
    # Predict moods
    predictions = []
    for idx, row in df.iterrows():
        features = {
            'tempo': row.get('tempo', 120),
            'swing': row.get('swing', 0),
            'density': row.get('density', 0),
            'dynamic_range': row.get('dynamic_range', 0),
            'energy': row.get('energy', 0)
        }
        
        mood = predict_mood_from_features(features, models)
        predictions.append(mood)
        
        if idx % 10 == 0:
            print(f"  Processed {idx + 1}/{len(df)} entries...")
    
    # Add predictions to dataframe
    df['predicted_mood'] = predictions
    
    # Save results
    output_file = csv_file.replace('.csv', '_with_predictions.csv')
    df.to_csv(output_file, index=False)
    print(f"✅ Predictions saved to {output_file}")
    
    # Print summary
    mood_counts = df['predicted_mood'].value_counts()
    print("\n📊 Prediction Summary:")
    for mood, count in mood_counts.items():
        print(f"  {mood}: {count}")


def main():
    """Main entry point for prediction."""
    parser = argparse.ArgumentParser(description="Aamati Mood Prediction")
    parser.add_argument("--csv-file", default="data/csv/groove_features_log_for_pred.csv",
                       help="CSV file to predict from")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    print("🎵 Aamati Mood Prediction System")
    print("=" * 50)
    
    # Load models
    print("🤖 Loading models...")
    models = load_prediction_models()
    
    if not models['main_mood_model']:
        print("❌ Main mood model not available. Please train models first.")
        sys.exit(1)
    
    # Run predictions
    predict_from_csv(args.csv_file, models)
    
    print("\n🎉 Prediction completed successfully!")


if __name__ == "__main__":
    main()