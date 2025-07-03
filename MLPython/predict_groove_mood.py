# predict_groove_model.py

import os
import joblib
import json
import pandas as pd
import numpy as np

from extract_groove_features import extract_full_feature_vector 

# === Load trained mood model and encoder ===
model = joblib.load("groove_mood_model.pkl")
encoder = joblib.load("categorical_encoder.pkl")

with open("mood_feature_map.json", "r") as f:
    mood_map = json.load(f)

categorical_features_order = [
    'timing_feel', 'rhythmic_density', 'dynamic_intensity',
    'fill_activity', 'fx_character'
]

numerical_features_order = [
    'tempo', 'swing', 'density', 'dynamic_range', 'energy',
    'mean_note_length', 'std_note_length', 'velocity_mean', 'velocity_std',
    'pitch_mean', 'pitch_range', 'avg_polyphony', 'syncopation',
    'onset_entropy', 'instrument_count'
]

def predict_mood(midi_path):
    features = extract_full_feature_vector(midi_path)
    if features is None:
        print("❌ Failed to extract features.")
        return

    df = pd.DataFrame([features], columns=categorical_features_order + numerical_features_order)

    X_cat = df[categorical_features_order]
    X_cat_encoded = encoder.transform(X_cat)

    X_num = df[numerical_features_order].values
    X_input = np.hstack([X_cat_encoded, X_num])

    prediction = model.predict(X_input)[0]
    print(f"\n🎵 Predicted Mood: {prediction}")
    print("📝 Mood Description:", mood_map.get(prediction, "No description available."))

if __name__ == "__main__":
    drop_folder = "MusicGroovesMidi/InputMIDI"
    midi_files = [f for f in os.listdir(drop_folder) if f.lower().endswith(('.mid', '.midi'))]
    if not midi_files:
        print("No MIDI files found in:", drop_folder)
        exit(1)

    midi_path = os.path.join(drop_folder, midi_files[0])
    print(f"Analyzing: {midi_path}")
    predict_mood(midi_path)
