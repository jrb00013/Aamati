"""
Comprehensive automation manager for the Aamati ML system.
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.mood_mappings import MOOD_DATA_TABLE, EMOJI_MAP, COLOR_MAP, RESET_COLOR


class AutomationManager:
    """Manages all automation scripts and workflows."""
    
    def __init__(self, base_dir: str = None):
        """Initialize automation manager."""
        self.base_dir = base_dir or Path(__file__).parent.parent
        self.scripts_dir = self.base_dir / "scripts"
        self.models_dir = self.base_dir / "models"
        self.data_dir = self.base_dir / "data"
        self.logs_dir = self.base_dir / "logs"
        
        # Create directories if they don't exist
        for dir_path in [self.models_dir, self.data_dir, self.logs_dir]:
            dir_path.mkdir(exist_ok=True)
    
    def run_script(self, script_name: str, args: List[str] = None, 
                   capture_output: bool = True, timeout: int = 300) -> Tuple[bool, str, str]:
        """Run a script with proper error handling and logging."""
        if args is None:
            args = []
            
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            return False, "", f"Script not found: {script_path}"
        
        print(f"🔄 Running {script_name}...")
        start_time = time.time()
        
        try:
            cmd = ['python3', str(script_path)] + args
            result = subprocess.run(
                cmd, 
                capture_output=capture_output, 
                text=True, 
                timeout=timeout,
                cwd=self.base_dir
            )
            
            elapsed = time.time() - start_time
            print(f"✅ {script_name} completed in {elapsed:.2f}s")
            
            if result.returncode != 0:
                print(f"⚠️ {script_name} returned code {result.returncode}")
                if result.stderr:
                    print(f"Error: {result.stderr}")
            
            return result.returncode == 0, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            print(f"⏰ {script_name} timed out after {timeout}s")
            return False, "", "Script timed out"
        except Exception as e:
            print(f"❌ Error running {script_name}: {e}")
            return False, "", str(e)
    
    def run_training_workflow(self, interactive: bool = True) -> bool:
        """Run the complete training workflow."""
        print("🚀 Starting Training Workflow")
        print("=" * 50)
        
        # Step 1: Extract features
        success, stdout, stderr = self.run_script(
            "extract_features.py", 
            ["--interactive" if interactive else "--non-interactive"]
        )
        if not success:
            print("❌ Feature extraction failed")
            return False
        
        # Step 2: Train models
        success, stdout, stderr = self.run_script("train_models.py")
        if not success:
            print("❌ Model training failed")
            return False
        
        # Step 3: Generate predictions
        success, stdout, stderr = self.run_script("generate_predictions.py")
        if not success:
            print("❌ Prediction generation failed")
            return False
        
        print("✅ Training workflow completed successfully!")
        return True
    
    def run_model_update_workflow(self, model_groups: List[str] = None) -> bool:
        """Run model update workflow for specific model groups."""
        if model_groups is None:
            model_groups = ["basic", "advanced", "specialized"]
        
        print("🔄 Starting Model Update Workflow")
        print("=" * 50)
        
        for group in model_groups:
            print(f"\n📊 Updating {group} models...")
            success, stdout, stderr = self.run_script(f"update_models_{group}.py")
            if not success:
                print(f"❌ Failed to update {group} models")
                return False
        
        print("✅ Model update workflow completed!")
        return True
    
    def run_data_management_workflow(self) -> bool:
        """Run data management workflow."""
        print("📁 Starting Data Management Workflow")
        print("=" * 50)
        
        # Step 1: Filter new MIDIs
        success, stdout, stderr = self.run_script("filter_new_midis.py")
        if not success:
            print("❌ MIDI filtering failed")
            return False
        
        # Step 2: Copy groove features
        success, stdout, stderr = self.run_script("copy_groove_features.py")
        if not success:
            print("❌ Feature copying failed")
            return False
        
        # Step 3: Compare mood data
        success, stdout, stderr = self.run_script("compare_mood_data.py")
        if not success:
            print("❌ Mood data comparison failed")
            return False
        
        print("✅ Data management workflow completed!")
        return True
    
    def run_cleanup_workflow(self) -> bool:
        """Run cleanup workflow."""
        print("🧹 Starting Cleanup Workflow")
        print("=" * 50)
        
        # Step 1: Reset groove features
        success, stdout, stderr = self.run_script("reset_groove_features.py")
        if not success:
            print("❌ Feature reset failed")
            return False
        
        # Step 2: Clean temporary files
        self._cleanup_temp_files()
        
        print("✅ Cleanup workflow completed!")
        return True
    
    def _cleanup_temp_files(self):
        """Clean up temporary files."""
        temp_extensions = ['.tmp', '.temp', '.log', '.cache']
        cleaned_count = 0
        
        for root, dirs, files in os.walk(self.base_dir):
            for file in files:
                if any(file.endswith(ext) for ext in temp_extensions):
                    try:
                        os.remove(os.path.join(root, file))
                        cleaned_count += 1
                    except:
                        pass
        
        if cleaned_count > 0:
            print(f"🧹 Cleaned {cleaned_count} temporary files")
    
    def get_system_status(self) -> Dict:
        """Get current system status."""
        status = {
            "models_loaded": self._check_models_loaded(),
            "data_files": self._check_data_files(),
            "logs": self._check_logs(),
            "disk_usage": self._get_disk_usage()
        }
        return status
    
    def _check_models_loaded(self) -> bool:
        """Check if models are properly loaded."""
        required_models = [
            "energy_random_forest.joblib",
            "dynamic_intensity_randomforest.joblib",
            "swing_random_forest.joblib",
            "fill_activity_randomforest.joblib",
            "rhythmic_density_ordinal_regression.joblib",
            "fx_character_classifier.joblib",
            "timing_feel_randomforest.joblib"
        ]
        
        for model in required_models:
            if not (self.models_dir / model).exists():
                return False
        return True
    
    def _check_data_files(self) -> Dict:
        """Check data file status."""
        data_files = {
            "current_groove_features.csv": (self.base_dir / "current_groove_features.csv").exists(),
            "groove_features_log.csv": (self.base_dir / "groove_features_log.csv").exists(),
            "mood_feature_map.json": (self.base_dir / "mood_feature_map.json").exists()
        }
        return data_files
    
    def _check_logs(self) -> List[str]:
        """Check available log files."""
        log_files = []
        for file in self.logs_dir.glob("*.log"):
            log_files.append(file.name)
        return log_files
    
    def _get_disk_usage(self) -> Dict:
        """Get disk usage information."""
        import shutil
        
        total, used, free = shutil.disk_usage(self.base_dir)
        return {
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2),
            "usage_percent": round((used / total) * 100, 2)
        }
    
    def print_status(self):
        """Print current system status."""
        status = self.get_system_status()
        
        print("📊 Aamati ML System Status")
        print("=" * 40)
        
        # Models status
        models_status = "✅ Loaded" if status["models_loaded"] else "❌ Missing"
        print(f"Models: {models_status}")
        
        # Data files status
        print("\n📁 Data Files:")
        for file, exists in status["data_files"].items():
            status_icon = "✅" if exists else "❌"
            print(f"  {status_icon} {file}")
        
        # Logs
        if status["logs"]:
            print(f"\n📋 Log Files ({len(status['logs'])}):")
            for log in status["logs"][:5]:  # Show first 5
                print(f"  📄 {log}")
            if len(status["logs"]) > 5:
                print(f"  ... and {len(status['logs']) - 5} more")
        
        # Disk usage
        disk = status["disk_usage"]
        print(f"\n💾 Disk Usage:")
        print(f"  Used: {disk['used_gb']}GB / {disk['total_gb']}GB ({disk['usage_percent']}%)")
        print(f"  Free: {disk['free_gb']}GB")


def main():
    """Main entry point for automation manager."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Aamati ML Automation Manager")
    parser.add_argument("--workflow", choices=[
        "training", "model-update", "data-management", "cleanup", "status"
    ], required=True, help="Workflow to run")
    parser.add_argument("--interactive", action="store_true", 
                       help="Run in interactive mode")
    parser.add_argument("--model-groups", nargs="+", 
                       choices=["basic", "advanced", "specialized"],
                       help="Model groups to update")
    
    args = parser.parse_args()
    
    manager = AutomationManager()
    
    if args.workflow == "training":
        success = manager.run_training_workflow(interactive=args.interactive)
    elif args.workflow == "model-update":
        success = manager.run_model_update_workflow(model_groups=args.model_groups)
    elif args.workflow == "data-management":
        success = manager.run_data_management_workflow()
    elif args.workflow == "cleanup":
        success = manager.run_cleanup_workflow()
    elif args.workflow == "status":
        manager.print_status()
        success = True
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
