# predict_groove_model.py
import os
import pretty_midi
import numpy as np
import joblib
import scipy.stats
import json
import pandas as pd

# === Load trained model, encoder, mood map ===
model = joblib.load('groove_mood_model.pkl')
encoder = joblib.load('categorical_encoder.pkl')
with open('mood_feature_map.json', 'r') as f:
    mood_map = json.load(f)

# === Category mappings from extract_groove_features.py ===
timing_feel_map = {'tight': 0, 'mid': 1, 'loose': 2, 'random': 3}
rhythmic_density_map = {'low': 0, 'medium': 1, 'high': 2, 'very_high': 3}
dynamic_intensity_map = {
    'soft': 0, 'gentle': 1, 'light': 2, 'bright': 3, 'deep': 4,
    'varied': 5, 'consistent': 6, 'hard': 7, 'harsh': 8, 'wild': 9
}
fill_activity_map = {
    'sparse': 0, 'minimal': 1, 'occasional': 2, 'moderate': 3,
    'medium': 4, 'frequent': 5, 'bursty': 6, 'irregular': 7
}
fx_character_map = {
    'wet, wide, airy': 0, 'dry, punchy, sharp': 1, 'dark, modulated, narrow': 2,
    'shimmery, wide, echoing': 3, 'saturated, low-end heavy': 4, 'warm, lush, resonant': 5,
    'distorted, mono, rough': 6, 'reverb-heavy, washed-out': 7, 'glitchy, stuttered, noisy': 8,
    'clean, subtle, precise': 9
}

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

def estimate_swing(note_starts):
    MIN_NOTES = 8
    TOLERANCE = 0.005
    sorted_starts = np.sort(note_starts)
    iois = np.diff(sorted_starts)
    if len(iois) < MIN_NOTES or np.std(iois) < TOLERANCE:
        return 0.0
    odd_iois = iois[0::2]
    even_iois = iois[1::2]
    if len(odd_iois) < 2 or len(even_iois) < 2 or np.mean(even_iois) == 0:
        return 0.0
    swing_ratio = np.mean(odd_iois) / np.mean(even_iois)
    return round(min(abs(swing_ratio - 1.0), 1.0), 4)

def extract_all_features(midi_path):
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
        duration = pm.get_end_time()
        velocity_mean = np.mean(velocities)
        velocities_np = np.array(velocities)

        dynamic_range = np.max(velocities_np) - np.min(velocities_np)
        if dynamic_range < 1e-3:
          dynamic_range = np.std(velocities_np)

        density = len(note_starts) / duration if duration > 0 else 0
        swing = estimate_swing(note_starts)
        pitch_range = np.max(pitches) - np.min(pitches)
        iois = np.diff(np.sort(note_starts))
        onset_entropy = scipy.stats.entropy(np.histogram(iois, bins=10)[0] + 1) if len(iois) > 1 else 0
        syncopation = np.var(iois) if len(iois) > 1 else 0

        timeline.sort()
        active_notes = 0
        polyphony_counts = []
        for _, event in timeline:
            active_notes += event
            polyphony_counts.append(active_notes)
        avg_polyphony = np.mean(polyphony_counts)

        energy = 0.4581 * density + 0.0372 * velocity_mean + 0.0154 * dynamic_range + 0.1026 * avg_polyphony + 0.7832

        # === Generate CATEGORICAL FEATURES using same logic ===
        if swing > 0.1 and syncopation > 0.02:
            timing_feel_score = 2  # loose
        elif swing < 0.03 and syncopation < 0.01:
            timing_feel_score = 0  # tight
        elif syncopation > 0.05 and onset_entropy > 2.0:
            timing_feel_score = 3  # random
        else:
            timing_feel_score = 1  # mid

        if density < 2:
            rhythmic_density_score = 0
        elif density < 5:
            rhythmic_density_score = 1
        elif density < 10:
            rhythmic_density_score = 2
        else:
            rhythmic_density_score = 3

        if pitch_range < 5 and onset_entropy < 1.2:
            fill_activity_score = 0
        elif pitch_range < 10 and onset_entropy < 1.5:
            fill_activity_score = 1
        elif pitch_range < 15 and onset_entropy < 1.8:
            fill_activity_score = 2
        elif pitch_range < 20 and onset_entropy < 2.1:
            fill_activity_score = 3
        elif pitch_range < 25 and onset_entropy < 2.4:
            fill_activity_score = 4
        elif pitch_range < 30 and onset_entropy < 2.7:
            fill_activity_score = 5
        elif pitch_range <= 35 or onset_entropy <= 3.0:
            fill_activity_score = 6
        else:
            fill_activity_score = 7

        # Default fallback fx_character for prediction (or build a predictor later)
        fx_character_score = 0

        # Conservative default for now:
        dynamic_intensity_score = 5  # varied

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
            'pitch_range': pitch_range,
            'avg_polyphony': avg_polyphony,
            'syncopation': syncopation,
            'onset_entropy': onset_entropy,
            'instrument_count': len(pm.instruments),
            'timing_feel': timing_feel_score,
            'rhythmic_density': rhythmic_density_score,
            'dynamic_intensity': dynamic_intensity_score,
            'fill_activity': fill_activity_score,
            'fx_character': fx_character_score
        }
        return features
    except Exception as e:
        print(f"Error processing {midi_path}: {e}")
        return None

def predict_mood(midi_path):
    features = extract_all_features(midi_path)
    if features is None:
        print("Could not extract features.")
        return

    # Ensure consistent order
    df = pd.DataFrame([features], columns=categorical_features_order + numerical_features_order)

    # Encode categorical features
    X_cat = df[categorical_features_order]
    X_cat_encoded = encoder.transform(X_cat)

    X_num = df[numerical_features_order].values
    X_input = np.hstack([X_cat_encoded, X_num])

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
    print(f"Predicting mood for: {midi_path}")
    predict_mood(midi_path)
