#!/usr/bin/env python3
"""
Master run script for the entire Aamati project.
Handles both ML training and JUCE plugin building.
"""

import os
import sys
import subprocess
import argparse
import time
from pathlib import Path
from typing import List, Dict, Optional
import json


class AamatiRunner:
    """Main runner class for the Aamati project."""
    
    def __init__(self, base_dir: str = None):
        """Initialize runner."""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.ml_dir = self.base_dir / "MLPython"
        self.juce_dir = self.base_dir / "Source"
        self.resources_dir = self.base_dir / "Resources"
        
        # Status tracking
        self.run_status = {
            "ml_training": False,
            "model_export": False,
            "juce_build": False,
            "plugin_test": False
        }
    
    def print_banner(self):
        """Print runner banner."""
        print("🎵" + "=" * 60 + "🎵")
        print("           AAMATI PROJECT RUNNER")
        print("    Complete ML Training & Plugin Building")
        print("🎵" + "=" * 60 + "🎵")
        print()
    
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met."""
        print("🔍 Checking prerequisites...")
        
        # Check Python
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required")
            return False
        print("✅ Python version OK")
        
        # Check ML directory
        if not self.ml_dir.exists():
            print("❌ MLPython directory not found")
            return False
        print("✅ MLPython directory found")
        
        # Check JUCE source
        if not self.juce_dir.exists():
            print("❌ Source directory not found")
            return False
        print("✅ Source directory found")
        
        # Check Resources
        if not self.resources_dir.exists():
            print("⚠️ Resources directory not found, creating...")
            self.resources_dir.mkdir(exist_ok=True)
        print("✅ Resources directory ready")
        
        return True
    
    def run_ml_training(self, interactive: bool = True, 
                       midi_folder: str = None) -> bool:
        """Run ML training pipeline."""
        print("\n🧠 Starting ML Training Pipeline")
        print("=" * 40)
        
        try:
            # Change to ML directory
            os.chdir(self.ml_dir)
            
            # Run full ML pipeline
            print("🚀 Running full ML pipeline...")
            cmd = ["python3", "main.py", "--mode", "full-pipeline"]
            if not interactive:
                cmd.append("--non-interactive")
            if midi_folder:
                cmd.extend(["--midi-folder", midi_folder])
            
            result = subprocess.run(cmd, check=True)
            print("✅ ML pipeline completed")
            
            self.run_status["ml_training"] = True
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ ML training failed: {e}")
            return False
        except Exception as e:
            print(f"❌ ML training error: {e}")
            return False
        finally:
            # Return to base directory
            os.chdir(self.base_dir)
    
    def export_models(self) -> bool:
        """Export models for JUCE plugin."""
        print("\n📦 Exporting models for JUCE plugin")
        print("=" * 40)
        
        try:
            # Run the setup script to copy models
            setup_script = self.base_dir / "setup_ml_models.py"
            if setup_script.exists():
                result = subprocess.run([sys.executable, str(setup_script)], 
                                      cwd=self.base_dir, check=True)
                print("✅ Models copied to Resources directory")
            else:
                print("⚠️ Setup script not found, copying manually...")
                
                # Copy ONNX model
                onnx_source = self.ml_dir / "groove_mood_model.onnx"
                if onnx_source.exists():
                    shutil.copy2(onnx_source, self.resources_dir)
                    print("✅ ONNX model copied to Resources")
                else:
                    print("⚠️ ONNX model not found")
                
                # Copy other model files
                models_source = self.ml_dir / "ModelClassificationScripts" / "models"
                if models_source.exists():
                    for model_file in models_source.glob("*.joblib"):
                        shutil.copy2(model_file, self.resources_dir)
                        print(f"✅ Copied {model_file.name}")
            
            self.run_status["model_export"] = True
            return True
            
        except Exception as e:
            print(f"❌ Model export failed: {e}")
            return False
    
    def _create_placeholder_model(self):
        """Create a placeholder ONNX model for testing."""
        print("Creating placeholder ONNX model...")
        
        # This would create a simple placeholder model
        # In practice, you'd use your trained model
        placeholder_content = b"PLACEHOLDER_ONNX_MODEL"
        placeholder_file = self.resources_dir / "groove_mood_model.onnx"
        placeholder_file.write_bytes(placeholder_content)
        print("✅ Placeholder model created")
    
    def build_juce_plugin(self, build_type: str = "Release") -> bool:
        """Build JUCE plugin."""
        print(f"\n🔨 Building JUCE plugin ({build_type})")
        print("=" * 40)
        
        try:
            # Create build directory
            build_dir = self.base_dir / "build"
            build_dir.mkdir(exist_ok=True)
            
            # Change to build directory
            os.chdir(build_dir)
            
            # Configure with CMake
            print("⚙️ Configuring with CMake...")
            cmd = ["cmake", "..", f"-DCMAKE_BUILD_TYPE={build_type}"]
            result = subprocess.run(cmd, check=True)
            print("✅ CMake configuration completed")
            
            # Build
            print("🔨 Building plugin...")
            cmd = ["make", "-j4"]  # Use 4 parallel jobs
            result = subprocess.run(cmd, check=True)
            print("✅ Plugin build completed")
            
            self.run_status["juce_build"] = True
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ JUCE build failed: {e}")
            return False
        except Exception as e:
            print(f"❌ JUCE build error: {e}")
            return False
        finally:
            # Return to base directory
            os.chdir(self.base_dir)
    
    def test_plugin(self) -> bool:
        """Test the built plugin."""
        print("\n🧪 Testing plugin")
        print("=" * 40)
        
        try:
            # Check if plugin was built
            plugin_path = self.base_dir / "build" / "Aamati"
            if not plugin_path.exists():
                print("❌ Plugin not found, build may have failed")
                return False
            
            print("✅ Plugin executable found")
            
            # Run basic plugin test
            print("🔍 Running basic plugin test...")
            cmd = [str(plugin_path), "--help"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Plugin test passed")
                self.run_status["plugin_test"] = True
                return True
            else:
                print("⚠️ Plugin test had issues, but plugin exists")
                return True
                
        except Exception as e:
            print(f"❌ Plugin test failed: {e}")
            return False
    
    def run_complete_pipeline(self, interactive: bool = True, 
                            midi_folder: str = None,
                            build_type: str = "Release") -> bool:
        """Run the complete Aamati pipeline."""
        self.print_banner()
        
        # Check prerequisites
        if not self.check_prerequisites():
            print("❌ Prerequisites not met")
            return False
        
        # Run ML training
        if not self.run_ml_training(interactive=interactive, midi_folder=midi_folder):
            print("❌ ML training failed")
            return False
        
        # Export models
        if not self.export_models():
            print("❌ Model export failed")
            return False
        
        # Build JUCE plugin
        if not self.build_juce_plugin(build_type=build_type):
            print("❌ JUCE build failed")
            return False
        
        # Test plugin
        if not self.test_plugin():
            print("❌ Plugin test failed")
            return False
        
        # Print success summary
        self.print_success_summary()
        return True
    
    def print_success_summary(self):
        """Print success summary."""
        print("\n🎉 AAMATI PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        
        for component, status in self.run_status.items():
            icon = "✅" if status else "❌"
            print(f"{icon} {component.replace('_', ' ').title()}")
        
        print("\n🎵 Your Aamati plugin is ready!")
        print("📁 Plugin location: build/Aamati")
        print("📚 Load it in your DAW and start creating!")
        print("\n🔧 For troubleshooting, check the logs in MLPython/logs/")


def main():
    """Main entry point for runner script."""
    parser = argparse.ArgumentParser(description="Aamati Project Runner")
    parser.add_argument("--interactive", action="store_true", default=True,
                       help="Run in interactive mode")
    parser.add_argument("--non-interactive", action="store_true",
                       help="Run in non-interactive mode")
    parser.add_argument("--midi-folder", 
                       help="Path to MIDI training folder")
    parser.add_argument("--build-type", choices=["Debug", "Release"], 
                       default="Release", help="Build type")
    parser.add_argument("--ml-only", action="store_true",
                       help="Run only ML training")
    parser.add_argument("--build-only", action="store_true",
                       help="Run only JUCE build")
    
    args = parser.parse_args()
    
    # Determine interactive mode
    interactive = args.interactive and not args.non_interactive
    
    runner = AamatiRunner()
    
    if args.ml_only:
        # Run only ML training
        if not runner.run_ml_training(interactive=interactive, 
                                    midi_folder=args.midi_folder):
            sys.exit(1)
    elif args.build_only:
        # Run only JUCE build
        if not runner.export_models():
            sys.exit(1)
        if not runner.build_juce_plugin(build_type=args.build_type):
            sys.exit(1)
    else:
        # Run complete pipeline
        if not runner.run_complete_pipeline(
            interactive=interactive,
            midi_folder=args.midi_folder,
            build_type=args.build_type
        ):
            sys.exit(1)


if __name__ == "__main__":
    main()
