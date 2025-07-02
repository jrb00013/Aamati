import os
from mido import MidiFile, MidiTrack, MetaMessage

def fix_midi_format(midi_path, output_path):
    try:
        midi = MidiFile(midi_path)
        original_track0 = midi.tracks[0]
        meta_messages = []

        # Collect meta messages from all tracks
        for track in midi.tracks:
            for msg in track:
                if msg.is_meta and msg.type in ['set_tempo', 'key_signature', 'time_signature']:
                    meta_messages.append(msg)

        # Remove those messages from all tracks
        for track in midi.tracks:
            track[:] = [msg for msg in track if not (msg.is_meta and msg.type in ['set_tempo', 'key_signature', 'time_signature'])]

        # Add cleaned meta messages to new track 0
        new_track0 = MidiTrack()
        new_track0.extend(meta_messages)
        new_track0.extend(original_track0)

        midi.tracks[0] = new_track0
        midi.save(output_path)
        print(f"✅ Fixed: {os.path.basename(midi_path)} ➜ {output_path}")
    except Exception as e:
        print(f"❌ Error fixing {midi_path}: {e}")

def fix_all_midis(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.mid', '.midi')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            fix_midi_format(input_path, output_path)

if __name__ == "__main__":
    input_dir = "MusicGroovesMIDI/TrainingMIDIs"   
    output_dir = "MusicGroovesMIDI/FixedMIDIs"     
    fix_all_midis(input_dir, output_dir)
