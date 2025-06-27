# predict_groove_model.py
import os
import pretty_midi
import numpy as np
import joblib
import scipy.stats
import json
import pandas as pd

# Load trained model, encoder and mood map
model = joblib.load('groove_mood_model.pkl')
encoder = joblib.load('categorical_encoder.pkl')
with open('mood_feature_map.json', 'r') as f:
    mood_map = json.load(f)

numerical_features_order = [
    'tempo', 'swing', 'density', 'dynamic_range', 'energy',
    'mean_note_length', 'std_note_length', 'velocity_mean', 'velocity_std',
    'pitch_mean', 'pitch_range', 'avg_polyphony', 'syncopation',
    'onset_entropy', 'instrument_count'
]

categorical_features_order = [
    'timing_feel', 'rhythmic_density', 'dynamic_intensity',
    'fill_activity', 'fx_character'
]

def extract_numerical_features(midi_path):
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
            return None

        note_lengths = np.array(note_ends) - np.array(note_starts)
        feature_vector = {
            'tempo': tempo,
            'swing': np.mean(np.abs(np.array(note_starts) - np.round(np.array(note_starts) * 2) / 2)),
            'density': len(note_starts) / pm.get_end_time(),
            'dynamic_range': np.max(velocities) - np.min(velocities),
            'energy': (len(note_starts) / pm.get_end_time()) * 0.5 + (np.mean(velocities) / 127 * 0.5),
            'mean_note_length': np.mean(note_lengths),
            'std_note_length': np.std(note_lengths),
            'velocity_mean': np.mean(velocities),
            'velocity_std': np.std(velocities),
            'pitch_mean': np.mean(pitches),
            'pitch_range': np.max(pitches) - np.min(pitches),
            'avg_polyphony': np.mean([sum(e for _, e in sorted(timeline[:i+1])) for i in range(len(timeline))]),
            'syncopation': np.var(np.diff(np.sort(note_starts))) if len(note_starts) > 2 else 0,
            'onset_entropy': scipy.stats.entropy(np.histogram(np.diff(np.sort(note_starts)), bins=10)[0] + 1) if len(note_starts) > 2 else 0,
            'instrument_count': len(pm.instruments)
        }
        return feature_vector

    except Exception as e:
        print(f"Error extracting: {e}")
        return None

def predict_mood(midi_path):
    numerical_features = extract_numerical_features(midi_path)
    if numerical_features is None:
        print("Could not extract features.")
        return

    
    # For now, fallback to 'chill' or any default mood
    rough_mood = 'chill'  

    # Get categorical features from rough mood 
    categorical_features = mood_map.get(rough_mood)
    if categorical_features is None:
        print(f"No categorical features found for mood '{rough_mood}', using empty strings.")
        categorical_features = {k: "" for k in categorical_features_order}

    # Combine categorical + numerical features 
    combined_features = {}
    combined_features.update(categorical_features)
    combined_features.update(numerical_features)

    # Create DataFrame in the expected column order
    df = pd.DataFrame([combined_features], columns=categorical_features_order + numerical_features_order)

    # Encode categorical features 
    X_cat = df[categorical_features_order]
    X_cat_encoded = encoder.transform(X_cat)

    # Combine encoded categorical + numerical features 
    X_num = df[numerical_features_order].values
    X_input = np.hstack([X_cat_encoded, X_num])

    # Predict final mood 
    prediction = model.predict(X_input)[0]

    print(f"Final Predicted Mood: {prediction}")
    print("Mood Description:", mood_map.get(prediction, "No description available."))

if __name__ == "__main__":
    drop_folder = "MusicGroovesMidi/InputMIDI"
    midi_files = [f for f in os.listdir(drop_folder) if f.lower().endswith(('.mid', '.midi'))]
    if not midi_files:
        print("No MIDI files found in:", drop_folder)
        exit(1)

    midi_path = os.path.join(drop_folder, midi_files[0])
    print(f"Predicting mood for {midi_path}")
    predict_mood(midi_path)
