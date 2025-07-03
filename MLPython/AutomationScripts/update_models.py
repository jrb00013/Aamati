import subprocess
import os

def run_script(script_name):
    print(f"Running {script_name} ...")
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors/warnings:")
        print(result.stderr)

if __name__ == "__main__":
    # Add more training scripts if needed
    scripts = [
        "../ModelClassificationScripts/dynamic_intensity_randomforest.py",
        "../ModelClassificationScripts/rhythmic_density_ordinal_regression.py",
        "../ModelClassificationScripts/fill_activity_randomforest.py",
        "../ModelClassificationScripts/fx_character_rfclassifier.py",
        "../ModelClassificationScripts/timing_feel_randomforest.py",
        "../ModelClassificationScripts/swing_randomforest.py" 
    ]

    for script in scripts:
        run_script(script)

    print("✅ All models retrained and updated.")
