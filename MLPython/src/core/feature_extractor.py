"""
Core feature extraction functionality for MIDI files and audio analysis.
"""

import os
import pretty_midi
import pandas as pd
import numpy as np
import datetime
import scipy.stats
import scipy.signal
import json
from typing import Dict, Optional, List, Tuple
from joblib import load

from ..utils.mood_mappings import (
    MOOD_FEATURE_MAP, 
    TIMING_FEEL_MAP, 
    RHYTHMIC_DENSITY_MAP,
    DYNAMIC_INTENSITY_MAP,
    FILL_ACTIVITY_MAP,
    FX_CHARACTER_MAP
)


class FeatureExtractor:
    """Main feature extraction class for MIDI and audio analysis."""
    
    def __init__(self, models_dir: str = "models"):
        """Initialize feature extractor with model directory."""
        self.models_dir = models_dir
        self.models = self._load_models()
        
    def _load_models(self) -> Dict:
        """Load all required ML models."""
        models = {}
        model_files = {
            'energy_model': 'energy_random_forest.joblib',
            'dynamic_intensity_model': 'dynamic_intensity_randomforest.joblib',
            'swing_model': 'swing_random_forest.joblib',
            'fill_activity_model': 'fill_activity_randomforest.joblib',
            'rhythm_model': 'rhythmic_density_ordinal_regression.joblib',
            'fx_model': 'fx_character_classifier.joblib',
            'timing_feel_model': 'timing_feel_randomforest.joblib'
        }
        
        for name, filename in model_files.items():
            model_path = os.path.join(self.models_dir, filename)
            if os.path.exists(model_path):
                try:
                    models[name] = load(model_path)
                    print(f"✅ Loaded {name}")
                except Exception as e:
                    print(f"⚠️ Failed to load {name}: {e}")
                    models[name] = None
            else:
                print(f"⚠️ Model file not found: {model_path}")
                models[name] = None
                
        return models
    
    def estimate_swing(self, note_starts: np.ndarray) -> float:
        """Estimate swing from note onset times."""
        MIN_NOTES = 12
        TOLERANCE = 0.003

        sorted_starts = np.sort(note_starts)
        iois = np.diff(sorted_starts)

        if len(iois) < MIN_NOTES:
            return 0.0

        # Filter out outlier IOIs
        median_ioi = np.median(iois)
        std_ioi = np.std(iois)
        clipped_iois = np.clip(iois, median_ioi - 3*std_ioi, median_ioi + 3*std_ioi)

        # Smooth IOIs with median filter
        smoothed_iois = scipy.signal.medfilt(clipped_iois, kernel_size=3)

        if np.std(smoothed_iois) < TOLERANCE:
            return 0.0

        # Separate odd and even IOIs
        odd_iois = smoothed_iois[0::2]
        even_iois = smoothed_iois[1::2]

        if len(odd_iois) < 3 or len(even_iois) < 3:
            return 0.0

        mean_odd = np.mean(odd_iois)
        mean_even = np.mean(even_iois)
        if mean_even == 0:
            return 0.0

        swing_ratio = mean_odd / mean_even
        swing_amount = abs(swing_ratio - 1.0)
        scaled_swing = min(swing_amount, 1.0)

        return round(scaled_swing, 4)
    
    def extract_basic_features(self, midi_path: str) -> Optional[Dict]:
        """Extract basic features from MIDI file."""
        try:
            pm = pretty_midi.PrettyMIDI(midi_path)
            tempo = np.mean(pm.get_tempo_changes()[1]) if pm.get_tempo_changes()[1].size > 0 else 120

            note_starts, note_ends, velocities, pitches, timeline = [], [], [], [], []

            for instrument in pm.instruments:
                for note in instrument.notes:
                    note_starts.append(note.start)
                    note_ends.append(note.end)
                    velocities.append(note.velocity)
                    pitches.append(note.pitch)
                    timeline.append((note.start, +1))
                    timeline.append((note.end, -1))

            if len(note_starts) < 2:
                print(f"Not enough notes in {midi_path} for feature extraction.")
                return None

            note_lengths = np.array(note_ends) - np.array(note_starts)
            velocity_mean = np.mean(velocities)
            duration = pm.get_end_time()
            density = len(note_starts) / duration if duration > 0 else 0
            
            # Calculate dynamic range
            velocities_np = np.array(velocities)
            dynamic_range = np.max(velocities_np) - np.min(velocities_np)
            if dynamic_range < 1e-3:
                dynamic_range = np.std(velocities_np)
            
            # Calculate polyphony
            timeline.sort()
            polyphony_counts = []
            active_notes = 0
            for _, event in timeline:
                active_notes += event
                polyphony_counts.append(active_notes)
            
            avg_polyphony = np.mean(polyphony_counts)
            iois = np.diff(np.sort(note_starts))

            return {
                'tempo': tempo,
                'density': density,
                'dynamic_range': dynamic_range,
                'mean_note_length': np.mean(note_lengths),
                'std_note_length': np.std(note_lengths),
                'velocity_mean': velocity_mean,
                'velocity_std': np.std(velocities),
                'pitch_mean': np.mean(pitches),
                'pitch_range': np.max(pitches) - np.min(pitches),
                'avg_polyphony': avg_polyphony,
                'syncopation': np.var(iois) if len(iois) > 1 else 0,
                'onset_entropy': scipy.stats.entropy(np.histogram(iois, bins=10)[0] + 1) if len(iois) > 1 else 0,
                'instrument_count': len(pm.instruments),
                'timestamp': datetime.datetime.now().isoformat()
            }

        except Exception as e:
            print(f"Error processing {midi_path}: {e}")
            return None
    
    def predict_ml_features(self, features: Dict) -> Dict:
        """Predict ML-based features using trained models."""
        if not self.models:
            print("⚠️ No models loaded, returning basic features only")
            return features
            
        # Predict energy
        if self.models['energy_model']:
            energy_input = pd.DataFrame([{
                'density': features['density'],
                'velocity_mean': features['velocity_mean'],
                'dynamic_range': features['dynamic_range'],
                'avg_polyphony': features['avg_polyphony']
            }])
            features['energy'] = float(self.models['energy_model'].predict(energy_input)[0])
        else:
            features['energy'] = 0.0
            
        # Predict swing
        if self.models['swing_model']:
            swing_input = pd.DataFrame([{
                'density': features['density'],
                'velocity_mean': features['velocity_mean'],
                'dynamic_range': features['dynamic_range'],
                'avg_polyphony': features['avg_polyphony'],
                'syncopation': features['syncopation'],
                'onset_entropy': features['onset_entropy'],
                'rhythmic_density': -1  # placeholder
            }])
            features['swing'] = float(self.models['swing_model'].predict(swing_input)[0])
        else:
            features['swing'] = 0.0
            
        # Predict rhythmic density
        if self.models['rhythm_model']:
            rhythm_input = pd.DataFrame([{
                'density': features['density'],
                'syncopation': features['syncopation'],
                'std_note_length': features['std_note_length']
            }])
            features['rhythmic_density'] = int(self.models['rhythm_model'].predict(rhythm_input)[0])
        else:
            features['rhythmic_density'] = 0
            
        # Update swing with rhythmic density
        if self.models['swing_model']:
            swing_input = pd.DataFrame([{
                'density': features['density'],
                'velocity_mean': features['velocity_mean'],
                'dynamic_range': features['dynamic_range'],
                'avg_polyphony': features['avg_polyphony'],
                'syncopation': features['syncopation'],
                'onset_entropy': features['onset_entropy'],
                'rhythmic_density': features['rhythmic_density']
            }])
            features['swing'] = float(self.models['swing_model'].predict(swing_input)[0])
            
        # Predict timing feel
        if self.models['timing_feel_model']:
            timing_input = pd.DataFrame([{
                'swing': features['swing'],
                'syncopation': features['syncopation'],
                'onset_entropy': features['onset_entropy'],
                'pitch_range': features['pitch_range'],
                'density': features['density'],
                'velocity_std': features['velocity_std'],
                'avg_polyphony': features['avg_polyphony'],
                'dynamic_range': features['dynamic_range']
            }])
            features['timing_feel'] = int(self.models['timing_feel_model'].predict(timing_input)[0])
        else:
            features['timing_feel'] = 0
            
        # Predict dynamic intensity
        if self.models['dynamic_intensity_model']:
            dynamic_input = pd.DataFrame([{
                'velocity_mean': features['velocity_mean'],
                'dynamic_range': features['dynamic_range'],
                'velocity_std': features['velocity_std']
            }])
            features['dynamic_intensity'] = int(self.models['dynamic_intensity_model'].predict(dynamic_input)[0])
        else:
            features['dynamic_intensity'] = 0
            
        # Predict fill activity
        if self.models['fill_activity_model']:
            fill_input = pd.DataFrame([{
                'pitch_range': features['pitch_range'],
                'velocity_std': features['velocity_std'],
                'onset_entropy': features['onset_entropy'],
                'syncopation': features['syncopation'],
                'density': features['density'],
                'avg_polyphony': features['avg_polyphony'],
                'std_note_length': features['std_note_length'],
                'energy': features['energy']
            }])
            features['fill_activity'] = int(self.models['fill_activity_model'].predict(fill_input)[0])
        else:
            features['fill_activity'] = 0
            
        # Predict FX character
        if self.models['fx_model']:
            fx_input = pd.DataFrame([{
                'instrument_count': features['instrument_count'],
                'onset_entropy': features['onset_entropy'],
                'pitch_range': features['pitch_range'],
                'entropy_pitch_interaction': features['onset_entropy'] * features['pitch_range'],
                'instr_entropy_interaction': features['instrument_count'] * features['onset_entropy']
            }])
            features['fx_character'] = int(self.models['fx_model'].predict(fx_input)[0])
        else:
            features['fx_character'] = 0
            
        return features
    
    def extract_features(self, midi_path: str) -> Optional[Dict]:
        """Extract all features from MIDI file."""
        basic_features = self.extract_basic_features(midi_path)
        if basic_features is None:
            return None
            
        return self.predict_ml_features(basic_features)
    
    def append_to_log(self, new_data: pd.DataFrame, log_csv: str, current_csv: str):
        """Append new data to log files."""
        columns = [
            'tempo', 'swing', 'density', 'dynamic_range', 'energy',
            'mean_note_length', 'std_note_length', 'velocity_mean', 'velocity_std',
            'pitch_mean', 'pitch_range', 'avg_polyphony', 'syncopation',
            'onset_entropy', 'instrument_count',
            'primary_mood', 'secondary_mood', 'timing_feel', 'rhythmic_density', 
            'dynamic_intensity', 'fill_activity', 'fx_character', 'timestamp', 'midi_file_name'
        ]
        
        if os.path.exists(log_csv):
            old = pd.read_csv(log_csv)
            if 'midi_file_name' not in old.columns:
                old['midi_file_name'] = ''
            new_data_clean = new_data.dropna(axis=1, how='all')
            combined = pd.concat([old, new_data_clean], ignore_index=True)
        else:
            combined = new_data
            
        combined[columns].to_csv(log_csv, index=False, float_format="%.4f")
        new_data[columns].to_csv(current_csv, index=False, float_format="%.4f")
        print(f"Appended to {log_csv} and updated {current_csv}")
