#!/usr/bin/env python3
"""
Main entry point for the Aamati ML system.
"""

import sys
import argparse
import subprocess
from pathlib import Path


def run_script(script_name, args=None):
    """Run a script with proper error handling."""
    if args is None:
        args = []
    
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)] + args,
            cwd=Path(__file__).parent
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running {script_name}: {e}")
        return False


def main():
    """Main entry point for ML system."""
    parser = argparse.ArgumentParser(description="Aamati ML System")
    parser.add_argument("--mode", choices=[
        "extract", "train", "predict", "copy-log", "clear-log", "full-pipeline", "automate"
    ], required=True, help="Operation mode")
    parser.add_argument("--workflow", choices=[
        "training", "prediction", "full"
    ], default="full", help="Workflow type for automate mode")
    parser.add_argument("--interactive", action="store_true", default=True,
                       help="Run in interactive mode")
    parser.add_argument("--non-interactive", action="store_true",
                       help="Run in non-interactive mode")
    parser.add_argument("--midi-folder", default="MusicGroovesMIDI/TrainingMIDIs",
                       help="Path to MIDI folder")
    parser.add_argument("--csv-file", default="data/csv/groove_features_log_for_pred.csv",
                       help="CSV file for prediction")
    
    args = parser.parse_args()
    
    print("🎵 Aamati ML System")
    print("=" * 50)
    
    # Determine interactive mode
    interactive = args.interactive and not args.non_interactive
    
    success = True
    
    if args.mode == "extract":
        # Run feature extraction
        print("📊 Running feature extraction...")
        extract_args = ["--interactive"] if interactive else ["--non-interactive"]
        extract_args.extend(["--midi-folder", args.midi_folder])
        success = run_script("extract_groove_features.py", extract_args)
        
    elif args.mode == "train":
        # Run model training
        print("🤖 Running model training...")
        success = run_script("train_models.py")
        
    elif args.mode == "predict":
        # Run predictions
        print("🔮 Running mood prediction...")
        success = run_script("predict_groove_mood.py", ["--csv-file", args.csv_file])
        
    elif args.mode == "copy-log":
        # Copy log to pred
        print("📋 Copying log to prediction file...")
        success = run_script("scripts/copy_groove_features.py")
        
    elif args.mode == "clear-log":
        # Clear log
        print("🧹 Clearing log file...")
        success = run_script("scripts/reset_groove_features.py")
        
    elif args.mode == "automate":
        # Run automated workflow based on workflow type
        print(f"🤖 Running automated workflow: {args.workflow}")
        
        if args.workflow == "training":
            # Training workflow: extract -> copy to pred -> clear log -> train
            print("📚 Training workflow...")
            
            # Step 1: Extract features
            print("1️⃣ Extracting features...")
            extract_args = ["--interactive"] if interactive else ["--non-interactive"]
            extract_args.extend(["--midi-folder", args.midi_folder])
            if not run_script("extract_groove_features.py", extract_args):
                success = False
            
            # Step 2: Copy log to pred
            if success:
                print("2️⃣ Copying log to prediction file...")
                if not run_script("scripts/copy_groove_features.py"):
                    print("⚠️ No existing log to copy, continuing...")
            
            # Step 3: Clear log
            if success:
                print("3️⃣ Clearing log file...")
                run_script("scripts/reset_groove_features.py")
            
            # Step 4: Train models
            if success:
                print("4️⃣ Training models...")
                if not run_script("train_models.py"):
                    success = False
        
        elif args.workflow == "prediction":
            # Prediction workflow: predict from existing data
            print("🔮 Prediction workflow...")
            print("1️⃣ Generating predictions...")
            if not run_script("predict_groove_mood.py", ["--csv-file", args.csv_file]):
                success = False
        
        elif args.workflow == "full":
            # Full workflow: complete pipeline
            print("🚀 Full workflow...")
            
            # Step 1: Copy existing log to pred
            print("1️⃣ Copying existing log to prediction file...")
            if not run_script("scripts/copy_groove_features.py"):
                print("⚠️ No existing log to copy, continuing...")
            
            # Step 2: Clear log
            print("2️⃣ Clearing log file...")
            run_script("scripts/reset_groove_features.py")
            
            # Step 3: Extract features
            print("3️⃣ Extracting features...")
            extract_args = ["--interactive"] if interactive else ["--non-interactive"]
            extract_args.extend(["--midi-folder", args.midi_folder, "--copy-to-pred"])
            if not run_script("extract_groove_features.py", extract_args):
                success = False
            
            # Step 4: Train models
            if success:
                print("4️⃣ Training models...")
                if not run_script("train_models.py"):
                    success = False
            
            # Step 5: Generate predictions
            if success:
                print("5️⃣ Generating predictions...")
                if not run_script("predict_groove_mood.py", ["--csv-file", args.csv_file]):
                    success = False
    
    elif args.mode == "full-pipeline":
        # Run complete pipeline
        print("🚀 Running full ML pipeline...")
        
        # Step 1: Copy existing log to pred
        print("1️⃣ Copying existing log to prediction file...")
        if not run_script("scripts/copy_groove_features.py"):
            print("⚠️ No existing log to copy, continuing...")
        
        # Step 2: Clear log
        print("2️⃣ Clearing log file...")
        run_script("scripts/reset_groove_features.py")
        
        # Step 3: Extract features
        print("3️⃣ Extracting features...")
        extract_args = ["--interactive"] if interactive else ["--non-interactive"]
        extract_args.extend(["--midi-folder", args.midi_folder, "--copy-to-pred"])
        if not run_script("extract_groove_features.py", extract_args):
            success = False
        
        # Step 4: Train models
        if success:
            print("4️⃣ Training models...")
            if not run_script("train_models.py"):
                success = False
        
        # Step 5: Generate predictions
        if success:
            print("5️⃣ Generating predictions...")
            if not run_script("predict_groove_mood.py", ["--csv-file", args.csv_file]):
                success = False
    
    if success:
        print("\n✅ Operation completed successfully!")
    else:
        print("\n❌ Operation failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
