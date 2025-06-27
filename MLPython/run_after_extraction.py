import subprocess

def run_script(script_name):
    print(f"Running {script_name} ...")
    result = subprocess.run(['python3', script_name], capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Errors/warnings:")
        print(result.stderr)

if __name__ == "__main__":
    scripts = [
        "MachineLearningModel.py",
        "predict_groove_mood.py"
    ]

    for script in scripts:
        run_script(script)
