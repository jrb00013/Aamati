#!/usr/bin/env python3
"""
Main entry point for the Aamati ML system.
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.core.training_pipeline import TrainingPipeline
from scripts.automation_manager import AutomationManager


def main():
    """Main entry point for ML system."""
    parser = argparse.ArgumentParser(description="Aamati ML System")
    parser.add_argument("--mode", choices=[
        "extract", "train", "predict", "automate", "status"
    ], required=True, help="Operation mode")
    parser.add_argument("--interactive", action="store_true", default=True,
                       help="Run in interactive mode")
    parser.add_argument("--midi-folder", 
                       help="Path to MIDI folder")
    parser.add_argument("--output-csv", 
                       help="Output CSV file")
    parser.add_argument("--workflow", 
                       help="Automation workflow to run")
    
    args = parser.parse_args()
    
    if args.mode == "extract":
        # Run feature extraction
        pipeline = TrainingPipeline(
            midi_folder=args.midi_folder or "MusicGroovesMIDI/TrainingMIDIs",
            output_csv=args.output_csv or "current_groove_features.csv"
        )
        pipeline.run_training(interactive=args.interactive)
        
    elif args.mode == "train":
        # Run model training
        from scripts.train_models import main as train_main
        train_main()
        
    elif args.mode == "predict":
        # Run predictions
        from scripts.generate_predictions import main as predict_main
        predict_main()
        
    elif args.mode == "automate":
        # Run automation
        manager = AutomationManager()
        if args.workflow:
            if args.workflow == "training":
                manager.run_training_workflow(interactive=args.interactive)
            elif args.workflow == "model-update":
                manager.run_model_update_workflow()
            elif args.workflow == "data-management":
                manager.run_data_management_workflow()
            elif args.workflow == "cleanup":
                manager.run_cleanup_workflow()
        else:
            print("Please specify --workflow")
            
    elif args.mode == "status":
        # Show status
        manager = AutomationManager()
        manager.print_status()


if __name__ == "__main__":
    main()
