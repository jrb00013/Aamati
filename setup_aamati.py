#!/usr/bin/env python3
"""
Comprehensive setup script for the entire Aamati project.
Sets up both ML Python side and JUCE plugin side.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from typing import List, Dict, Optional
import json


class AamatiSetup:
    """Main setup class for the Aamati project."""
    
    def __init__(self, base_dir: str = None):
        """Initialize setup manager."""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        
        # Directories
        self.ml_dir = self.base_dir / "MLPython"
        self.juce_dir = self.base_dir / "Source"
        self.resources_dir = self.base_dir / "Resources"
        
        # Setup status
        self.setup_status = {
            "python_deps": False,
            "onnx_runtime": False,
            "juce": False,
            "models": False,
            "resources": False
        }
    
    def print_banner(self):
        """Print setup banner."""
        print("🎵" + "=" * 60 + "🎵")
        print("           AAMATI PROJECT SETUP")
        print("    AI-Powered Music Mood Analysis & Processing")
        print("🎵" + "=" * 60 + "🎵")
        print()
    
    def check_python_version(self) -> bool:
        """Check Python version compatibility."""
        print("🐍 Checking Python version...")
        
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required. Current version:", sys.version)
            return False
        
        print(f"✅ Python {sys.version.split()[0]} detected")
        return True
    
    def install_python_dependencies(self) -> bool:
        """Install Python dependencies."""
        print("\n📦 Installing Python dependencies...")
        
        requirements = [
            "pandas>=1.3.0",
            "numpy>=1.21.0",
            "scikit-learn>=1.0.0",
            "joblib>=1.0.0",
            "torch>=1.9.0",
            "skl2onnx>=1.10.0",
            "pretty_midi>=0.2.9",
            "scipy>=1.7.0",
            "matplotlib>=3.4.0",
            "seaborn>=0.11.0"
        ]
        
        try:
            for req in requirements:
                print(f"  Installing {req}...")
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", req],
                    capture_output=True,
                    text=True,
                    check=True
                )
            
            print("✅ Python dependencies installed successfully")
            self.setup_status["python_deps"] = True
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Python dependencies: {e}")
            return False
    
    def install_onnx_runtime(self) -> bool:
        """Install ONNX Runtime for the current platform."""
        print("\n🤖 Installing ONNX Runtime...")
        
        try:
            # Install ONNX Runtime Python package
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "onnxruntime"],
                capture_output=True,
                text=True,
                check=True
            )
            
            print("✅ ONNX Runtime Python package installed")
            
            # For JUCE plugin, we need the C++ libraries
            if self.system == "darwin":  # macOS
                self._install_onnx_runtime_macos()
            elif self.system == "linux":
                self._install_onnx_runtime_linux()
            elif self.system == "windows":
                self._install_onnx_runtime_windows()
            else:
                print(f"⚠️ Unsupported platform: {self.system}")
                return False
            
            self.setup_status["onnx_runtime"] = True
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install ONNX Runtime: {e}")
            return False
    
    def _install_onnx_runtime_macos(self):
        """Install ONNX Runtime for macOS."""
        print("  Installing ONNX Runtime for macOS...")
        
        # Try Homebrew first
        try:
            result = subprocess.run(
                ["brew", "install", "onnxruntime"],
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ ONNX Runtime installed via Homebrew")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️ Homebrew not found, please install ONNX Runtime manually")
            print("   Download from: https://github.com/microsoft/onnxruntime/releases")
    
    def _install_onnx_runtime_linux(self):
        """Install ONNX Runtime for Linux."""
        print("  Installing ONNX Runtime for Linux...")
        
        # Try apt first
        try:
            result = subprocess.run(
                ["sudo", "apt", "update"],
                capture_output=True,
                text=True,
                check=True
            )
            result = subprocess.run(
                ["sudo", "apt", "install", "-y", "libonnxruntime-dev"],
                capture_output=True,
                text=True,
                check=True
            )
            print("✅ ONNX Runtime installed via apt")
        except subprocess.CalledProcessError:
            print("⚠️ apt installation failed, please install ONNX Runtime manually")
            print("   Download from: https://github.com/microsoft/onnxruntime/releases")
    
    def _install_onnx_runtime_windows(self):
        """Install ONNX Runtime for Windows."""
        print("  Installing ONNX Runtime for Windows...")
        print("⚠️ Please install ONNX Runtime manually for Windows")
        print("   Download from: https://github.com/microsoft/onnxruntime/releases")
    
    def setup_juce(self) -> bool:
        """Setup JUCE framework."""
        print("\n🎛️ Setting up JUCE framework...")
        
        # Check if JUCE is already available
        juce_path = self._find_juce_path()
        if juce_path:
            print(f"✅ JUCE found at: {juce_path}")
            self.setup_status["juce"] = True
            return True
        
        print("⚠️ JUCE not found. Please install JUCE manually:")
        print("   1. Download from: https://juce.com/")
        print("   2. Extract to a suitable location")
        print("   3. Set JUCE_PATH environment variable")
        print("   4. Or place JUCE in /opt/JUCE (Linux/macOS)")
        
        return False
    
    def _find_juce_path(self) -> Optional[str]:
        """Find JUCE installation path."""
        # Check environment variable
        juce_path = os.environ.get("JUCE_PATH")
        if juce_path and os.path.exists(juce_path):
            return juce_path
        
        # Check common locations
        common_paths = [
            "/opt/JUCE",
            "/usr/local/JUCE",
            "C:\\JUCE",
            "C:\\Program Files\\JUCE"
        ]
        
        for path in common_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def setup_ml_models(self) -> bool:
        """Setup ML models and organize structure."""
        print("\n🧠 Setting up ML models...")
        
        try:
            # Create organized directory structure
            self._create_ml_structure()
            
            # Copy models to organized structure
            self._copy_models()
            
            # Create __init__.py files
            self._create_init_files()
            
            print("✅ ML models structure created")
            self.setup_status["models"] = True
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup ML models: {e}")
            return False
    
    def _create_ml_structure(self):
        """Create organized ML directory structure."""
        directories = [
            "MLPython/src/core",
            "MLPython/src/models", 
            "MLPython/src/utils",
            "MLPython/src/data",
            "MLPython/scripts",
            "MLPython/tests",
            "MLPython/config",
            "MLPython/logs",
            "Resources"
        ]
        
        for dir_path in directories:
            full_path = self.base_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
    
    def _copy_models(self):
        """Copy models to organized structure."""
        # Copy existing models to new structure
        models_source = self.ml_dir / "ModelClassificationScripts" / "models"
        models_dest = self.ml_dir / "models"
        
        if models_source.exists():
            for model_file in models_source.glob("*.joblib"):
                shutil.copy2(model_file, models_dest)
                print(f"  Copied {model_file.name}")
    
    def _create_init_files(self):
        """Create __init__.py files for Python packages."""
        init_files = [
            "MLPython/src/__init__.py",
            "MLPython/src/core/__init__.py",
            "MLPython/src/models/__init__.py",
            "MLPython/src/utils/__init__.py",
            "MLPython/src/data/__init__.py"
        ]
        
        for init_file in init_files:
            file_path = self.base_dir / init_file
            if not file_path.exists():
                file_path.write_text("# Aamati ML Package\n")
    
    def setup_resources(self) -> bool:
        """Setup Resources directory for JUCE plugin."""
        print("\n📁 Setting up Resources directory...")
        
        try:
            # Create Resources directory
            self.resources_dir.mkdir(exist_ok=True)
            
            # Copy models to Resources
            self._copy_models_to_resources()
            
            print("✅ Resources directory setup complete")
            self.setup_status["resources"] = True
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup Resources: {e}")
            return False
    
    def _copy_models_to_resources(self):
        """Copy models to Resources directory for JUCE plugin."""
        # Copy ONNX model
        onnx_source = self.ml_dir / "groove_mood_model.onnx"
        if onnx_source.exists():
            shutil.copy2(onnx_source, self.resources_dir)
            print(f"  Copied {onnx_source.name}")
        
        # Copy other model files
        models_source = self.ml_dir / "models"
        if models_source.exists():
            for model_file in models_source.glob("*.joblib"):
                shutil.copy2(model_file, self.resources_dir)
                print(f"  Copied {model_file.name}")
    
    def create_cmake_config(self) -> bool:
        """Create CMake configuration for JUCE plugin."""
        print("\n🔧 Creating CMake configuration...")
        
        cmake_content = '''cmake_minimum_required(VERSION 3.15)
project(Aamati)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find JUCE
find_package(PkgConfig REQUIRED)
pkg_check_modules(JUCE REQUIRED juce)

# Find ONNX Runtime
find_package(onnxruntime REQUIRED)

# Include directories
include_directories(${JUCE_INCLUDE_DIRS})
include_directories(${onnxruntime_INCLUDE_DIRS})

# Add source files
set(SOURCES
    Source/PluginProcessor.cpp
    Source/PluginProcessor.h
    Source/PluginEditor.cpp
    Source/PluginEditor.h
    Source/ModelRunner.cpp
    Source/ModelRunner.h
    Source/FeatureExtractor.cpp
    Source/FeatureExtractor.h
)

# Create the plugin executable
add_executable(Aamati ${SOURCES})

# Link libraries
target_link_libraries(Aamati ${JUCE_LIBRARIES})
target_link_libraries(Aamati ${onnxruntime_LIBRARIES})

# Copy Resources folder
file(COPY Resources DESTINATION ${CMAKE_BINARY_DIR})
'''
        
        cmake_file = self.base_dir / "CMakeLists.txt"
        cmake_file.write_text(cmake_content)
        print("✅ CMakeLists.txt created")
        return True
    
    def create_build_scripts(self) -> bool:
        """Create build scripts for different platforms."""
        print("\n🔨 Creating build scripts...")
        
        # Create build script for current platform
        if self.system == "darwin":
            self._create_macos_build_script()
        elif self.system == "linux":
            self._create_linux_build_script()
        elif self.system == "windows":
            self._create_windows_build_script()
        
        return True
    
    def _create_macos_build_script(self):
        """Create macOS build script."""
        script_content = '''#!/bin/bash
# macOS Build Script for Aamati

set -e

echo "🍎 Building Aamati for macOS..."

# Create build directory
mkdir -p build
cd build

# Configure with CMake
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build
make -j$(sysctl -n hw.ncpu)

echo "✅ Build complete! Plugin available in build/"
'''
        
        script_file = self.base_dir / "build_macos.sh"
        script_file.write_text(script_content)
        script_file.chmod(0o755)
        print("✅ macOS build script created")
    
    def _create_linux_build_script(self):
        """Create Linux build script."""
        script_content = '''#!/bin/bash
# Linux Build Script for Aamati

set -e

echo "🐧 Building Aamati for Linux..."

# Create build directory
mkdir -p build
cd build

# Configure with CMake
cmake .. -DCMAKE_BUILD_TYPE=Release

# Build
make -j$(nproc)

echo "✅ Build complete! Plugin available in build/"
'''
        
        script_file = self.base_dir / "build_linux.sh"
        script_file.write_text(script_content)
        script_file.chmod(0o755)
        print("✅ Linux build script created")
    
    def _create_windows_build_script(self):
        """Create Windows build script."""
        script_content = '''@echo off
REM Windows Build Script for Aamati

echo Building Aamati for Windows...

REM Create build directory
if not exist build mkdir build
cd build

REM Configure with CMake
cmake .. -DCMAKE_BUILD_TYPE=Release

REM Build
cmake --build . --config Release

echo Build complete! Plugin available in build/
pause
'''
        
        script_file = self.base_dir / "build_windows.bat"
        script_file.write_text(script_content)
        print("✅ Windows build script created")
    
    def print_setup_summary(self):
        """Print setup summary."""
        print("\n📊 Setup Summary")
        print("=" * 40)
        
        for component, status in self.setup_status.items():
            icon = "✅" if status else "❌"
            print(f"{icon} {component.replace('_', ' ').title()}")
        
        print("\n🎵 Next Steps:")
        print("1. Train your ML models: python3 MLPython/scripts/extract_features.py")
        print("2. Build the JUCE plugin: ./build_macos.sh (or build_linux.sh)")
        print("3. Test the plugin in your DAW")
        print("\n📚 For detailed instructions, see JUCE_PLUGIN_SETUP.md")
    
    def run_setup(self):
        """Run the complete setup process."""
        self.print_banner()
        
        # Check Python version
        if not self.check_python_version():
            sys.exit(1)
        
        # Install dependencies
        if not self.install_python_dependencies():
            sys.exit(1)
        
        if not self.install_onnx_runtime():
            sys.exit(1)
        
        # Setup components
        self.setup_juce()
        self.setup_ml_models()
        self.setup_resources()
        
        # Create build configuration
        self.create_cmake_config()
        self.create_build_scripts()
        
        # Print summary
        self.print_setup_summary()


def main():
    """Main entry point for setup script."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Aamati Project Setup")
    parser.add_argument("--base-dir", help="Base directory for setup")
    parser.add_argument("--skip-python", action="store_true", 
                       help="Skip Python dependency installation")
    parser.add_argument("--skip-onnx", action="store_true",
                       help="Skip ONNX Runtime installation")
    parser.add_argument("--skip-juce", action="store_true",
                       help="Skip JUCE setup")
    
    args = parser.parse_args()
    
    setup = AamatiSetup(base_dir=args.base_dir)
    
    if args.skip_python:
        setup.setup_status["python_deps"] = True
    if args.skip_onnx:
        setup.setup_status["onnx_runtime"] = True
    if args.skip_juce:
        setup.setup_status["juce"] = True
    
    setup.run_setup()


if __name__ == "__main__":
    main()
