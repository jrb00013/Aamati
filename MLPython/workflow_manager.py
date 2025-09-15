#!/usr/bin/env python3
"""
Workflow Manager for Aamati ML Pipeline
Handles the complete workflow: extract -> classify -> copy -> clear -> retrain
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command with error handling."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"Output: {result.stdout}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error in {description}: {e}")
        return False

def copy_log_to_pred():
    """Copy groove_features_log.csv to groove_features_log_for_pred.csv"""
    log_file = "data/csv/groove_features_log.csv"
    pred_file = "data/csv/groove_features_log_for_pred.csv"
    
    if os.path.exists(log_file):
        shutil.copy2(log_file, pred_file)
        print(f"✅ Copied {log_file} to {pred_file}")
        return True
    else:
        print(f"⚠️ {log_file} not found")
        return False

def clear_log():
    """Clear the groove_features_log.csv file"""
    log_file = "data/csv/groove_features_log.csv"
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🧹 Cleared {log_file}")
        return True
    else:
        print(f"⚠️ {log_file} not found")
        return False

def check_duplicates():
    """Check for duplicate MIDI files"""
    print("🔍 Checking for duplicate MIDI files...")
    return run_command("python3 AutomationScripts/filter_new_midis.py", "Duplicate check")

def format_midis():
    """Format MIDI files for compliance"""
    print("🔧 Formatting MIDI files...")
    return run_command("python3 fixed_midi_compliance.py", "MIDI formatting")

def extract_features(interactive=True, max_files=None):
    """Extract features from MIDI files"""
    cmd = "python3 extract_groove_features.py"
    if not interactive:
        cmd += " --non-interactive"
    if max_files:
        cmd += f" --max-files {max_files}"
    
    return run_command(cmd, "Feature extraction")

def train_models():
    """Train all models"""
    return run_command("python3 train_models.py", "Model training")

def workflow_step1_classify_existing():
    """Step 1: Classify moods for existing 500 samples (no retraining)"""
    print("\n🎯 STEP 1: Classify moods for existing samples")
    print("=" * 60)
    
    # Just copy existing data to prediction file
    if copy_log_to_pred():
        print("✅ Existing samples copied to prediction file")
        print("📝 You can now manually classify moods in the CSV if needed")
        return True
    return False

def workflow_step2_add_new_midis():
    """Step 2: Add new MIDI files and process them"""
    print("\n🎵 STEP 2: Add new MIDI files")
    print("=" * 60)
    
    # Check for duplicates
    if not check_duplicates():
        print("⚠️ Duplicate check failed, continuing...")
    
    # Format MIDI files
    if not format_midis():
        print("⚠️ MIDI formatting failed, continuing...")
    
    # Extract features (interactive mode for mood classification)
    if extract_features(interactive=True):
        print("✅ New MIDI files processed")
        return True
    return False

def workflow_step3_retrain_models():
    """Step 3: Retrain models with new data"""
    print("\n🤖 STEP 3: Retrain models")
    print("=" * 60)
    
    # Copy current log to prediction file
    if not copy_log_to_pred():
        print("❌ Failed to copy log to prediction file")
        return False
    
    # Clear log for next batch
    if not clear_log():
        print("❌ Failed to clear log file")
        return False
    
    # Train models
    if train_models():
        print("✅ Models retrained successfully")
        return True
    return False

def workflow_full_cycle():
    """Complete workflow cycle"""
    print("\n🚀 FULL WORKFLOW CYCLE")
    print("=" * 60)
    
    # Step 1: Process existing samples
    if not workflow_step1_classify_existing():
        print("❌ Step 1 failed")
        return False
    
    # Step 2: Add new MIDI files
    if not workflow_step2_add_new_midis():
        print("❌ Step 2 failed")
        return False
    
    # Step 3: Retrain models
    if not workflow_step3_retrain_models():
        print("❌ Step 3 failed")
        return False
    
    print("\n🎉 Full workflow cycle completed successfully!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Aamati Workflow Manager")
    parser.add_argument("--step", choices=[
        "classify-existing", "add-new", "retrain", "full-cycle"
    ], required=True, help="Workflow step to execute")
    parser.add_argument("--interactive", action="store_true", default=True,
                       help="Run in interactive mode")
    parser.add_argument("--max-files", type=int, default=None,
                       help="Maximum number of files to process")
    
    args = parser.parse_args()
    
    print("🎵 Aamati Workflow Manager")
    print("=" * 50)
    
    success = False
    
    if args.step == "classify-existing":
        success = workflow_step1_classify_existing()
    elif args.step == "add-new":
        success = workflow_step2_add_new_midis()
    elif args.step == "retrain":
        success = workflow_step3_retrain_models()
    elif args.step == "full-cycle":
        success = workflow_full_cycle()
    
    if success:
        print("\n✅ Workflow step completed successfully!")
    else:
        print("\n❌ Workflow step failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
