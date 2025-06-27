# extract_groove_features.py
import os
import pretty_midi
import pandas as pd
import numpy as np
import datetime
import scipy.stats
import json

# Step 1: Define mood-to-feature mapping
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

# Step 2: Define numeric mappings
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

def extract_features(midi_path):
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
        swing = np.mean(np.abs(np.array(note_starts) - np.round(np.array(note_starts) * 2) / 2))

        timeline.sort()
        polyphony_counts = []
        active_notes = 0
        for _, event in timeline:
            active_notes += event
            polyphony_counts.append(active_notes)

        iois = np.diff(np.sort(note_starts))
        return {
            'tempo': tempo,
            'swing': swing,
            'density': density,
            'dynamic_range': np.max(velocities) - np.min(velocities),
            'energy': (density * 0.5) + (velocity_mean / 127 * 0.5),
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

    except Exception as e:
        print(f"Error processing {midi_path}: {e}")
        return None

def append_to_log(new_data: pd.DataFrame, log_csv: str):
    columns = [
        'tempo', 'swing', 'density', 'dynamic_range', 'energy',
        'mean_note_length', 'std_note_length', 'velocity_mean', 'velocity_std',
        'pitch_mean', 'pitch_range', 'avg_polyphony', 'syncopation',
        'onset_entropy', 'instrument_count',
        'mood', 'timing_feel', 'rhythmic_density', 'dynamic_intensity',
        'fill_activity', 'fx_character', 'timestamp'
    ]
    if os.path.exists(log_csv):
        old = pd.read_csv(log_csv)
        combined = pd.concat([old, new_data], ignore_index=True)
    else:
        combined = new_data
    combined[columns].to_csv(log_csv, index=False, float_format="%.4f")
    print(f"Appended to {log_csv}")

def main(midi_folder, output_csv, log_csv):
    records = []
    moods = list(mood_feature_map.keys())

    for filename in os.listdir(midi_folder):
        if filename.lower().endswith(('.mid', '.midi')):
            midi_path = os.path.join(midi_folder, filename)
            features = extract_features(midi_path)
            if features:
                print(f"\n{filename} summary:")
                for k, v in features.items():
                    print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

                while True:
                    mood = input(f"Choose mood ({'/'.join(moods)}): ").strip().lower()
                    if mood in mood_feature_map:
                        break

                features['mood'] = mood
                description = mood_feature_map[mood]
                features['timing_feel'] = timing_feel_map[description['timing_feel']]
                features['rhythmic_density'] = rhythmic_density_map[description['rhythmic_density']]
                features['dynamic_intensity'] = dynamic_intensity_map[description['dynamic_intensity']]
                features['fill_activity'] = fill_activity_map[description['fill_activity']]
                features['fx_character'] = fx_character_map[description['fx_character']]
                records.append(features)

    if records:
        df = pd.DataFrame(records)
        df.to_csv(output_csv, index=False, float_format="%.4f")
        append_to_log(df, log_csv)
        print(f"Saved {len(records)} grooves to {output_csv}")
    else:
        print("No grooves processed.")
    with open("mood_feature_map.json", "w") as f:
         json.dump(mood_feature_map, f, indent=2)
         print("Exported mood_feature_map.json")

if __name__ == "__main__":
    main("MusicGroovesMIDI/TrainingMIDIs", "current_groove_features.csv", "groove_features_log.csv")
