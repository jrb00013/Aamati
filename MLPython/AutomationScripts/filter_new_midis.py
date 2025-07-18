import os
import shutil

# Define paths relative to AutomationScripts/
script_path = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.abspath(os.path.join(script_path, ".."))  # Go up to MLPython/
music_midi_path = os.path.join(base_path, "MusicGroovesMIDI")

new_midis_path = os.path.join(music_midi_path, "NewMIDIs")
processed_midis_path = os.path.join(music_midi_path, "ProcessedMIDIs")
training_midis_path = os.path.join(music_midi_path, "TrainingMIDIs")

# Get processed MIDI filenames
processed_files = {f for f in os.listdir(processed_midis_path) if f.lower().endswith(('.mid', '.midi'))}

# Create target folder if it doesn't exist
os.makedirs(training_midis_path, exist_ok=True)

# Check and move new files
moved_files = 0
for file in os.listdir(new_midis_path):
    if file.lower().endswith(('.mid', '.midi')):
        if file not in processed_files:
            src = os.path.join(new_midis_path, file)
            dst = os.path.join(training_midis_path, file)
            shutil.move(src, dst)
            moved_files += 1

print(f"Moved {moved_files} new MIDI files to TrainingMIDIs.")

if moved_files == 0:
        print("No new MIDI files.")