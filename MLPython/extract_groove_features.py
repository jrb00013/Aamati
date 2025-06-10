#extract_groove_features.py
import os
import pretty_midi
import pandas as pd
import numpy as np

def extract_features(midi_path):
    try:
        pm = pretty_midi.PrettyMIDI(midi_path)

        # Basic groove features
        tempo = np.mean(pm.get_tempo_changes()[1]) if pm.get_tempo_changes()[1].size > 0 else 120

        note_times = []
        velocities = []

        for instrument in pm.instruments:
            if not instrument.is_drum:  # You can set to only drums if needed
                continue
            for note in instrument.notes:
                note_times.append(note.start)
                velocities.append(note.velocity)

        if len(note_times) < 2:
            return None  # skip empty grooves

        # Calculate density: notes per second
        duration = pm.get_end_time()
        density = len(note_times) / duration if duration > 0 else 0

        # Calculate swing: average timing deviation from strict grid
        quantized_times = np.round(np.array(note_times) * 2) / 2  # 8th note grid
        swing = np.mean(np.abs(np.array(note_times) - quantized_times))

        # Dynamic range: max - min velocity
        dynamic_range = np.max(velocities) - np.min(velocities) if velocities else 0

        # Energy: weighted sum of density and mean velocity
        mean_velocity = np.mean(velocities) if velocities else 0
        energy = (density * 0.5) + (mean_velocity / 127 * 0.5)

        return {
            'tempo': tempo,
            'swing': swing,
            'density': density,
            'dynamic_range': dynamic_range,
            'energy': energy
        }
    except Exception as e:
        print(f"Error processing {midi_path}: {e}")
        return None

def append_to_log(temp_csv, log_csv):
    # Read the temporary CSV with new records
    temp_df = pd.read_csv(temp_csv)
    
    # Check if the log CSV exists
    if os.path.exists(log_csv):
        # Read existing log
        log_df = pd.read_csv(log_csv)
        # Append new records
        combined_df = pd.concat([log_df, temp_df], ignore_index=True)
    else:
        # No log exists yet, so new temp CSV becomes the log
        combined_df = temp_df
    
    # Save the updated log CSV
    combined_df.to_csv(log_csv, index=False)
    print(f"Appended {len(temp_df)} records to {log_csv}")

def main(midi_folder, output_csv, log_csv):
    records = []

    print(f"Looking for MIDI files in folder: {midi_folder}")
    print("Found files:", os.listdir(midi_folder))

    for filename in os.listdir(midi_folder):
        if filename.endswith('.mid') or filename.endswith('.midi'):
            print(f"Processing file {filename}...") 
            midi_path = os.path.join(midi_folder, filename)
            features = extract_features(midi_path)
            if features:
                # TEMPORARY: ask user for mood label for now
                print(f"Please label this groove: {filename}")
                mood = input("Mood (chill/tense/uplifting/dark/energetic/relaxed): ").strip()
                features['mood'] = mood
                records.append(features)
    print(f"Processed {len(records)} grooves successfully.")
    
    if not records:
        print("No valid grooves processed. Skipping CSV save and append.")
        return
    
    df = pd.DataFrame(records)
    df.to_csv(output_csv, index=False)
    print(f"Saved extracted features to {output_csv}")

    # Append to cumulative log
    append_to_log(output_csv, log_csv)

if __name__ == "__main__":

    midi_folder = "MusicGroovesMidi"  # <-- your folder with grooves
    output_csv = "groove_features.csv"  # temporary extraction file
    log_csv = "groove_features_log.csv"  # cumulative log file
    main(midi_folder, output_csv, log_csv)
