#!/usr/bin/env python3
"""
Optimized Mood Classifier for Aamati
Advanced mood classification with primary/secondary mood combinations and enhanced accuracy.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
import warnings
warnings.filterwarnings('ignore')

# Add parent directory to path for logging
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from logging_config import get_logger, log_performance

# Setup logger
logger = get_logger("aamati.mood_classifier")


class OptimizedMoodClassifier:
    """Advanced mood classifier with primary/secondary mood combinations."""
    
    def __init__(self):
        """Initialize the optimized mood classifier."""
        self.primary_classifier = None
        self.secondary_classifier = None
        self.combination_classifier = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_importance = {}
        self.mood_combinations = {}
        
        # Enhanced mood mapping with emotional characteristics
        self.mood_characteristics = {
            'chill': {'energy': 0.2, 'tension': 0.1, 'complexity': 0.3, 'danceability': 0.4},
            'energetic': {'energy': 0.9, 'tension': 0.6, 'complexity': 0.7, 'danceability': 0.9},
            'suspenseful': {'energy': 0.6, 'tension': 0.9, 'complexity': 0.8, 'danceability': 0.3},
            'uplifting': {'energy': 0.8, 'tension': 0.2, 'complexity': 0.5, 'danceability': 0.8},
            'ominous': {'energy': 0.4, 'tension': 0.8, 'complexity': 0.6, 'danceability': 0.2},
            'romantic': {'energy': 0.3, 'tension': 0.3, 'complexity': 0.7, 'danceability': 0.5},
            'gritty': {'energy': 0.7, 'tension': 0.7, 'complexity': 0.6, 'danceability': 0.6},
            'dreamy': {'energy': 0.2, 'tension': 0.1, 'complexity': 0.8, 'danceability': 0.3},
            'frantic': {'energy': 0.95, 'tension': 0.9, 'complexity': 0.9, 'danceability': 0.7},
            'focused': {'energy': 0.6, 'tension': 0.4, 'complexity': 0.4, 'danceability': 0.6}
        }
        
        # Mood combination weights (primary mood gets more weight)
        self.combination_weights = {
            'primary': 0.7,
            'secondary': 0.3
        }
    
    @log_performance("load_and_prepare_data")
    def load_and_prepare_data(self, csv_path: str):
        """Load and prepare data for training."""
        logger.info(f"Loading data from: {csv_path}")
        
        try:
            # Load data
            data = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(data)} samples")
            
            # Check for required columns
            required_cols = ['primary_mood', 'secondary_mood', 'tempo', 'swing', 'density', 
                           'dynamic_range', 'energy', 'velocity_mean', 'velocity_std',
                           'pitch_mean', 'pitch_range', 'avg_polyphony', 'syncopation', 'onset_entropy']
            
            missing_cols = [col for col in required_cols if col not in data.columns]
            if missing_cols:
                logger.warning(f"Missing columns: {missing_cols}")
                # Use fallback columns if available
                if 'mood' in data.columns and 'primary_mood' not in data.columns:
                    data['primary_mood'] = data['mood']
                    data['secondary_mood'] = data['mood']
                    logger.info("Using 'mood' column as both primary and secondary mood")
            
            # Clean data
            data = data.dropna(subset=required_cols)
            logger.info(f"After cleaning: {len(data)} samples")
            
            # Create mood combinations
            data['mood_combination'] = data['primary_mood'] + '_' + data['secondary_mood']
            
            # Feature engineering
            data = self._engineer_features(data)
            
            return data
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def _engineer_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Engineer additional features for better classification."""
        logger.info("Engineering additional features...")
        
        # Musical complexity features
        data['harmonic_complexity'] = data['pitch_range'] * data['avg_polyphony'] / 100
        data['rhythmic_complexity'] = data['syncopation'] * data['onset_entropy']
        data['dynamic_complexity'] = data['dynamic_range'] * data['velocity_std'] / 100
        
        # Energy features
        data['energy_intensity'] = data['energy'] * data['density'] / 100
        data['tempo_energy'] = data['tempo'] * data['energy'] / 1000
        
        # Groove features
        data['groove_swing'] = data['swing'] * data['density'] / 100
        data['groove_consistency'] = 1 / (1 + data['velocity_std'] / 100)
        
        # Emotional features based on mood characteristics
        for mood, chars in self.mood_characteristics.items():
            data[f'{mood}_energy_match'] = np.abs(data['energy'] / 100 - chars['energy'])
            data[f'{mood}_tension_match'] = np.abs(data['syncopation'] - chars['tension'])
            data[f'{mood}_complexity_match'] = np.abs(data['harmonic_complexity'] - chars['complexity'])
            data[f'{mood}_danceability_match'] = np.abs(data['groove_swing'] - chars['danceability'])
        
        logger.info("Feature engineering completed")
        return data
    
    @log_performance("train_classifiers")
    def train_classifiers(self, data: pd.DataFrame):
        """Train primary, secondary, and combination classifiers."""
        logger.info("Training mood classifiers...")
        
        # Prepare features
        feature_cols = [
            'tempo', 'swing', 'density', 'dynamic_range', 'energy',
            'velocity_mean', 'velocity_std', 'pitch_mean', 'pitch_range',
            'avg_polyphony', 'syncopation', 'onset_entropy',
            'harmonic_complexity', 'rhythmic_complexity', 'dynamic_complexity',
            'energy_intensity', 'tempo_energy', 'groove_swing', 'groove_consistency'
        ]
        
        # Add mood characteristic features
        for mood in self.mood_characteristics.keys():
            feature_cols.extend([f'{mood}_energy_match', f'{mood}_tension_match', 
                               f'{mood}_complexity_match', f'{mood}_danceability_match'])
        
        X = data[feature_cols].values
        y_primary = data['primary_mood'].values
        y_secondary = data['secondary_mood'].values
        y_combination = data['mood_combination'].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train primary mood classifier
        logger.info("Training primary mood classifier...")
        self.primary_classifier = self._train_classifier(X_scaled, y_primary, "primary")
        
        # Train secondary mood classifier
        logger.info("Training secondary mood classifier...")
        self.secondary_classifier = self._train_classifier(X_scaled, y_secondary, "secondary")
        
        # Train combination classifier
        logger.info("Training mood combination classifier...")
        self.combination_classifier = self._train_classifier(X_scaled, y_combination, "combination")
        
        # Store feature importance
        self.feature_importance = {
            'primary': dict(zip(feature_cols, self.primary_classifier.feature_importances_)),
            'secondary': dict(zip(feature_cols, self.secondary_classifier.feature_importances_)),
            'combination': dict(zip(feature_cols, self.combination_classifier.feature_importances_))
        }
        
        logger.info("All classifiers trained successfully")
    
    def _train_classifier(self, X, y, classifier_type):
        """Train a single classifier with optimized parameters."""
        # Create pipeline with SMOTE for handling imbalanced data
        pipeline = ImbPipeline([
            ('smote', SMOTE(random_state=42, k_neighbors=3)),
            ('classifier', RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                min_samples_leaf=2,
                max_features='sqrt',
                random_state=42,
                n_jobs=-1
            ))
        ])
        
        # Train the pipeline
        pipeline.fit(X, y)
        
        # Get the classifier from the pipeline
        classifier = pipeline.named_steps['classifier']
        
        # Cross-validation score
        cv_scores = cross_val_score(classifier, X, y, cv=5, scoring='accuracy')
        logger.info(f"{classifier_type} classifier CV accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
        
        return classifier
    
    @log_performance("predict_mood")
    def predict_mood(self, features: dict) -> dict:
        """Predict primary and secondary mood with confidence scores."""
        logger.info("Predicting mood from features...")
        
        try:
            # Convert features to DataFrame
            feature_df = pd.DataFrame([features])
            
            # Engineer features
            feature_df = self._engineer_features(feature_df)
            
            # Select features
            feature_cols = [
                'tempo', 'swing', 'density', 'dynamic_range', 'energy',
                'velocity_mean', 'velocity_std', 'pitch_mean', 'pitch_range',
                'avg_polyphony', 'syncopation', 'onset_entropy',
                'harmonic_complexity', 'rhythmic_complexity', 'dynamic_complexity',
                'energy_intensity', 'tempo_energy', 'groove_swing', 'groove_consistency'
            ]
            
            # Add mood characteristic features
            for mood in self.mood_characteristics.keys():
                feature_cols.extend([f'{mood}_energy_match', f'{mood}_tension_match', 
                                   f'{mood}_complexity_match', f'{mood}_danceability_match'])
            
            X = feature_df[feature_cols].values
            X_scaled = self.scaler.transform(X)
            
            # Predict primary mood
            primary_pred = self.primary_classifier.predict(X_scaled)[0]
            primary_proba = self.primary_classifier.predict_proba(X_scaled)[0]
            primary_confidence = np.max(primary_proba)
            
            # Predict secondary mood
            secondary_pred = self.secondary_classifier.predict(X_scaled)[0]
            secondary_proba = self.secondary_classifier.predict_proba(X_scaled)[0]
            secondary_confidence = np.max(secondary_proba)
            
            # Predict combination
            combination_pred = self.combination_classifier.predict(X_scaled)[0]
            combination_proba = self.combination_classifier.predict_proba(X_scaled)[0]
            combination_confidence = np.max(combination_proba)
            
            # Calculate weighted confidence
            weighted_confidence = (primary_confidence * self.combination_weights['primary'] + 
                                 secondary_confidence * self.combination_weights['secondary'])
            
            result = {
                'primary_mood': primary_pred,
                'secondary_mood': secondary_pred,
                'mood_combination': combination_pred,
                'primary_confidence': float(primary_confidence),
                'secondary_confidence': float(secondary_confidence),
                'combination_confidence': float(combination_confidence),
                'weighted_confidence': float(weighted_confidence),
                'emotional_characteristics': self.mood_characteristics.get(primary_pred, {}),
                'recommended_presets': self._get_recommended_presets(primary_pred, secondary_pred)
            }
            
            logger.info(f"Predicted mood: {primary_pred} + {secondary_pred} (confidence: {weighted_confidence:.3f})")
            return result
            
        except Exception as e:
            logger.error(f"Error predicting mood: {e}")
            return {
                'primary_mood': 'unknown',
                'secondary_mood': 'unknown',
                'mood_combination': 'unknown_unknown',
                'primary_confidence': 0.0,
                'secondary_confidence': 0.0,
                'combination_confidence': 0.0,
                'weighted_confidence': 0.0,
                'emotional_characteristics': {},
                'recommended_presets': []
            }
    
    def _get_recommended_presets(self, primary_mood: str, secondary_mood: str) -> list:
        """Get recommended presets based on mood combination."""
        presets = []
        
        # Base presets for primary mood
        primary_presets = {
            'chill': ['ambient_pad', 'soft_arpeggio', 'reverb_wash'],
            'energetic': ['driving_bass', 'punchy_drums', 'bright_lead'],
            'suspenseful': ['dark_pad', 'tension_build', 'minor_harmony'],
            'uplifting': ['major_chords', 'bright_melody', 'cheerful_rhythm'],
            'ominous': ['low_brass', 'dissonant_harmony', 'sparse_rhythm'],
            'romantic': ['warm_strings', 'smooth_melody', 'gentle_rhythm'],
            'gritty': ['distorted_bass', 'aggressive_rhythm', 'raw_sound'],
            'dreamy': ['ethereal_pad', 'floating_melody', 'soft_reverb'],
            'frantic': ['rapid_arpeggio', 'complex_rhythm', 'high_energy'],
            'focused': ['steady_rhythm', 'clear_melody', 'balanced_mix']
        }
        
        # Secondary mood modifications
        secondary_modifications = {
            'chill': ['reduce_velocity', 'add_reverb', 'soften_attack'],
            'energetic': ['increase_velocity', 'add_punch', 'brighten_tone'],
            'suspenseful': ['add_tension', 'minor_harmony', 'build_anticipation'],
            'uplifting': ['major_harmony', 'brighten_tone', 'add_cheer'],
            'ominous': ['darken_tone', 'add_dissonance', 'reduce_brightness'],
            'romantic': ['warm_tone', 'smooth_legato', 'add_expression'],
            'gritty': ['add_distortion', 'increase_attack', 'raw_sound'],
            'dreamy': ['add_reverb', 'soften_edges', 'ethereal_tone'],
            'frantic': ['increase_tempo', 'add_complexity', 'high_energy'],
            'focused': ['clarify_mix', 'steady_rhythm', 'balanced_tone']
        }
        
        # Combine presets
        if primary_mood in primary_presets:
            presets.extend(primary_presets[primary_mood])
        
        if secondary_mood in secondary_modifications:
            presets.extend(secondary_modifications[secondary_mood])
        
        return list(set(presets))  # Remove duplicates
    
    def save_models(self, output_dir: str = "models/trained"):
        """Save trained models and scalers."""
        logger.info(f"Saving models to: {output_dir}")
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save individual models
        joblib.dump(self.primary_classifier, f"{output_dir}/primary_mood_classifier.joblib")
        joblib.dump(self.secondary_classifier, f"{output_dir}/secondary_mood_classifier.joblib")
        joblib.dump(self.combination_classifier, f"{output_dir}/combination_classifier.joblib")
        joblib.dump(self.scaler, f"{output_dir}/feature_scaler.joblib")
        
        # Save feature importance
        import json
        with open(f"{output_dir}/feature_importance.json", 'w') as f:
            json.dump(self.feature_importance, f, indent=2)
        
        # Convert to ONNX for JUCE
        self._convert_to_onnx(output_dir)
        
        logger.info("Models saved successfully")
    
    def _convert_to_onnx(self, output_dir: str):
        """Convert models to ONNX format for JUCE."""
        logger.info("Converting models to ONNX format...")
        
        try:
            # Define input type
            initial_type = [('float_input', FloatTensorType([None, 19]))]  # Adjust based on feature count
            
            # Convert primary classifier
            onnx_model_primary = convert_sklearn(
                self.primary_classifier,
                initial_types=initial_type,
                target_opset=11
            )
            
            with open(f"{output_dir}/primary_mood_classifier.onnx", "wb") as f:
                f.write(onnx_model_primary.SerializeToString())
            
            # Convert secondary classifier
            onnx_model_secondary = convert_sklearn(
                self.secondary_classifier,
                initial_types=initial_type,
                target_opset=11
            )
            
            with open(f"{output_dir}/secondary_mood_classifier.onnx", "wb") as f:
                f.write(onnx_model_secondary.SerializeToString())
            
            # Convert combination classifier
            onnx_model_combination = convert_sklearn(
                self.combination_classifier,
                initial_types=initial_type,
                target_opset=11
            )
            
            with open(f"{output_dir}/combination_classifier.onnx", "wb") as f:
                f.write(onnx_model_combination.SerializeToString())
            
            logger.info("ONNX models created successfully")
            
        except Exception as e:
            logger.error(f"Error converting to ONNX: {e}")


def main():
    """Main training function."""
    logger.info("Starting optimized mood classifier training...")
    
    # Initialize classifier
    classifier = OptimizedMoodClassifier()
    
    # Load and prepare data
    data = classifier.load_and_prepare_data("data/csv/groove_features_log_for_pred.csv")
    
    # Train classifiers
    classifier.train_classifiers(data)
    
    # Save models
    classifier.save_models()
    
    # Test prediction
    test_features = {
        'tempo': 120, 'swing': 0.5, 'density': 15.0, 'dynamic_range': 80.0,
        'energy': 8.0, 'velocity_mean': 70.0, 'velocity_std': 15.0,
        'pitch_mean': 60.0, 'pitch_range': 24.0, 'avg_polyphony': 3.0,
        'syncopation': 0.1, 'onset_entropy': 0.5
    }
    
    prediction = classifier.predict_mood(test_features)
    logger.info(f"Test prediction: {prediction}")
    
    logger.info("Optimized mood classifier training completed!")


if __name__ == "__main__":
    main()
