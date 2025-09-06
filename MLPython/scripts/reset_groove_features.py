#!/usr/bin/env python3
"""
Reset groove_features_log.csv by clearing it.
This is used to prevent duplicate data in training.
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))


def clear_log():
    """Clear the groove_features_log.csv file."""
    log_file = "data/csv/groove_features_log.csv"
    
    if os.path.exists(log_file):
        os.remove(log_file)
        print(f"🧹 Cleared {log_file}")
        return True
    else:
        print(f"⚠️ {log_file} not found")
        return False


def main():
    """Main entry point."""
    print("🧹 Resetting groove features log...")
    
    success = clear_log()
    
    if success:
        print("✅ Log reset completed successfully!")
    else:
        print("❌ Log reset failed")
        sys.exit(1)


if __name__ == "__main__":
    main()
