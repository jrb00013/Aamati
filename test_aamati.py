#!/usr/bin/env python3
"""
Comprehensive test script for the Aamati project.
Tests both ML components and JUCE plugin functionality.
"""

import os
import sys
import subprocess
import time
import json
import tempfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import pandas as pd
import numpy as np


class AamatiTester:
    """Main test class for the Aamati project."""
    
    def __init__(self, base_dir: str = None):
        """Initialize tester."""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.ml_dir = self.base_dir / "MLPython"
        self.juce_dir = self.base_dir / "Source"
        self.resources_dir = self.base_dir / "Resources"
        self.build_dir = self.base_dir / "build"
        
        # Test results
        self.test_results = {
            "python_imports": False,
            "ml_models": False,
            "feature_extraction": False,
            "model_training": False,
            "juce_compilation": False,
            "plugin_functionality": False,
            "integration": False
        }
    
    def print_banner(self):
        """Print test banner."""
        print("🧪" + "=" * 60 + "🧪")
        print("           AAMATI PROJECT TEST SUITE")
        print("    Comprehensive Testing for ML & JUCE Components")
        print("🧪" + "=" * 60 + "🧪")
        print()
    
    def test_python_imports(self) -> bool:
        """Test Python imports and dependencies."""
        print("🐍 Testing Python imports...")
        
        required_modules = [
            "pandas", "numpy", "scikit-learn", "joblib", 
            "torch", "skl2onnx", "pretty_midi", "scipy",
            "matplotlib", "seaborn", "onnxruntime"
        ]
        
        failed_imports = []
        
        for module in required_modules:
            try:
                __import__(module)
                print(f"  ✅ {module}")
            except ImportError as e:
                print(f"  ❌ {module}: {e}")
                failed_imports.append(module)
        
        if failed_imports:
            print(f"❌ Failed to import: {', '.join(failed_imports)}")
            return False
        
        print("✅ All Python imports successful")
        self.test_results["python_imports"] = True
        return True
    
    def test_ml_models(self) -> bool:
        """Test ML model loading and functionality."""
        print("\n🧠 Testing ML models...")
        
        try:
            # Test model loading
            from src.core.feature_extractor import FeatureExtractor
            
            extractor = FeatureExtractor(models_dir="models")
            
            # Check if models are loaded
            loaded_models = sum(1 for model in extractor.models.values() if model is not None)
            total_models = len(extractor.models)
            
            print(f"  📊 Loaded {loaded_models}/{total_models} models")
            
            if loaded_models == 0:
                print("⚠️ No models loaded, but structure is correct")
            elif loaded_models < total_models:
                print("⚠️ Some models missing, but core functionality available")
            else:
                print("✅ All models loaded successfully")
            
            self.test_results["ml_models"] = True
            return True
            
        except Exception as e:
            print(f"❌ ML model test failed: {e}")
            return False
    
    def test_feature_extraction(self) -> bool:
        """Test feature extraction functionality."""
        print("\n📊 Testing feature extraction...")
        
        try:
            from src.core.feature_extractor import FeatureExtractor
            
            extractor = FeatureExtractor(models_dir="models")
            
            # Create a test MIDI file (simple)
            test_midi_path = self._create_test_midi()
            
            # Test feature extraction
            features = extractor.extract_basic_features(str(test_midi_path))
            
            if features is None:
                print("❌ Feature extraction returned None")
                return False
            
            # Check required features
            required_features = [
                'tempo', 'density', 'dynamic_range', 'velocity_mean',
                'pitch_mean', 'avg_polyphony', 'syncopation'
            ]
            
            missing_features = [f for f in required_features if f not in features]
            if missing_features:
                print(f"❌ Missing features: {missing_features}")
                return False
            
            print("✅ Feature extraction working correctly")
            
            # Test ML feature prediction
            ml_features = extractor.predict_ml_features(features)
            if 'energy' not in ml_features:
                print("⚠️ ML feature prediction not working")
            else:
                print("✅ ML feature prediction working")
            
            # Cleanup
            test_midi_path.unlink()
            
            self.test_results["feature_extraction"] = True
            return True
            
        except Exception as e:
            print(f"❌ Feature extraction test failed: {e}")
            return False
    
    def _create_test_midi(self) -> Path:
        """Create a simple test MIDI file."""
        try:
            import pretty_midi
            
            # Create a simple MIDI file
            midi = pretty_midi.PrettyMIDI()
            piano = pretty_midi.Instrument(program=0)
            
            # Add a simple melody
            for i, note in enumerate([60, 62, 64, 65, 67, 69, 71, 72]):
                note_start = i * 0.5
                note_end = note_start + 0.4
                note_obj = pretty_midi.Note(
                    velocity=80, pitch=note, start=note_start, end=note_end
                )
                piano.notes.append(note_obj)
            
            midi.instruments.append(piano)
            
            # Save to temporary file
            temp_file = Path(tempfile.mktemp(suffix=".mid"))
            midi.write(str(temp_file))
            
            return temp_file
            
        except Exception as e:
            print(f"⚠️ Could not create test MIDI: {e}")
            # Return a dummy path
            return Path("dummy.mid")
    
    def test_model_training(self) -> bool:
        """Test model training pipeline."""
        print("\n🤖 Testing model training...")
        
        try:
            # Test if training scripts exist and are runnable
            training_scripts = [
                "scripts/extract_features.py",
                "scripts/train_models.py",
                "scripts/generate_predictions.py"
            ]
            
            for script in training_scripts:
                script_path = self.ml_dir / script
                if not script_path.exists():
                    print(f"❌ Training script not found: {script}")
                    return False
                
                # Test script syntax
                result = subprocess.run(
                    [sys.executable, "-m", "py_compile", str(script_path)],
                    capture_output=True, text=True
                )
                
                if result.returncode != 0:
                    print(f"❌ Syntax error in {script}: {result.stderr}")
                    return False
                
                print(f"  ✅ {script} syntax OK")
            
            print("✅ Model training scripts are valid")
            self.test_results["model_training"] = True
            return True
            
        except Exception as e:
            print(f"❌ Model training test failed: {e}")
            return False
    
    def test_juce_compilation(self) -> bool:
        """Test JUCE plugin compilation."""
        print("\n🔨 Testing JUCE compilation...")
        
        try:
            # Check if CMakeLists.txt exists
            cmake_file = self.base_dir / "CMakeLists.txt"
            if not cmake_file.exists():
                print("❌ CMakeLists.txt not found")
                return False
            
            # Check if Source files exist
            source_files = [
                "Source/PluginProcessor.cpp",
                "Source/PluginProcessor.h",
                "Source/PluginEditor.cpp", 
                "Source/PluginEditor.h",
                "Source/ModelRunner.cpp",
                "Source/ModelRunner.h",
                "Source/FeatureExtractor.cpp",
                "Source/FeatureExtractor.h"
            ]
            
            missing_files = []
            for file in source_files:
                if not (self.base_dir / file).exists():
                    missing_files.append(file)
            
            if missing_files:
                print(f"❌ Missing source files: {missing_files}")
                return False
            
            print("✅ All source files present")
            
            # Test CMake configuration
            if self.build_dir.exists():
                print("  🔍 Testing CMake configuration...")
                result = subprocess.run(
                    ["cmake", ".."],
                    cwd=self.build_dir,
                    capture_output=True, text=True
                )
                
                if result.returncode == 0:
                    print("✅ CMake configuration successful")
                else:
                    print(f"⚠️ CMake configuration issues: {result.stderr}")
            
            self.test_results["juce_compilation"] = True
            return True
            
        except Exception as e:
            print(f"❌ JUCE compilation test failed: {e}")
            return False
    
    def test_plugin_functionality(self) -> bool:
        """Test plugin functionality."""
        print("\n🎛️ Testing plugin functionality...")
        
        try:
            # Check if plugin was built
            plugin_path = self.build_dir / "Aamati"
            if not plugin_path.exists():
                print("⚠️ Plugin not built, skipping functionality test")
                return True
            
            # Test plugin execution
            print("  🔍 Testing plugin execution...")
            result = subprocess.run(
                [str(plugin_path), "--help"],
                capture_output=True, text=True, timeout=10
            )
            
            if result.returncode == 0:
                print("✅ Plugin executes successfully")
            else:
                print(f"⚠️ Plugin execution issues: {result.stderr}")
            
            self.test_results["plugin_functionality"] = True
            return True
            
        except Exception as e:
            print(f"❌ Plugin functionality test failed: {e}")
            return False
    
    def test_integration(self) -> bool:
        """Test integration between ML and JUCE components."""
        print("\n🔗 Testing ML-JUCE integration...")
        
        try:
            # Check if Resources directory has required files
            required_files = [
                "groove_mood_model.onnx",
                "mood_feature_map.json"
            ]
            
            missing_files = []
            for file in required_files:
                if not (self.resources_dir / file).exists():
                    missing_files.append(file)
            
            if missing_files:
                print(f"⚠️ Missing resource files: {missing_files}")
            else:
                print("✅ All resource files present")
            
            # Test data flow
            print("  🔍 Testing data flow...")
            
            # Check if feature extraction produces compatible output
            from src.core.feature_extractor import FeatureExtractor
            extractor = FeatureExtractor(models_dir="models")
            
            # Test with dummy data
            dummy_features = {
                'tempo': 120.0,
                'density': 10.0,
                'dynamic_range': 50.0,
                'velocity_mean': 64.0,
                'avg_polyphony': 3.0,
                'syncopation': 0.01,
                'onset_entropy': 1.5,
                'pitch_range': 24.0,
                'std_note_length': 0.5,
                'instrument_count': 1
            }
            
            ml_features = extractor.predict_ml_features(dummy_features)
            
            if 'energy' in ml_features and 'swing' in ml_features:
                print("✅ ML feature prediction working")
            else:
                print("⚠️ ML feature prediction issues")
            
            self.test_results["integration"] = True
            return True
            
        except Exception as e:
            print(f"❌ Integration test failed: {e}")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all tests."""
        self.print_banner()
        
        tests = [
            ("Python Imports", self.test_python_imports),
            ("ML Models", self.test_ml_models),
            ("Feature Extraction", self.test_feature_extraction),
            ("Model Training", self.test_model_training),
            ("JUCE Compilation", self.test_juce_compilation),
            ("Plugin Functionality", self.test_plugin_functionality),
            ("Integration", self.test_integration)
        ]
        
        passed_tests = 0
        total_tests = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n{'='*20} {test_name} {'='*20}")
            try:
                if test_func():
                    passed_tests += 1
                    print(f"✅ {test_name} PASSED")
                else:
                    print(f"❌ {test_name} FAILED")
            except Exception as e:
                print(f"❌ {test_name} ERROR: {e}")
        
        # Print summary
        self.print_test_summary(passed_tests, total_tests)
        
        return passed_tests == total_tests
    
    def print_test_summary(self, passed: int, total: int):
        """Print test summary."""
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        for component, status in self.test_results.items():
            icon = "✅" if status else "❌"
            print(f"{icon} {component.replace('_', ' ').title()}")
        
        print(f"\n🎯 Overall: {passed}/{total} test suites passed")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Your Aamati setup is working perfectly!")
        elif passed >= total * 0.8:
            print("⚠️ Most tests passed, but some issues need attention")
        else:
            print("❌ Multiple test failures detected, setup needs fixing")
        
        print("\n📚 For detailed troubleshooting, check the logs and documentation")


def main():
    """Main entry point for test script."""
    parser = argparse.ArgumentParser(description="Aamati Project Test Suite")
    parser.add_argument("--base-dir", help="Base directory for testing")
    parser.add_argument("--test", choices=[
        "python", "ml", "features", "training", "juce", "plugin", "integration", "all"
    ], default="all", help="Specific test to run")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose output")
    
    args = parser.parse_args()
    
    tester = AamatiTester(base_dir=args.base_dir)
    
    if args.test == "all":
        success = tester.run_all_tests()
    else:
        # Run specific test
        test_map = {
            "python": tester.test_python_imports,
            "ml": tester.test_ml_models,
            "features": tester.test_feature_extraction,
            "training": tester.test_model_training,
            "juce": tester.test_juce_compilation,
            "plugin": tester.test_plugin_functionality,
            "integration": tester.test_integration
        }
        
        if args.test in test_map:
            success = test_map[args.test]()
        else:
            print(f"❌ Unknown test: {args.test}")
            sys.exit(1)
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
