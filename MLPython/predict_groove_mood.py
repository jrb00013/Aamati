import os
import pretty_midi
import numpy as np
import joblib
import scipy.stats

# Load the trained model
model = joblib.load('groove_mood_model.pkl')

def extract_features(midi_path):
    try:
        pm = pretty_midi.PrettyMIDI(midi_path)
        tempo = np.mean(pm.get_tempo_changes()[1]) if pm.get_tempo_changes()[1].size > 0 else 120

        note_starts = []
        note_ends = []
        velocities = []
        pitches = []

        timeline = []

        for instrument in pm.instruments:
            for note in instrument.notes:
                note_starts.append(note.start)
                note_ends.append(note.end)
                velocities.append(note.velocity)
                pitches.append(note.pitch)
                timeline.append((note.start, +1))
                timeline.append((note.end, -1))

        if len(note_starts) < 2:
            print("Not enough note events in the MIDI to extract features.")
            return None

        note_lengths = np.array(note_ends) - np.array(note_starts)
        mean_note_length = np.mean(note_lengths)
        std_note_length = np.std(note_lengths)

        velocity_mean = np.mean(velocities)
        velocity_std = np.std(velocities)
        dynamic_range = np.max(velocities) - np.min(velocities)

        pitch_mean = np.mean(pitches)
        pitch_range = np.max(pitches) - np.min(pitches)

        duration = pm.get_end_time()
        density = len(note_starts) / duration if duration > 0 else 0

        quantized_times = np.round(np.array(note_starts) * 2) / 2
        swing = np.mean(np.abs(np.array(note_starts) - quantized_times))

        energy = (density * 0.5) + (velocity_mean / 127 * 0.5)

        timeline.sort()
        active_notes = 0
        polyphony_counts = []
        for _, event in timeline:
            active_notes += event
            polyphony_counts.append(active_notes)
        avg_polyphony = np.mean(polyphony_counts) if polyphony_counts else 0

        sorted_starts = np.sort(note_starts)
        iois = np.diff(sorted_starts)
        if len(iois) > 1:
            syncopation = np.var(iois)
            onset_entropy = scipy.stats.entropy(np.histogram(iois, bins=10)[0] + 1)
        else:
            syncopation = 0
            onset_entropy = 0

        instrument_count = len(pm.instruments)

        feature_vector = np.array([
            tempo,
            swing,
            density,
            dynamic_range,
            energy,
            mean_note_length,
            std_note_length,
            velocity_mean,
            velocity_std,
            pitch_mean,
            pitch_range,
            avg_polyphony,
            syncopation,
            onset_entropy,
            instrument_count
        ])

        return feature_vector

    except Exception as e:
        print(f"Error processing {midi_path}: {e}")
        return None

def predict_mood(midi_path):
    features = extract_features(midi_path)
    if features is None:
        print("Unable to extract features.")
        return

    features = features.reshape(1, -1)
    mood = model.predict(features)[0]
    print(f"The predicted mood for {os.path.basename(midi_path)} is: {mood}")

if __name__ == "__main__":
    drop_folder = "MusicGroovesMidi/InputMIDI"
    if not os.path.exists(drop_folder):
        print(f"Folder '{drop_folder}' does not exist.")
        exit(1)

    midi_files = [f for f in os.listdir(drop_folder) if f.lower().endswith(('.mid', '.midi'))]
    if not midi_files:
        print(f"No MIDI files found in '{drop_folder}'. Please drop a MIDI file there.")
        exit(1)

    midi_path = os.path.join(drop_folder, midi_files[0])
    print(f"Using MIDI file: {midi_path}")

    predict_mood(midi_path)
