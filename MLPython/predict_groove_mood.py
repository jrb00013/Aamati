#predict_groove_mood.py
import pretty_midi
import pandas as pd
import numpy as np
import joblib  # To load the model

# Load the trained model (assuming it's in the current directory)
model = joblib.load('groove_mood_model.pkl')

def extract_features(midi_path):
    try:
        pm = pretty_midi.PrettyMIDI(midi_path)

        # Basic groove features
        tempo = np.mean(pm.get_tempo_changes()[1]) if pm.get_tempo_changes()[1].size > 0 else 120

        note_times = []
        velocities = []

        for instrument in pm.instruments:
            if not instrument.is_drum:  # Only focus on drum tracks
                continue
            for note in instrument.notes:
                note_times.append(note.start)
                velocities.append(note.velocity)

        if len(note_times) < 2:
            return None  # Skip empty grooves

        # Calculate groove features
        duration = pm.get_end_time()
        density = len(note_times) / duration if duration > 0 else 0
        quantized_times = np.round(np.array(note_times) * 2) / 2  # 8th note grid
        swing = np.mean(np.abs(np.array(note_times) - quantized_times))
        dynamic_range = np.max(velocities) - np.min(velocities) if velocities else 0
        mean_velocity = np.mean(velocities) if velocities else 0
        energy = (density * 0.5) + (mean_velocity / 127 * 0.5)

        return np.array([tempo, swing, density, dynamic_range, energy])
    except Exception as e:
        print(f"Error processing {midi_path}: {e}")
        return None

def predict_mood(midi_path):
    # Extract features from the MIDI file
    features = extract_features(midi_path)
    if features is None:
        print("Unable to extract features.")
        return

    # Reshape for the model (it expects a 2D array, even for a single sample)
    features = features.reshape(1, -1)

    # Make prediction
    mood = model.predict(features)[0]  # Get the predicted mood (it returns a list)
    print(f"The predicted mood for {midi_path} is: {mood}")

if __name__ == "__main__":
    midi_path = input("Enter the path to the MIDI file you want to classify: ").strip()
    predict_mood(midi_path)
