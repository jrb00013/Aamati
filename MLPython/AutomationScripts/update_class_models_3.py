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
    # Add more training scripts 
    scripts = [
        "../ModelClassificationScripts/timing_feel_randomforest.py",
        "../ModelClassificationScripts/swing_randomforest.py" 
    ]

    for script in scripts:
        run_script(script)

    print("✅ All models retrained and updated.")
