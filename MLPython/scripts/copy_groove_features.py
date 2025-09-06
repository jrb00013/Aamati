#!/usr/bin/env python3
"""
Copy groove_features_log.csv to groove_features_log_for_pred.csv
This ensures we preserve the training data before clearing the log.
"""

import os
import shutil
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))


def copy_log_to_pred():
    """Copy groove_features_log.csv to groove_features_log_for_pred.csv."""
    log_file = "data/csv/groove_features_log.csv"
    pred_file = "data/csv/groove_features_log_for_pred.csv"
    
    # Ensure directories exist
    os.makedirs("data/csv", exist_ok=True)
    
    if os.path.exists(log_file):
        shutil.copy2(log_file, pred_file)
        print(f"✅ Copied {log_file} to {pred_file}")
        return True
    else:
        print(f"⚠️ {log_file} not found")
        return False


def main():
    """Main entry point."""
    print("📋 Copying groove features log to prediction file...")
    
    success = copy_log_to_pred()
    
    if success:
        print("✅ Data copying completed successfully!")
    else:
        print("❌ Data copying failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
