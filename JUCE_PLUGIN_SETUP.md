# Aamati JUCE Plugin Setup Guide

This guide will help you set up the Aamati JUCE plugin with machine learning capabilities.

## Overview

The Aamati plugin is a real-time audio processor that uses machine learning to analyze audio features and apply mood-based processing. It includes:

- Real-time audio feature extraction
- ML model integration for mood prediction
- Dynamic audio processing based on predicted mood
- Modern JUCE-based UI with live feedback

## Prerequisites

1. **JUCE Framework**: Download and install JUCE from https://juce.com/
2. **ONNX Runtime**: Install ONNX Runtime for C++ (https://onnxruntime.ai/)
3. **CMake**: For building the project
4. **Python**: For setting up ML models

## Setup Instructions

### 1. Install Dependencies

#### ONNX Runtime
```bash
# On macOS with Homebrew
brew install onnxruntime

# Or download from: https://github.com/microsoft/onnxruntime/releases
```

#### JUCE
1. Download JUCE from https://juce.com/
2. Extract to a suitable location
3. Note the path for CMake configuration

### 2. Set Up ML Models

Run the setup script to copy ML models to the Resources folder:

```bash
cd Aamati
python3 setup_ml_models.py
```

This will copy the following files to the `Resources/` folder:
- `groove_mood_model.onnx` - Main mood prediction model
- `groove_mood_model.pkl` - Python model (for reference)
- Various `.joblib` files - Individual feature classification models

### 3. Configure CMake

Create a `CMakeLists.txt` in the root directory or update the existing one:

```cmake
cmake_minimum_required(VERSION 3.15)
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
```

### 4. Build the Plugin

```bash
mkdir build
cd build
cmake ..
make
```

## Plugin Features

### Audio Processing
- **High-pass and Low-pass filters**: Traditional EQ controls
- **Mid/Side processing**: Stereo image manipulation
- **ML-based processing**: Dynamic processing based on mood prediction

### Machine Learning Integration
- **Real-time feature extraction**: Analyzes audio in real-time
- **Mood prediction**: Uses trained models to predict musical mood
- **Dynamic processing**: Applies different effects based on predicted mood

### UI Controls
- **High Pass Frequency**: 20Hz - 5kHz
- **Low Pass Frequency**: 5kHz - 22kHz
- **ML Sensitivity**: 0.1x - 2.0x (controls intensity of ML processing)
- **ML Enabled**: Toggle for ML processing
- **Live Status Display**: Shows model status, predicted mood, and features

## Model Integration

The plugin uses several ML models:

1. **Main Mood Model** (`groove_mood_model.onnx`): Predicts overall mood from 5 core features
2. **Feature Classification Models**: Individual models for specific features
   - Energy classification
   - Dynamic intensity
   - Swing detection
   - Fill activity
   - Rhythmic density
   - FX character
   - Timing feel

## Real-time Feature Extraction

The plugin extracts the following features from live audio:

- **Tempo**: BPM estimation
- **Swing**: Rhythm feel analysis
- **Density**: Event density per second
- **Dynamic Range**: Amplitude variation
- **Energy**: Overall energy level
- **Velocity Mean/Std**: Amplitude statistics
- **Pitch Mean/Range**: Frequency content
- **Polyphony**: Simultaneous voice count
- **Syncopation**: Off-beat emphasis
- **Onset Entropy**: Rhythm complexity

## Mood Categories

The plugin can predict 10 different moods:

1. **Chill**: Loose, low density, soft dynamics
2. **Energetic**: Tight, high density, hard dynamics
3. **Suspenseful**: Mid timing, varied dynamics
4. **Uplifting**: High density, bright dynamics
5. **Ominous**: Tight, medium density, deep dynamics
6. **Romantic**: Loose, gentle dynamics
7. **Gritty**: Tight, high density, harsh dynamics
8. **Dreamy**: Loose, low density, light dynamics
9. **Frantic**: Random timing, very high density
10. **Focused**: Tight, consistent dynamics

## Troubleshooting

### Model Loading Issues
- Ensure `groove_mood_model.onnx` is in the Resources folder
- Check that ONNX Runtime is properly installed
- Verify the model file is not corrupted

### Build Issues
- Ensure JUCE is properly installed and configured
- Check that ONNX Runtime headers are available
- Verify CMake configuration

### Runtime Issues
- Check console output for error messages
- Ensure audio buffer size is appropriate
- Verify sample rate compatibility

## Development Notes

### Adding New Features
1. Update `GrooveFeatures` struct in `FeatureExtractor.h`
2. Implement feature calculation in `FeatureExtractor.cpp`
3. Update mood processing in `PluginProcessor.cpp`
4. Add UI controls in `PluginEditor.cpp`

### Model Updates
1. Retrain models using the Python scripts in `MLPython/`
2. Export new models to ONNX format
3. Update model loading code if input/output format changes
4. Test with the plugin

## Performance Considerations

- Feature extraction runs every audio buffer
- ML prediction runs every few buffers to avoid CPU overload
- Audio history is limited to 10 seconds to manage memory
- Consider reducing analysis frequency for lower CPU usage

## Future Enhancements

- MIDI input support for drum pattern analysis
- More sophisticated pitch detection
- Real-time model switching
- Preset management
- Advanced visualization
- Multi-channel analysis
