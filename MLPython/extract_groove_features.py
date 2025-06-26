# extract_groove_features.py

import os
import pretty_midi
import pandas as pd
import numpy as np
import datetime
import scipy.stats

def extract_features(midi_path):
    try:
        pm = pretty_midi.PrettyMIDI(midi_path)
        tempo = np.mean(pm.get_tempo_changes()[1]) if pm.get_tempo_changes()[1].size > 0 else 120

        note_starts = []
        note_ends = []
        velocities = []
        pitches = []

        # Track polyphony (notes overlapping)
        timeline = []

        for instrument in pm.instruments:
            print(f"Instrument: name={instrument.name}, is_drum={instrument.is_drum}, program={instrument.program}")
            for note in instrument.notes:
                note_starts.append(note.start)
                note_ends.append(note.end)
                velocities.append(note.velocity)
                pitches.append(note.pitch)
                timeline.append((note.start, +1))  # note on event
                timeline.append((note.end, -1))    # note off event

        if len(note_starts) < 2:
            print(f"Not enough notes in {midi_path} for feature extraction.")
            return None

        # Note lengths
        note_lengths = np.array(note_ends) - np.array(note_starts)
        mean_note_length = np.mean(note_lengths)
        std_note_length = np.std(note_lengths)

        # Velocity stats
        velocity_mean = np.mean(velocities)
        velocity_std = np.std(velocities)
        dynamic_range = np.max(velocities) - np.min(velocities) if velocities else 0

        # Pitch stats
        pitch_mean = np.mean(pitches) if pitches else 0
        pitch_range = (np.max(pitches) - np.min(pitches)) if pitches else 0

        # Density
        duration = pm.get_end_time()
        density = len(note_starts) / duration if duration > 0 else 0

        # Swing (timing deviation from grid, 8th notes)
        quantized_times = np.round(np.array(note_starts) * 2) / 2
        swing = np.mean(np.abs(np.array(note_starts) - quantized_times))

        # Energy (combined metric)
        energy = (density * 0.5) + (velocity_mean / 127 * 0.5)

        # Polyphony calculation
        timeline.sort()
        active_notes = 0
        polyphony_counts = []
        for _, event in timeline:
            active_notes += event
            polyphony_counts.append(active_notes)
        avg_polyphony = np.mean(polyphony_counts) if polyphony_counts else 0

        # Inter-onset intervals (IOIs)
        sorted_starts = np.sort(note_starts)
        iois = np.diff(sorted_starts)
        if len(iois) > 1:
            syncopation = np.var(iois)
            onset_entropy = scipy.stats.entropy(np.histogram(iois, bins=10)[0] + 1)  # add 1 to avoid zero counts
        else:
            syncopation = 0
            onset_entropy = 0

        # Instrument count
        instrument_count = len(pm.instruments)

        return {
            'tempo': tempo,
            'swing': swing,
            'density': density,
            'dynamic_range': dynamic_range,
            'energy': energy,
            'mean_note_length': mean_note_length,
            'std_note_length': std_note_length,
            'velocity_mean': velocity_mean,
            'velocity_std': velocity_std,
            'pitch_mean': pitch_mean,
            'pitch_range': pitch_range,
            'avg_polyphony': avg_polyphony,
            'syncopation': syncopation,
            'onset_entropy': onset_entropy,
            'instrument_count': instrument_count,
            'timestamp': datetime.datetime.now().isoformat()
        }

    except Exception as e:
        print(f"Error processing {midi_path}: {e}")
        return None

def append_to_log(new_data: pd.DataFrame, log_csv: str):
    column_order = [
        'tempo', 'swing', 'density', 'dynamic_range', 'energy',
        'mean_note_length', 'std_note_length', 'velocity_mean', 'velocity_std',
        'pitch_mean', 'pitch_range', 'avg_polyphony', 'syncopation',
        'onset_entropy', 'instrument_count',
        'mood', 'timestamp'
    ]

    if os.path.exists(log_csv):
        log_df = pd.read_csv(log_csv)
        combined_df = pd.concat([log_df, new_data], ignore_index=True)
    else:
        combined_df = new_data

    combined_df = combined_df[column_order]
    combined_df.to_csv(log_csv, index=False, float_format="%.4f")
    print(f"Appended {len(new_data)} records to {log_csv}")

def main(midi_folder, output_csv, log_csv):
    records = []
    print(f"Looking for MIDI files in folder: {midi_folder}")
    print("Found files:", os.listdir(midi_folder))

    for filename in os.listdir(midi_folder):
        if filename.lower().endswith(('.mid', '.midi')):
            print(f"Processing file {filename}...")
            midi_path = os.path.join(midi_folder, filename)
            features = extract_features(midi_path)
            if features:
                print(f"Please label this groove: {filename}")
                mood = input("Mood (chill/tense/uplifting/dark/energetic/relaxed): ").strip()
                features['mood'] = mood
                records.append(features)

    print(f"Processed {len(records)} grooves successfully.")

    if not records:
        print("No valid grooves processed. Skipping save.")
        return

    df = pd.DataFrame(records)
    column_order = [
        'tempo', 'swing', 'density', 'dynamic_range', 'energy',
        'mean_note_length', 'std_note_length', 'velocity_mean', 'velocity_std',
        'pitch_mean', 'pitch_range', 'avg_polyphony', 'syncopation',
        'onset_entropy', 'instrument_count',
        'mood', 'timestamp'
    ]
    df = df[column_order]

    df.to_csv(output_csv, index=False, float_format="%.4f")
    print(f"Saved last batch to {output_csv}")

    append_to_log(df, log_csv)

if __name__ == "__main__":
    midi_folder = "MusicGroovesMIDI/TrainingMIDIs"
    output_csv = "current_groove_features.csv"
    log_csv = "groove_features_log.csv"
    main(midi_folder, output_csv, log_csv)
