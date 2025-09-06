#!/usr/bin/env python3
"""
Comprehensive integration tests for the Aamati project.
Tests all components and their interactions with detailed logging.
"""

import os
import sys
import subprocess
import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import traceback
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('aamati_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AamatiTester:
    """Comprehensive test suite for Aamati project."""
    
    def __init__(self, base_dir: str = None):
        """Initialize tester."""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.ml_dir = self.base_dir / "MLPython"
        self.source_dir = self.base_dir / "Source"
        self.resources_dir = self.base_dir / "Resources"
        
        # Test results
        self.test_results = {
            "python_environment": False,
            "ml_dependencies": False,
            "juce_environment": False,
            "data_structure": False,
            "feature_extraction": False,
            "model_training": False,
            "model_prediction": False,
            "model_export": False,
            "juce_compilation": False,
            "plugin_integration": False,
            "end_to_end": False
        }
        
        # Test data
        self.test_midi_file = None
        self.test_features = None
        self.test_predictions = None
        
        logger.info("🧪 AamatiTester initialized")
    
    def run_all_tests(self) -> bool:
        """Run all integration tests."""
        logger.info("🚀 Starting comprehensive Aamati integration tests")
        logger.info("=" * 60)
        
        start_time = time.time()
        
        # Test sequence
        tests = [
            ("Python Environment", self.test_python_environment),
            ("ML Dependencies", self.test_ml_dependencies),
            ("JUCE Environment", self.test_juce_environment),
            ("Data Structure", self.test_data_structure),
            ("Feature Extraction", self.test_feature_extraction),
            ("Model Training", self.test_model_training),
            ("Model Prediction", self.test_model_prediction),
            ("Model Export", self.test_model_export),
            ("JUCE Compilation", self.test_juce_compilation),
            ("Plugin Integration", self.test_plugin_integration),
            ("End-to-End Pipeline", self.test_end_to_end)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            logger.info(f"\n🔍 Running {test_name} test...")
            try:
                result = test_func()
                if result:
                    logger.info(f"✅ {test_name} test PASSED")
                    passed += 1
                else:
                    logger.error(f"❌ {test_name} test FAILED")
            except Exception as e:
                logger.error(f"❌ {test_name} test ERROR: {e}")
                logger.error(traceback.format_exc())
        
        # Summary
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"\n📊 Test Summary")
        logger.info("=" * 40)
        logger.info(f"Tests passed: {passed}/{total}")
        logger.info(f"Success rate: {(passed/total)*100:.1f}%")
        logger.info(f"Duration: {duration:.2f} seconds")
        
        if passed == total:
            logger.info("🎉 All tests passed! System is fully operational.")
            return True
        else:
            logger.warning(f"⚠️ {total-passed} tests failed. Check logs for details.")
            return False
    
    def test_python_environment(self) -> bool:
        """Test Python environment and version."""
        logger.info("🐍 Testing Python environment...")
        
        try:
            # Check Python version
            version = sys.version_info
            if version < (3, 8):
                logger.error(f"Python {version.major}.{version.minor} is too old. Need 3.8+")
                return False
            
            logger.info(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
            
            # Check required modules
            required_modules = [
                'pandas', 'numpy', 'scikit-learn', 'joblib', 
                'pretty_midi', 'scipy', 'matplotlib', 'seaborn'
            ]
            
            missing_modules = []
            for module in required_modules:
                try:
                    __import__(module)
                    logger.info(f"✅ {module} available")
                except ImportError:
                    missing_modules.append(module)
                    logger.error(f"❌ {module} missing")
            
            if missing_modules:
                logger.error(f"Missing modules: {missing_modules}")
                return False
            
            self.test_results["python_environment"] = True
            return True
            
        except Exception as e:
            logger.error(f"Python environment test failed: {e}")
            return False
    
    def test_ml_dependencies(self) -> bool:
        """Test ML-specific dependencies."""
        logger.info("🤖 Testing ML dependencies...")
        
        try:
            # Test ONNX Runtime
            try:
                import onnxruntime as ort
                logger.info(f"✅ ONNX Runtime {ort.__version__} available")
            except ImportError:
                logger.warning("⚠️ ONNX Runtime not available (needed for JUCE)")
            
            # Test model files
            model_files = [
                "ModelClassificationScripts/models/energy_random_forest.joblib",
                "ModelClassificationScripts/models/swing_random_forest.joblib",
                "ModelClassificationScripts/models/dynamic_intensity_randomforest.joblib"
            ]
            
            for model_file in model_files:
                model_path = self.ml_dir / model_file
                if model_path.exists():
                    logger.info(f"✅ {model_file} found")
                else:
                    logger.warning(f"⚠️ {model_file} not found")
            
            self.test_results["ml_dependencies"] = True
            return True
            
        except Exception as e:
            logger.error(f"ML dependencies test failed: {e}")
            return False
    
    def test_juce_environment(self) -> bool:
        """Test JUCE environment."""
        logger.info("🎛️ Testing JUCE environment...")
        
        try:
            # Check JUCE source files
            required_files = [
                "PluginProcessor.cpp", "PluginProcessor.h",
                "PluginEditor.cpp", "PluginEditor.h",
                "FeatureExtractor.cpp", "FeatureExtractor.h",
                "ModelRunner.cpp", "ModelRunner.h"
            ]
            
            missing_files = []
            for file in required_files:
                file_path = self.source_dir / file
                if file_path.exists():
                    logger.info(f"✅ {file} found")
                else:
                    missing_files.append(file)
                    logger.error(f"❌ {file} missing")
            
            if missing_files:
                logger.error(f"Missing JUCE files: {missing_files}")
                return False
            
            # Check CMakeLists.txt
            cmake_file = self.base_dir / "CMakeLists.txt"
            if cmake_file.exists():
                logger.info("✅ CMakeLists.txt found")
            else:
                logger.warning("⚠️ CMakeLists.txt not found")
            
            self.test_results["juce_environment"] = True
            return True
            
        except Exception as e:
            logger.error(f"JUCE environment test failed: {e}")
            return False
    
    def test_data_structure(self) -> bool:
        """Test data directory structure."""
        logger.info("📁 Testing data structure...")
        
        try:
            # Check MLPython structure
            required_dirs = [
                "data/csv", "data/logs", "data/exports",
                "models/trained", "models/checkpoints",
                "src/core", "scripts", "config"
            ]
            
            for dir_path in required_dirs:
                full_path = self.ml_dir / dir_path
                if full_path.exists():
                    logger.info(f"✅ {dir_path}/ directory exists")
                else:
                    logger.warning(f"⚠️ {dir_path}/ directory missing")
                    # Create missing directories
                    full_path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"✅ Created {dir_path}/ directory")
            
            # Check MIDI directories
            midi_dirs = ["MusicGroovesMIDI/TrainingMIDIs", "MusicGroovesMIDI/ProcessedMIDIs"]
            for midi_dir in midi_dirs:
                full_path = self.ml_dir / midi_dir
                if full_path.exists():
                    logger.info(f"✅ {midi_dir}/ directory exists")
                else:
                    logger.warning(f"⚠️ {midi_dir}/ directory missing")
                    full_path.mkdir(parents=True, exist_ok=True)
                    logger.info(f"✅ Created {midi_dir}/ directory")
            
            self.test_results["data_structure"] = True
            return True
            
        except Exception as e:
            logger.error(f"Data structure test failed: {e}")
            return False
    
    def test_feature_extraction(self) -> bool:
        """Test feature extraction functionality."""
        logger.info("📊 Testing feature extraction...")
        
        try:
            # Create a test MIDI file if none exists
            test_midi_path = self.ml_dir / "MusicGroovesMIDI/TrainingMIDIs/test.mid"
            if not test_midi_path.exists():
                logger.info("Creating test MIDI file...")
                self._create_test_midi_file(test_midi_path)
            
            # Test feature extraction
            os.chdir(self.ml_dir)
            
            # Run feature extraction on test file
            cmd = [
                "python3", "extract_groove_features.py",
                "--midi-folder", "MusicGroovesMIDI/TrainingMIDIs",
                "--max-files", "1",
                "--non-interactive",
                "--verbose"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("✅ Feature extraction test passed")
                
                # Check if features were extracted
                csv_file = self.ml_dir / "data/csv/groove_features_log.csv"
                if csv_file.exists():
                    df = pd.read_csv(csv_file)
                    if len(df) > 0:
                        logger.info(f"✅ Extracted {len(df)} feature records")
                        self.test_features = df.iloc[0].to_dict()
                    else:
                        logger.warning("⚠️ No features extracted")
                else:
                    logger.warning("⚠️ Feature CSV not created")
                
                self.test_results["feature_extraction"] = True
                return True
            else:
                logger.error(f"Feature extraction failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Feature extraction test failed: {e}")
            return False
        finally:
            os.chdir(self.base_dir)
    
    def test_model_training(self) -> bool:
        """Test model training functionality."""
        logger.info("🤖 Testing model training...")
        
        try:
            # Check if we have training data
            pred_csv = self.ml_dir / "data/csv/groove_features_log_for_pred.csv"
            if not pred_csv.exists():
                logger.warning("⚠️ No training data found, creating test data...")
                self._create_test_training_data()
            
            os.chdir(self.ml_dir)
            
            # Test model training
            cmd = ["python3", "train_models.py", "--verbose"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("✅ Model training test passed")
                
                # Check if models were created
                model_files = [
                    "ModelClassificationScripts/models/energy_random_forest.joblib",
                    "ModelClassificationScripts/models/swing_random_forest.joblib"
                ]
                
                models_created = 0
                for model_file in model_files:
                    if (self.ml_dir / model_file).exists():
                        models_created += 1
                        logger.info(f"✅ {model_file} created")
                
                if models_created > 0:
                    logger.info(f"✅ {models_created} models created")
                    self.test_results["model_training"] = True
                    return True
                else:
                    logger.warning("⚠️ No models were created")
                    return False
            else:
                logger.error(f"Model training failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Model training test failed: {e}")
            return False
        finally:
            os.chdir(self.base_dir)
    
    def test_model_prediction(self) -> bool:
        """Test model prediction functionality."""
        logger.info("🔮 Testing model prediction...")
        
        try:
            os.chdir(self.ml_dir)
            
            # Test prediction
            cmd = [
                "python3", "predict_groove_mood.py",
                "--csv-file", "data/csv/groove_features_log_for_pred.csv",
                "--verbose"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("✅ Model prediction test passed")
                
                # Check if predictions were generated
                output_file = self.ml_dir / "data/csv/groove_features_log_for_pred_with_predictions.csv"
                if output_file.exists():
                    df = pd.read_csv(output_file)
                    if 'predicted_mood' in df.columns:
                        logger.info(f"✅ Generated predictions for {len(df)} records")
                        self.test_predictions = df['predicted_mood'].tolist()
                    else:
                        logger.warning("⚠️ No predicted_mood column found")
                else:
                    logger.warning("⚠️ Prediction output file not created")
                
                self.test_results["model_prediction"] = True
                return True
            else:
                logger.error(f"Model prediction failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Model prediction test failed: {e}")
            return False
        finally:
            os.chdir(self.base_dir)
    
    def test_model_export(self) -> bool:
        """Test model export functionality."""
        logger.info("📦 Testing model export...")
        
        try:
            # Test model export
            cmd = ["python3", "../setup_ml_models.py"]
            result = subprocess.run(cmd, cwd=self.ml_dir, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info("✅ Model export test passed")
                
                # Check if models were exported
                onnx_model = self.resources_dir / "groove_mood_model.onnx"
                if onnx_model.exists():
                    logger.info("✅ ONNX model exported to Resources")
                else:
                    logger.warning("⚠️ ONNX model not found in Resources")
                
                self.test_results["model_export"] = True
                return True
            else:
                logger.error(f"Model export failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Model export test failed: {e}")
            return False
    
    def test_juce_compilation(self) -> bool:
        """Test JUCE compilation."""
        logger.info("🔨 Testing JUCE compilation...")
        
        try:
            # Check if build directory exists
            build_dir = self.base_dir / "build"
            if not build_dir.exists():
                build_dir.mkdir()
                logger.info("✅ Created build directory")
            
            # Test CMake configuration
            os.chdir(self.base_dir)
            cmd = ["cmake", "-B", "build", "-S", "."]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("✅ CMake configuration successful")
                
                # Test compilation
                cmd = ["cmake", "--build", "build", "--config", "Release"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    logger.info("✅ JUCE compilation successful")
                    self.test_results["juce_compilation"] = True
                    return True
                else:
                    logger.error(f"JUCE compilation failed: {result.stderr}")
                    return False
            else:
                logger.error(f"CMake configuration failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"JUCE compilation test failed: {e}")
            return False
    
    def test_plugin_integration(self) -> bool:
        """Test plugin integration."""
        logger.info("🔌 Testing plugin integration...")
        
        try:
            # Check if plugin files exist
            plugin_files = [
                "build/Aamati_artefacts/Release/VST3/Aamati.vst3",
                "build/Aamati_artefacts/Release/AU/Aamati.component",
                "build/Aamati_artefacts/Release/Standalone/Aamati.app"
            ]
            
            plugins_found = 0
            for plugin_file in plugin_files:
                plugin_path = self.base_dir / plugin_file
                if plugin_path.exists():
                    plugins_found += 1
                    logger.info(f"✅ {plugin_file} found")
                else:
                    logger.warning(f"⚠️ {plugin_file} not found")
            
            if plugins_found > 0:
                logger.info(f"✅ {plugins_found} plugin formats available")
                self.test_results["plugin_integration"] = True
                return True
            else:
                logger.warning("⚠️ No plugin files found")
                return False
                
        except Exception as e:
            logger.error(f"Plugin integration test failed: {e}")
            return False
    
    def test_end_to_end(self) -> bool:
        """Test complete end-to-end pipeline."""
        logger.info("🔄 Testing end-to-end pipeline...")
        
        try:
            # Run complete pipeline
            cmd = [
                "python3", "run_aamati.py",
                "--full-pipeline",
                "--non-interactive"
            ]
            
            result = subprocess.run(cmd, cwd=self.base_dir, capture_output=True, text=True, timeout=600)
            
            if result.returncode == 0:
                logger.info("✅ End-to-end pipeline test passed")
                self.test_results["end_to_end"] = True
                return True
            else:
                logger.error(f"End-to-end pipeline failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"End-to-end pipeline test failed: {e}")
            return False
    
    def _create_test_midi_file(self, file_path: Path):
        """Create a simple test MIDI file."""
        try:
            import pretty_midi
            
            # Create a simple MIDI file
            midi = pretty_midi.PrettyMIDI()
            piano = pretty_midi.Instrument(program=0)  # Acoustic Grand Piano
            
            # Add some notes
            notes = [
                (60, 0.0, 1.0, 80),  # C4
                (64, 1.0, 2.0, 80),  # E4
                (67, 2.0, 3.0, 80),  # G4
            ]
            
            for pitch, start, end, velocity in notes:
                note = pretty_midi.Note(
                    velocity=velocity,
                    pitch=pitch,
                    start=start,
                    end=end
                )
                piano.notes.append(note)
            
            midi.instruments.append(piano)
            midi.write(str(file_path))
            logger.info(f"✅ Created test MIDI file: {file_path}")
            
        except Exception as e:
            logger.error(f"Failed to create test MIDI file: {e}")
    
    def _create_test_training_data(self):
        """Create test training data."""
        try:
            # Create test features
            test_data = {
                'tempo': [120.0, 140.0, 100.0],
                'swing': [0.5, 0.3, 0.7],
                'density': [15.0, 25.0, 10.0],
                'dynamic_range': [80.0, 120.0, 60.0],
                'energy': [8.0, 12.0, 6.0],
                'velocity_mean': [70.0, 90.0, 50.0],
                'velocity_std': [15.0, 20.0, 10.0],
                'pitch_mean': [60.0, 65.0, 55.0],
                'pitch_range': [24.0, 36.0, 12.0],
                'avg_polyphony': [3.0, 5.0, 2.0],
                'syncopation': [0.1, 0.3, 0.05],
                'onset_entropy': [0.5, 0.8, 0.3],
                'instrument_count': [1, 2, 1],
                'primary_mood': ['energetic', 'chill', 'romantic'],
                'secondary_mood': ['energetic', 'chill', 'romantic'],
                'timing_feel': [0, 2, 1],
                'rhythmic_density': [2, 1, 0],
                'dynamic_intensity': [6, 3, 5],
                'fill_activity': [4, 2, 3],
                'fx_character': [1, 0, 2],
                'timestamp': ['2024-01-01T00:00:00'] * 3,
                'midi_file_name': ['test1.mid', 'test2.mid', 'test3.mid']
            }
            
            df = pd.DataFrame(test_data)
            pred_csv = self.ml_dir / "data/csv/groove_features_log_for_pred.csv"
            df.to_csv(pred_csv, index=False)
            logger.info(f"✅ Created test training data: {pred_csv}")
            
        except Exception as e:
            logger.error(f"Failed to create test training data: {e}")
    
    def generate_test_report(self) -> str:
        """Generate a comprehensive test report."""
        report = []
        report.append("🧪 AAMATI INTEGRATION TEST REPORT")
        report.append("=" * 50)
        report.append(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Test results
        report.append("📊 TEST RESULTS:")
        for test_name, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            report.append(f"  {test_name.replace('_', ' ').title()}: {status}")
        
        report.append("")
        
        # Summary
        passed = sum(self.test_results.values())
        total = len(self.test_results)
        success_rate = (passed / total) * 100
        
        report.append(f"📈 SUMMARY:")
        report.append(f"  Tests Passed: {passed}/{total}")
        report.append(f"  Success Rate: {success_rate:.1f}%")
        report.append(f"  Status: {'🎉 ALL SYSTEMS OPERATIONAL' if passed == total else '⚠️ SOME ISSUES DETECTED'}")
        
        return "\n".join(report)


def main():
    """Main entry point for testing."""
    parser = argparse.ArgumentParser(description="Aamati Integration Tests")
    parser.add_argument("--component", choices=[
        "python", "ml", "juce", "integration", "all"
    ], default="all", help="Component to test")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    parser.add_argument("--report", action="store_true",
                       help="Generate test report")
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create tester
    tester = AamatiTester()
    
    # Run tests
    if args.component == "all":
        success = tester.run_all_tests()
    else:
        # Run specific component tests
        if args.component == "python":
            success = tester.test_python_environment()
        elif args.component == "ml":
            success = (tester.test_ml_dependencies() and 
                      tester.test_feature_extraction() and
                      tester.test_model_training())
        elif args.component == "juce":
            success = (tester.test_juce_environment() and
                      tester.test_juce_compilation() and
                      tester.test_plugin_integration())
        elif args.component == "integration":
            success = tester.test_end_to_end()
    
    # Generate report
    if args.report:
        report = tester.generate_test_report()
        print("\n" + report)
        
        # Save report
        report_file = Path("aamati_test_report.txt")
        with open(report_file, 'w') as f:
            f.write(report)
        print(f"\n📄 Test report saved to: {report_file}")
    
    return success


if __name__ == "__main__":
    import argparse
    success = main()
    sys.exit(0 if success else 1)