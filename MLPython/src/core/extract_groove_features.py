"""
Core feature extraction functionality for MIDI files.
This is the main extraction engine for the Aamati ML system.
"""

import os
import pretty_midi
import pandas as pd
import numpy as np
import datetime
import scipy.stats
import scipy.signal
import json
import time
from joblib import load
from pathlib import Path

# Add parent directory to path for logging
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
from logging_config import get_logger, log_performance

# Setup logger
logger = get_logger("aamati.feature_extraction")

# Import data analysis models
def load_models():
    """Load all required ML models."""
    models = {}
    model_files = {
        'energy_model': 'ModelClassificationScripts/models/energy_random_forest.joblib',
        'dynamic_intensity_model': 'ModelClassificationScripts/models/dynamic_intensity_randomforest.joblib',
        'swing_model': 'ModelClassificationScripts/models/swing_random_forest.joblib',
        'fill_activity_model': 'ModelClassificationScripts/models/fill_activity_randomforest.joblib',
        'rhythm_model': 'ModelClassificationScripts/models/rhythmic_density_ordinal_regression.joblib',
        'fx_model': 'ModelClassificationScripts/models/fx_character_classifier.joblib',
        'timing_feel_model': 'ModelClassificationScripts/models/timing_feel_randomforest.joblib'
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

# Load models
models = load_models()


# Define mood-to-feature mapping
mood_feature_map = {
    "chill": {"timing_feel": "loose", "rhythmic_density": "low", "dynamic_intensity": "soft", "fill_activity": "sparse", "fx_character": "wet, wide, airy"},
    "energetic": {"timing_feel": "tight", "rhythmic_density": "high", "dynamic_intensity": "hard", "fill_activity": "frequent", "fx_character": "dry, punchy, sharp"},
    "suspenseful": {"timing_feel": "mid", "rhythmic_density": "medium", "dynamic_intensity": "varied", "fill_activity": "moderate", "fx_character": "dark, modulated, narrow"},
    "uplifting": {"timing_feel": "mid", "rhythmic_density": "high", "dynamic_intensity": "bright", "fill_activity": "medium", "fx_character": "shimmery, wide, echoing"},
    "ominous": {"timing_feel": "tight", "rhythmic_density": "medium", "dynamic_intensity": "deep", "fill_activity": "sparse", "fx_character": "saturated, low-end heavy"},
    "romantic": {"timing_feel": "loose", "rhythmic_density": "medium", "dynamic_intensity": "gentle", "fill_activity": "occasional", "fx_character": "warm, lush, resonant"},
    "gritty": {"timing_feel": "tight", "rhythmic_density": "high", "dynamic_intensity": "harsh", "fill_activity": "irregular", "fx_character": "distorted, mono, rough"},
    "dreamy": {"timing_feel": "loose", "rhythmic_density": "low", "dynamic_intensity": "light", "fill_activity": "sparse", "fx_character": "reverb-heavy, washed-out"},
    "frantic": {"timing_feel": "random", "rhythmic_density": "very_high", "dynamic_intensity": "wild", "fill_activity": "bursty", "fx_character": "glitchy, stuttered, noisy"},
    "focused": {"timing_feel": "tight", "rhythmic_density": "medium", "dynamic_intensity": "consistent", "fill_activity": "minimal", "fx_character": "clean, subtle, precise"}
}

# Define numeric mappings
timing_feel_map = {'tight': 0, 'mid': 1, 'loose': 2, 'random': 3}
rhythmic_density_map = {'low': 0, 'medium': 1, 'high': 2, 'very_high': 3}
dynamic_intensity_map = {'soft': 0, 'gentle': 1, 'light': 2, 'bright': 3, 'deep': 4, 'varied': 5, 'consistent': 6, 'hard': 7, 'harsh': 8, 'wild': 9}
fill_activity_map = {'sparse': 0, 'minimal': 1, 'occasional': 2, 'moderate': 3, 'medium': 4, 'frequent': 5, 'bursty': 6, 'irregular': 7}
fx_character_map = {
    'wet, wide, airy': 0, 'dry, punchy, sharp': 1, 'dark, modulated, narrow': 2,
    'shimmery, wide, echoing': 3, 'saturated, low-end heavy': 4, 'warm, lush, resonant': 5,
    'distorted, mono, rough': 6, 'reverb-heavy, washed-out': 7, 'glitchy, stuttered, noisy': 8,
    'clean, subtle, precise': 9
}

def estimate_swing(note_starts):

    MIN_NOTES = 12  # need more notes for reliability
    TOLERANCE = 0.003  # stricter tolerance for quantized rhythms

    sorted_starts = np.sort(note_starts)
    iois = np.diff(sorted_starts)

    if len(iois) < MIN_NOTES:
        return 0.0  # not enough data

    # Filter out outlier IOIs by clipping to median +/- 3*std
    median_ioi = np.median(iois)
    std_ioi = np.std(iois)
    clipped_iois = np.clip(iois, median_ioi - 3*std_ioi, median_ioi + 3*std_ioi)

    # Smooth IOIs with median filter (window size 3)
    smoothed_iois = scipy.signal.medfilt(clipped_iois, kernel_size=3)

    # If rhythm is too uniform, no swing
    if np.std(smoothed_iois) < TOLERANCE:
        return 0.0

    # Separate odd and even IOIs (1st, 3rd, 5th...) and (2nd, 4th, 6th...)
    odd_iois = smoothed_iois[0::2]
    even_iois = smoothed_iois[1::2]

    if len(odd_iois) < 3 or len(even_iois) < 3:
        return 0.0

    mean_odd = np.mean(odd_iois)
    mean_even = np.mean(even_iois)
    if mean_even == 0:
        return 0.0

    # Compute swing ratio, difference from 1 means swing amount
    swing_ratio = mean_odd / mean_even
    swing_amount = abs(swing_ratio - 1.0)

    # Scale swing_amount nonlinearly to emphasize common swing ranges
    scaled_swing = min(swing_amount, 1.0)

    return round(scaled_swing, 4)

@log_performance("extract_features")
def extract_features(midi_path):
    """Extract comprehensive features from a MIDI file."""
    logger.info(f"Starting feature extraction for: {midi_path}")
    
    try:
        pm = pretty_midi.PrettyMIDI(midi_path)
        logger.debug(f"Successfully loaded MIDI file: {midi_path}")
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
        quarter_note = 60.0 / tempo
        eighth_note = quarter_note / 2
        #quant_grid = np.round(np.array(note_starts) / eighth_note) * eighth_note
        #swing = estimate_swing(note_starts)
        #swing = np.mean(np.abs(np.array(note_starts) - np.round(np.array(note_starts) * 2) / 2)) # OLD swing equation
        dynamic_range = np.max(velocities) - np.min(velocities)
        
        timeline.sort()
        polyphony_counts = []
        active_notes = 0
        for _, event in timeline:
            active_notes += event
            polyphony_counts.append(active_notes)

        iois = np.diff(np.sort(note_starts))
        avg_polyphony = np.mean(polyphony_counts)
        peak_polyphony = np.max(polyphony_counts) # just to have, maybe used for later
        
        # dynamic range calculation
        velocities_np = np.array(velocities)
        dynamic_range = np.max(velocities_np) - np.min(velocities_np)
        if dynamic_range < 1e-3:
                dynamic_range = np.std(velocities_np)
        
        # Enhanced energy calculation with multiple factors
        if models['energy_model']:
            # Use more comprehensive features for energy prediction
            input_features = pd.DataFrame([{ 
                'density': density,
                'velocity_mean': velocity_mean,
                'dynamic_range': dynamic_range,
                'avg_polyphony': avg_polyphony,
                'tempo': tempo,
                'syncopation': np.var(iois) if len(iois) > 1 else 0,
                'onset_entropy': scipy.stats.entropy(np.histogram(iois, bins=10)[0] + 1) if len(iois) > 1 else 0
            }])
            energy = float(models['energy_model'].predict(input_features)[0])
        else:
            # Fallback energy calculation based on musical characteristics
            energy = min(17, max(0, (
                (tempo / 200.0) * 0.3 +  # Tempo contribution
                (density / 50.0) * 0.4 +  # Density contribution
                (velocity_mean / 127.0) * 0.2 +  # Velocity contribution
                (dynamic_range / 127.0) * 0.1  # Dynamic range contribution
            ) * 17))
        
        # Enhanced swing calculation with improved algorithm
        if models['swing_model']:
            swing_input_df = pd.DataFrame([{
                'density': density,
                'velocity_mean': velocity_mean,
                'dynamic_range': dynamic_range,
                'avg_polyphony': avg_polyphony,
                'syncopation': np.var(iois) if len(iois) > 1 else 0,
                'onset_entropy': scipy.stats.entropy(np.histogram(iois, bins=10)[0] + 1) if len(iois) > 1 else 0,
                'rhythmic_density': density * tempo / 1000  # Improved rhythmic density calculation
            }])
            swing = float(models['swing_model'].predict(swing_input_df)[0])
        else:
            # Enhanced fallback swing calculation
            swing = estimate_swing(note_starts)
            # Apply tempo-based swing adjustment
            tempo_factor = min(1.0, tempo / 120.0)  # Normalize to 120 BPM
            swing = swing * tempo_factor

        features = {
            'tempo': tempo,
            'swing': swing,
            'density': density,
            'dynamic_range': dynamic_range,
            'energy': energy,
            'mean_note_length': np.mean(note_lengths),
            'std_note_length': np.std(note_lengths),
            'velocity_mean': velocity_mean,
            'velocity_std': np.std(velocities),
            'pitch_mean': np.mean(pitches),
            'pitch_range': np.max(pitches) - np.min(pitches),
            'avg_polyphony': np.mean(polyphony_counts),
            'syncopation': np.var(iois) if len(iois) > 1 else 0,
            'onset_entropy': scipy.stats.entropy(np.histogram(iois, bins=10)[0] + 1) if len(iois) > 1 else 0,
            'instrument_count': len(pm.instruments),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        # Log feature extraction
        logger.log_feature_extraction(midi_path, features)
        logger.info(f"Successfully extracted features for: {midi_path}")
        
        return features

    except Exception as e:
        logger.error(f"Error processing {midi_path}: {e}")
        return None

def append_to_log(new_data: pd.DataFrame, log_csv: str, current_csv: str):
    columns = [
        'tempo', 'swing', 'density', 'dynamic_range', 'energy',
        'mean_note_length', 'std_note_length', 'velocity_mean', 'velocity_std',
        'pitch_mean', 'pitch_range', 'avg_polyphony', 'syncopation',
        'onset_entropy', 'instrument_count',
        'primary_mood','secondary_mood', 'timing_feel', 'rhythmic_density', 'dynamic_intensity',
        'fill_activity', 'fx_character', 'timestamp','midi_file_name'
    ]
    
    if os.path.exists(log_csv):
        old = pd.read_csv(log_csv)
        if 'midi_file_name' not in old.columns:
            old['midi_file_name'] = ''  #   Blank for old rows
        # Drop empty/all-NA columns to avoid FutureWarning
        # old = old.dropna(axis=1, how='all')
        new_data_clean = new_data.dropna(axis=1, how='all')
        combined = pd.concat([old, new_data_clean], ignore_index=True)

    else:
        combined = new_data
    combined[columns].to_csv(log_csv, index=False, float_format="%.4f") # append to log
    new_data[columns].to_csv(current_csv, index=False, float_format="%.4f") # overwrite
    print(f"Appended to {log_csv} and updated {current_csv}")


# def extract_full_feature_vector(midi_path, default_mood="unknown"):
#     features = extract_features(midi_path)
#     if features is None:
#         return None

#     # Predict timing feel
#     features_df = pd.DataFrame([{
#         'swing': features['swing'],
#         'syncopation': features['syncopation'],
#         'onset_entropy': features['onset_entropy'],
#         'pitch_range': features['pitch_range'],
#         'density': features['density'],
#         'velocity_std': features['velocity_std'],
#         'avg_polyphony': features['avg_polyphony'],
#         'dynamic_range': features['dynamic_range']
#     }])
#     features['timing_feel'] = int(timing_feel_model.predict(features_df)[0])

#     # Predict rhythmic density
#     rhythm_features = pd.DataFrame([{
#         'density': features['density'],
#         'syncopation': features['syncopation'],
#         'std_note_length': features['std_note_length']
#     }])
#     features['rhythmic_density'] = int(rhythm_model.predict(rhythm_features)[0])

#     # Predict dynamic intensity
#     dyn_features = pd.DataFrame([{
#         'velocity_mean': features['velocity_mean'],
#         'dynamic_range': features['dynamic_range'],
#         'velocity_std': features['velocity_std']
#     }])
#     features['dynamic_intensity'] = int(dynamic_intensity_model.predict(dyn_features)[0])

#     # Predict fill activity
#     fill_features = pd.DataFrame([{
#         'pitch_range': features['pitch_range'],
#         'velocity_std': features['velocity_std'],
#         'onset_entropy': features['onset_entropy'],
#         'syncopation': features['syncopation'],
#         'density': features['density'],
#         'avg_polyphony': features['avg_polyphony'],
#         'std_note_length': features['std_note_length'],
#         'energy': features['energy']
#     }])
#     features['fill_activity'] = int(fill_activity_model.predict(fill_features)[0])

#     # Predict FX character
#     fx_features = pd.DataFrame([{
#         'instrument_count': features['instrument_count'],
#         'onset_entropy': features['onset_entropy'],
#         'pitch_range': features['pitch_range'],
#         'entropy_pitch_interaction': features['onset_entropy'] * features['pitch_range'],
#         'instr_entropy_interaction': features['instrument_count'] * features['onset_entropy']
#     }])
#     label_classes = np.load("ModelClassificationScripts/models/fx_character_label_classes.npy", allow_pickle=True)
#     fx_idx = int(fx_model.predict(fx_features)[0])
#     features['fx_character'] = fx_idx

#     # Optionally tag mood for logging
#     features['mood'] = default_mood

#     return features
        
def main(midi_folder, output_csv, log_csv, interactive=True, batch_size=50, max_files=None):
    records = []
    moods = list(mood_feature_map.keys())
    
    # Ensure output directories exist
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(os.path.dirname(log_csv), exist_ok=True)

    inactive_folder = os.path.join(os.path.dirname(midi_folder), "ProcessedMIDIs")
    os.makedirs(inactive_folder, exist_ok=True)

    # Get list of MIDI files
    midi_files = [f for f in os.listdir(midi_folder) if f.lower().endswith(('.mid', '.midi'))]
    
    if max_files:
        midi_files = midi_files[:max_files]
    
    total_files = len(midi_files)
    print(f"📁 Found {total_files} MIDI files to process")
    
    if total_files == 0:
        print("⚠️ No MIDI files found in the specified folder")
        return

    # Process files in batches
    for batch_start in range(0, total_files, batch_size):
        batch_end = min(batch_start + batch_size, total_files)
        batch_files = midi_files[batch_start:batch_end]
        
        print(f"\n📦 Processing batch {batch_start//batch_size + 1}/{(total_files-1)//batch_size + 1}")
        print(f"   Files {batch_start + 1}-{batch_end} of {total_files}")
        
        for i, filename in enumerate(batch_files):
            file_num = batch_start + i + 1
            print(f"\n🎵 [{file_num}/{total_files}] Processing: {filename}")
            
            midi_path = os.path.join(midi_folder, filename)
            
            try:
                features = extract_features(midi_path)
                if features:
                    print(f"   ✅ Features extracted successfully")
                    if interactive:
                        print(f"   📊 Feature summary:")
                        for k, v in features.items():
                            if isinstance(v, float):
                                print(f"      {k}: {v:.4f}")
                            else:
                                print(f"      {k}: {v}")

                    # Get mood labels
                    if interactive:
                        while True:
                            primary_mood = input(f"🎯 Choose **primary** mood ({'/'.join(moods)}): ").strip().lower()
                            if primary_mood in mood_feature_map:
                                break
                            print("Invalid mood, please try again.")

                        while True:
                            secondary_mood = input(f"🎨 Choose **secondary** mood ({'/'.join(moods)}), or press Enter to default to primary mood: ").strip().lower()
                            if not secondary_mood:  # If user just hits Enter
                                secondary_mood = primary_mood
                                break
                            elif secondary_mood in mood_feature_map:
                                break
                            else:
                                print("Invalid secondary mood, try again.")
                    else:
                        # Non-interactive mode - use default mood or auto-detect
                        primary_mood = "unknown"
                        secondary_mood = "unknown"
                        print(f"   🤖 Using default mood: {primary_mood}")

                    features['primary_mood'] = primary_mood
                    features['secondary_mood'] = secondary_mood if secondary_mood else primary_mood

                    description = mood_feature_map.get(primary_mood, {})

                    syncopation = features['syncopation']
                    onset_entropy = features['onset_entropy']
                    pitch_range = features['pitch_range']
                    density = features['density']
                
                # Extraction
                # Estimate Rhythmic Density
                if models['rhythm_model']:
                    rhythm_features = pd.DataFrame([{ 'density': density,'syncopation': features['syncopation'],'std_note_length': features['std_note_length']}])
                    predicted_rhythmic_density = models['rhythm_model'].predict(rhythm_features)[0]
                    features['rhythmic_density'] = int(predicted_rhythmic_density)
                else:
                    features['rhythmic_density'] = 0

                # Estimate Swing
                swing = features['swing']

                if models['swing_model']:
                    swing_input_df = pd.DataFrame([{
                        'density': features['density'],
                        'velocity_mean': features['velocity_mean'],
                        'dynamic_range': features['dynamic_range'],
                        'avg_polyphony': features['avg_polyphony'],
                        'syncopation': features['syncopation'],
                        'onset_entropy': features['onset_entropy'],
                        'rhythmic_density': features['rhythmic_density']
                    }])

                    # Predict swing using the model
                    predicted_swing = models['swing_model'].predict(swing_input_df)[0]
                    features['swing'] = float(predicted_swing)

                # Estimate Timing Feel
                if models['timing_feel_model']:
                    features_df = pd.DataFrame([{
                        'swing': features['swing'],
                        'syncopation': features['syncopation'],
                        'onset_entropy': features['onset_entropy'],
                        'pitch_range': features['pitch_range'],
                        'density': features['density'],
                        'velocity_std': features['velocity_std'],
                        'avg_polyphony': features['avg_polyphony'],
                        'dynamic_range': features['dynamic_range']
                    }])

                    features['timing_feel'] = int(models['timing_feel_model'].predict(features_df)[0])
                else:
                    features['timing_feel'] = 0
                
                # Estimate Dynamic_Intensity 
                if models['dynamic_intensity_model']:
                    dynamic_input = pd.DataFrame([{ 'velocity_mean': features['velocity_mean'], 'dynamic_range': features['dynamic_range'], 'velocity_std': features['velocity_std']}])
                    pred_dynamic = models['dynamic_intensity_model'].predict(dynamic_input)[0]
                    features['dynamic_intensity'] = int(pred_dynamic)
                else:
                    features['dynamic_intensity'] = 0

                # Estimate Fill Activity on an 8-level scale (0 to 7)
                if models['fill_activity_model']:
                    fill_features = pd.DataFrame([{
                        'pitch_range': features['pitch_range'],
                        'velocity_std': features['velocity_std'],
                        'onset_entropy': features['onset_entropy'],
                        'syncopation': features['syncopation'],
                        'density': features['density'],
                        'avg_polyphony': features['avg_polyphony'],
                        'std_note_length': features['std_note_length'],
                        'energy': features['energy']
                    }])

                    predicted_fill_activity = models['fill_activity_model'].predict(fill_features)[0]
                    features['fill_activity'] = int(predicted_fill_activity)
                else:
                    features['fill_activity'] = 0

                # Estimate Fx Character
                if models['fx_model']:
                    fx_features = pd.DataFrame([{
                        'instrument_count': features['instrument_count'],
                        'onset_entropy': features['onset_entropy'],
                        'pitch_range': features['pitch_range'],
                        'entropy_pitch_interaction': features['onset_entropy'] * features['pitch_range'],
                        'instr_entropy_interaction': features['instrument_count'] * features['onset_entropy'],
                    }])

                    predicted_fx_idx = models['fx_model'].predict(fx_features)[0]
                    # Load label encoder classes
                    label_classes_path = "ModelClassificationScripts/models/fx_character_label_classes.npy"
                    if os.path.exists(label_classes_path):
                        label_classes = np.load(label_classes_path, allow_pickle=True)
                        predicted_fx_label = label_classes[predicted_fx_idx]
                    features['fx_character'] = int(predicted_fx_idx)
                else:
                    features['fx_character'] = 0

                # Add to features record
                features['midi_file_name'] = filename
                records.append(features)
                df_single = pd.DataFrame([features])
                append_to_log(df_single, log_csv,output_csv)
                print(f"✅ Appended {filename} to log.")

                 # Move processed MIDI to InactiveMIDIs
                new_path = os.path.join(inactive_folder, filename)
                os.rename(midi_path, new_path)
                print(f"🗂️  Moved {filename} to InactiveMIDIs.\n")

    print(f"Finished processing {len(records)} MIDI files.")
    df_all = pd.DataFrame(records)
    df_all.to_csv(output_csv, index=False, float_format="%.4f")

    with open("mood_feature_map.json", "w") as f:
         json.dump(mood_feature_map, f, indent=2)
         print("Exported mood_feature_map.json")

if __name__ == "__main__":
    main("MusicGroovesMIDI/TrainingMIDIs", "current_groove_features.csv", "groove_features_log.csv")
