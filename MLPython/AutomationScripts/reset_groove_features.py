# reset_groove_features.py
import os
import pandas as pd

# Locate the log file
script_dir = os.path.dirname(os.path.abspath(__file__))
mlpython_dir = os.path.abspath(os.path.join(script_dir, ".."))
log_path = os.path.join(mlpython_dir, "groove_features_log.csv")

try:
    # Read the existing file to extract the column headers
    df = pd.read_csv(log_path)

    # Create a new empty DataFrame with just the headers
    df.iloc[0:0].to_csv(log_path, index=False)

    print("✅ groove_features_log.csv cleared (header preserved, data removed).")
except FileNotFoundError:
    print("❌ groove_features_log.csv not found.")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
