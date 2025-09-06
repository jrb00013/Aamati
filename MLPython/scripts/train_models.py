#!/usr/bin/env python3
"""
Optimized model training script with improved error handling and progress tracking.
"""

import os
import sys
import argparse
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))


def setup_logging():
    """Setup logging configuration."""
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"model_training_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


def run_training_script(script_path: str, logger: logging.Logger) -> Tuple[bool, str]:
    """Run a single training script with error handling."""
    if not os.path.exists(script_path):
        error_msg = f"Script not found: {script_path}"
        logger.error(error_msg)
        return False, error_msg
    
    logger.info(f"🔄 Running {os.path.basename(script_path)}...")
    
    try:
        result = subprocess.run(
            ['python3', script_path],
            capture_output=True,
            text=True,
            timeout=600,  # 10 minute timeout
            cwd=Path(__file__).parent.parent
        )
        
        if result.returncode == 0:
            logger.info(f"✅ {os.path.basename(script_path)} completed successfully")
            if result.stdout:
                logger.debug(f"Output: {result.stdout}")
            return True, result.stdout
        else:
            error_msg = f"Script failed with return code {result.returncode}"
            if result.stderr:
                error_msg += f"\nError: {result.stderr}"
            logger.error(error_msg)
            return False, error_msg
            
    except subprocess.TimeoutExpired:
        error_msg = f"Script timed out: {os.path.basename(script_path)}"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        error_msg = f"Error running script: {e}"
        logger.error(error_msg)
        return False, error_msg


def train_basic_models(logger: logging.Logger) -> bool:
    """Train basic classification models."""
    logger.info("📊 Training basic models...")
    
    scripts = [
        "src/models/energy_randomforest.py",
        "src/models/dynamic_intensity_randomforest.py",
        "src/models/swing_randomforest.py"
    ]
    
    success_count = 0
    for script in scripts:
        success, output = run_training_script(script, logger)
        if success:
            success_count += 1
        else:
            logger.warning(f"⚠️ Failed to train {script}")
    
    logger.info(f"✅ Trained {success_count}/{len(scripts)} basic models")
    return success_count == len(scripts)


def train_advanced_models(logger: logging.Logger) -> bool:
    """Train advanced classification models."""
    logger.info("📊 Training advanced models...")
    
    scripts = [
        "src/models/fill_activity_randomforest.py",
        "src/models/timing_feel_randomforest.py",
        "src/models/fx_character_rfclassifier.py"
    ]
    
    success_count = 0
    for script in scripts:
        success, output = run_training_script(script, logger)
        if success:
            success_count += 1
        else:
            logger.warning(f"⚠️ Failed to train {script}")
    
    logger.info(f"✅ Trained {success_count}/{len(scripts)} advanced models")
    return success_count == len(scripts)


def train_specialized_models(logger: logging.Logger) -> bool:
    """Train specialized models."""
    logger.info("📊 Training specialized models...")
    
    scripts = [
        "src/models/rhythmic_density_ordinal_regression.py"
    ]
    
    success_count = 0
    for script in scripts:
        success, output = run_training_script(script, logger)
        if success:
            success_count += 1
        else:
            logger.warning(f"⚠️ Failed to train {script}")
    
    logger.info(f"✅ Trained {success_count}/{len(scripts)} specialized models")
    return success_count == len(scripts)


def train_main_model(logger: logging.Logger) -> bool:
    """Train the main mood classification model."""
    logger.info("🎯 Training main mood classification model...")
    
    script = "src/models/mood_classifier.py"
    success, output = run_training_script(script, logger)
    
    if success:
        logger.info("✅ Main mood model trained successfully")
    else:
        logger.error("❌ Failed to train main mood model")
    
    return success


def main():
    """Main entry point for model training."""
    parser = argparse.ArgumentParser(description="Aamati Model Training")
    parser.add_argument("--models", nargs="+", 
                       choices=["basic", "advanced", "specialized", "main", "all"],
                       default=["all"],
                       help="Models to train")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--skip-existing", action="store_true",
                       help="Skip training if models already exist")
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("🚀 Starting Aamati Model Training")
    logger.info(f"Models to train: {args.models}")
    
    # Check if models already exist
    if args.skip_existing:
        models_dir = Path(__file__).parent.parent / "models"
        existing_models = list(models_dir.glob("*.joblib"))
        if existing_models:
            logger.info(f"Found {len(existing_models)} existing models, skipping training")
            return
    
    success_count = 0
    total_count = 0
    
    try:
        # Train models based on selection
        if "all" in args.models or "basic" in args.models:
            total_count += 1
            if train_basic_models(logger):
                success_count += 1
        
        if "all" in args.models or "advanced" in args.models:
            total_count += 1
            if train_advanced_models(logger):
                success_count += 1
        
        if "all" in args.models or "specialized" in args.models:
            total_count += 1
            if train_specialized_models(logger):
                success_count += 1
        
        if "all" in args.models or "main" in args.models:
            total_count += 1
            if train_main_model(logger):
                success_count += 1
        
        # Summary
        if success_count == total_count:
            logger.info("🎉 All model training completed successfully!")
        else:
            logger.warning(f"⚠️ {success_count}/{total_count} model groups trained successfully")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("⏹️ Model training interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Model training failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
