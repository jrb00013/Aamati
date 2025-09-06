#!/usr/bin/env python3
"""
Optimized feature extraction script with improved error handling and logging.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.core.training_pipeline import TrainingPipeline


def setup_logging():
    """Setup logging configuration."""
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / f"feature_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)


def main():
    """Main entry point for feature extraction."""
    parser = argparse.ArgumentParser(description="Aamati Feature Extraction")
    parser.add_argument("--midi-folder", default="MusicGroovesMIDI/TrainingMIDIs",
                       help="Path to MIDI training folder")
    parser.add_argument("--output-csv", default="current_groove_features.csv",
                       help="Output CSV file")
    parser.add_argument("--log-csv", default="groove_features_log.csv",
                       help="Log CSV file")
    parser.add_argument("--models-dir", default="models",
                       help="Models directory")
    parser.add_argument("--interactive", action="store_true", default=True,
                       help="Run in interactive mode")
    parser.add_argument("--non-interactive", action="store_true",
                       help="Run in non-interactive mode")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logging()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Determine interactive mode
    interactive = args.interactive and not args.non_interactive
    
    logger.info("🚀 Starting Aamati Feature Extraction")
    logger.info(f"MIDI Folder: {args.midi_folder}")
    logger.info(f"Output CSV: {args.output_csv}")
    logger.info(f"Interactive Mode: {interactive}")
    
    try:
        # Initialize training pipeline
        pipeline = TrainingPipeline(
            midi_folder=args.midi_folder,
            output_csv=args.output_csv,
            log_csv=args.log_csv,
            models_dir=args.models_dir
        )
        
        # Run training
        pipeline.run_training(interactive=interactive)
        
        logger.info("✅ Feature extraction completed successfully!")
        
    except KeyboardInterrupt:
        logger.info("⏹️ Feature extraction interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Feature extraction failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
