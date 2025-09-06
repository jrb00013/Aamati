"""
Main training pipeline for the Aamati ML system.
"""

import os
import sys
import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.core.feature_extractor import FeatureExtractor
from src.utils.mood_mappings import MOOD_FEATURE_MAP


class TrainingPipeline:
    """Main training pipeline for mood classification."""
    
    def __init__(self, 
                 midi_folder: str = "MusicGroovesMIDI/TrainingMIDIs",
                 output_csv: str = "current_groove_features.csv",
                 log_csv: str = "groove_features_log.csv",
                 models_dir: str = "models"):
        """Initialize training pipeline."""
        self.midi_folder = midi_folder
        self.output_csv = output_csv
        self.log_csv = log_csv
        self.models_dir = models_dir
        self.feature_extractor = FeatureExtractor(models_dir)
        self.moods = list(MOOD_FEATURE_MAP.keys())
        
    def process_midi_files(self, interactive: bool = True) -> List[Dict]:
        """Process all MIDI files in the training folder."""
        records = []
        inactive_folder = os.path.join(os.path.dirname(self.midi_folder), "ProcessedMIDIs")
        os.makedirs(inactive_folder, exist_ok=True)

        midi_files = [f for f in os.listdir(self.midi_folder) 
                     if f.lower().endswith(('.mid', '.midi'))]
        
        if not midi_files:
            print("⚠️ No MIDI files found in training folder")
            return records
            
        print(f"🎵 Found {len(midi_files)} MIDI files to process")
        
        for i, filename in enumerate(midi_files, 1):
            print(f"\n📁 Processing {i}/{len(midi_files)}: {filename}")
            midi_path = os.path.join(self.midi_folder, filename)
            
            features = self.feature_extractor.extract_features(midi_path)
            if features is None:
                print(f"❌ Failed to extract features from {filename}")
                continue
                
            print(f"✅ Extracted features from {filename}")
            self._print_feature_summary(features)
            
            if interactive:
                primary_mood, secondary_mood = self._get_user_mood_input()
            else:
                # Auto-assign based on feature analysis
                primary_mood, secondary_mood = self._auto_assign_mood(features)
                
            features['primary_mood'] = primary_mood
            features['secondary_mood'] = secondary_mood
            features['midi_file_name'] = filename
            
            records.append(features)
            
            # Save individual record
            df_single = pd.DataFrame([features])
            self.feature_extractor.append_to_log(df_single, self.log_csv, self.output_csv)
            print(f"💾 Saved features for {filename}")
            
            # Move processed MIDI
            new_path = os.path.join(inactive_folder, filename)
            os.rename(midi_path, new_path)
            print(f"📦 Moved {filename} to ProcessedMIDIs")
            
        return records
    
    def _print_feature_summary(self, features: Dict):
        """Print a summary of extracted features."""
        print("📊 Feature Summary:")
        for key, value in features.items():
            if isinstance(value, float):
                print(f"  {key}: {value:.4f}")
            else:
                print(f"  {key}: {value}")
    
    def _get_user_mood_input(self) -> tuple:
        """Get mood input from user."""
        while True:
            primary_mood = input(f"🎯 Choose primary mood ({'/'.join(self.moods)}): ").strip().lower()
            if primary_mood in self.moods:
                break
            print("⚠️ Invalid mood, please try again")
            
        while True:
            secondary_mood = input(f"🎨 Choose secondary mood ({'/'.join(self.moods)}), or press Enter: ").strip().lower()
            if not secondary_mood or secondary_mood in self.moods:
                break
            print("⚠️ Invalid mood, please try again")
            
        return primary_mood, secondary_mood or primary_mood
    
    def _auto_assign_mood(self, features: Dict) -> tuple:
        """Auto-assign mood based on feature analysis."""
        # Simple heuristic-based mood assignment
        tempo = features.get('tempo', 120)
        density = features.get('density', 0)
        energy = features.get('energy', 0)
        dynamic_range = features.get('dynamic_range', 0)
        
        if tempo < 80 and density < 10:
            mood = "chill"
        elif tempo > 150 and density > 20:
            mood = "energetic"
        elif tempo > 200:
            mood = "frantic"
        elif energy > 12:
            mood = "gritty"
        elif dynamic_range < 30:
            mood = "dreamy"
        else:
            mood = "focused"
            
        return mood, mood
    
    def save_results(self, records: List[Dict]):
        """Save all processed records."""
        if not records:
            print("⚠️ No records to save")
            return
            
        df_all = pd.DataFrame(records)
        df_all.to_csv(self.output_csv, index=False, float_format="%.4f")
        print(f"💾 Saved {len(records)} records to {self.output_csv}")
        
        # Export mood feature map
        import json
        with open("mood_feature_map.json", "w") as f:
            json.dump(MOOD_FEATURE_MAP, f, indent=2)
        print("📋 Exported mood_feature_map.json")
    
    def run_training(self, interactive: bool = True):
        """Run the complete training pipeline."""
        print("🚀 Starting Aamati Training Pipeline")
        print("=" * 50)
        
        records = self.process_midi_files(interactive)
        
        if records:
            self.save_results(records)
            print(f"\n✅ Training completed! Processed {len(records)} files")
        else:
            print("\n❌ No files were processed")


def main():
    """Main entry point for training pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Aamati ML Training Pipeline")
    parser.add_argument("--midi-folder", default="MusicGroovesMIDI/TrainingMIDIs",
                       help="Path to MIDI training folder")
    parser.add_argument("--output-csv", default="current_groove_features.csv",
                       help="Output CSV file")
    parser.add_argument("--log-csv", default="groove_features_log.csv",
                       help="Log CSV file")
    parser.add_argument("--models-dir", default="models",
                       help="Models directory")
    parser.add_argument("--non-interactive", action="store_true",
                       help="Run in non-interactive mode (auto-assign moods)")
    
    args = parser.parse_args()
    
    pipeline = TrainingPipeline(
        midi_folder=args.midi_folder,
        output_csv=args.output_csv,
        log_csv=args.log_csv,
        models_dir=args.models_dir
    )
    
    pipeline.run_training(interactive=not args.non_interactive)


if __name__ == "__main__":
    main()
