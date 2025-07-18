# copy_groove_features.py
import os
import pandas as pd

# Set up paths
script_dir = os.path.dirname(os.path.abspath(__file__))
mlpython_dir = os.path.abspath(os.path.join(script_dir, ".."))

source_file = os.path.join(mlpython_dir, "groove_features_log.csv")
dest_file = os.path.join(mlpython_dir, "groove_features_log_for_pred.csv")

# Load source
try:
    df_src = pd.read_csv(source_file)
except FileNotFoundError:
    print("❌ Source file not found.")
    exit(1)

# Columns to use for comparison (exclude timestamp)
comparison_cols = [col for col in df_src.columns if col != "timestamp"]

# If prediction file doesn't exist, copy all
if not os.path.exists(dest_file):
    df_src.to_csv(dest_file, index=False)
    print(f"✅ Created groove_features_log_for_pred.csv with all {len(df_src)} entries.")
else:
    df_dest = pd.read_csv(dest_file)
    existing_rows = df_dest[comparison_cols]

    # Find rows in source that are NOT in destination
    merged = df_src.merge(existing_rows.drop_duplicates(), on=comparison_cols, how='left', indicator=True)
    new_rows = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    if not new_rows.empty:
        new_rows.to_csv(dest_file, mode='a', index=False, header=False)
        print(f"✅ Appended {len(new_rows)} new row(s) to groove_features_log_for_pred.csv.")
    else:
        print("ℹ️ No new rows to append — all entries already exist.")
