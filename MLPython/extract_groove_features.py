#!/usr/bin/env python3
"""
Main feature extraction script for Aamati ML system.
This is the primary script for extracting groove features from MIDI files.
"""

import os
import sys
import argparse
import shutil
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.extract_groove_features import main as extract_main


def copy_log_to_pred():
    """Copy groove_features_log.csv to groove_features_log_for_pred.csv before clearing."""
    log_file = "groove_features_log.csv"
    pred_file = "groove_features_log_for_pred.csv"
    
    if os.path.exists(log_file):
        shutil.copy2(log_file, pred_file)
        print(f"✅ Copied {log_file} to {pred_file}")
    else:
        print(f"⚠️ {log_file} not found, creating empty {pred_file}")
        Path(pred_file).touch()


def clear_log():
    """Clear the groove_features_log.csv file."""
    log_file = "groove_features_log.csv"
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🧹 Cleared {log_file}")
    else:
        print(f"⚠️ {log_file} not found")


def main():
    """Main entry point for feature extraction."""
    parser = argparse.ArgumentParser(description="Aamati Main Feature Extraction")
    parser.add_argument("--midi-folder", default="MusicGroovesMIDI/TrainingMIDIs",
                       help="Path to MIDI training folder")
    parser.add_argument("--output-csv", default="current_groove_features.csv",
                       help="Output CSV file")
    parser.add_argument("--log-csv", default="groove_features_log.csv",
                       help="Log CSV file")
    parser.add_argument("--pred-csv", default="groove_features_log_for_pred.csv",
                       help="Prediction CSV file")
    parser.add_argument("--interactive", action="store_true", default=True,
                       help="Run in interactive mode")
    parser.add_argument("--non-interactive", action="store_true",
                       help="Run in non-interactive mode")
    parser.add_argument("--clear-log", action="store_true",
                       help="Clear log file before starting")
    parser.add_argument("--copy-to-pred", action="store_true",
                       help="Copy log to pred file after extraction")
    
    args = parser.parse_args()
    
    print("🎵 Aamati Main Feature Extraction")
    print("=" * 50)
    
    # Determine interactive mode
    interactive = args.interactive and not args.non_interactive
    
    # Copy log to pred before clearing (if requested)
    if args.clear_log:
        copy_log_to_pred()
        clear_log()
    
    # Run the main extraction
    print(f"📊 Extracting features from: {args.midi_folder}")
    print(f"📝 Interactive mode: {interactive}")
    
    try:
        extract_main(args.midi_folder, args.output_csv, args.log_csv)
        print("✅ Feature extraction completed successfully!")
        
        # Copy log to pred after extraction (if requested)
        if args.copy_to_pred:
            copy_log_to_pred()
            clear_log()
            print("✅ Data copied to prediction file and log cleared")
            
    except Exception as e:
        print(f"❌ Feature extraction failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()