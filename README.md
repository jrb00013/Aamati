# 🎵 Aamati - AI-Powered Music Mood Analysis & Processing

Aamati is a comprehensive system that combines machine learning with real-time audio processing to analyze musical mood and apply intelligent effects. It consists of a Python-based ML training pipeline and a JUCE-based audio plugin for real-time processing.

## 🏗️ Project Structure

```
Aamati/
├── 📁 MLPython/                    # Machine Learning Components
│   ├── 📁 src/                     # Source code
│   │   ├── 📁 core/               # Core ML functionality
│   │   │   ├── feature_extractor.py
│   │   │   └── training_pipeline.py
│   │   ├── 📁 models/             # Model training scripts
│   │   ├── 📁 utils/              # Utility functions
│   │   └── 📁 data/               # Data processing
│   ├── 📁 scripts/                # Automation scripts
│   │   ├── automation_manager.py
│   │   ├── extract_features.py
│   │   ├── train_models.py
│   │   └── generate_predictions.py
│   ├── 📁 models/                 # Trained models
│   ├── 📁 MusicGroovesMIDI/       # MIDI training data
│   └── main.py                    # ML system entry point
├── 📁 Source/                     # JUCE Plugin Source
│   ├── PluginProcessor.cpp/h
│   ├── PluginEditor.cpp/h
│   ├── ModelRunner.cpp/h
│   └── FeatureExtractor.cpp/h
├── 📁 Resources/                  # Plugin resources
├── setup_aamati.py               # Complete setup script
├── run_aamati.py                 # Master run script
├── test_aamati.py                # Comprehensive test suite
└── CMakeLists.txt                # Build configuration
```

## 🚀 Quick Start

### 1. Complete Setup
```bash
# Run the comprehensive setup script
python3 setup_aamati.py

# This will:
# - Install all Python dependencies
# - Setup ONNX Runtime
# - Organize the ML structure
# - Create build scripts
# - Setup Resources directory
```

### 2. Train ML Models
```bash
# Interactive training (recommended for first time)
python3 run_aamati.py --interactive

# Non-interactive training (for automation)
python3 run_aamati.py --non-interactive
```

### 3. Build JUCE Plugin
```bash
# Build the plugin
python3 run_aamati.py --build-only

# Or use platform-specific scripts
./build_macos.sh    # macOS
./build_linux.sh    # Linux
```

### 4. Test Everything
```bash
# Run comprehensive test suite
python3 test_aamati.py

# Run specific tests
python3 test_aamati.py --test ml
python3 test_aamati.py --test juc
```

## 🧠 ML System Usage

### Feature Extraction
```bash
# Extract features from MIDI files
python3 MLPython/main.py --mode extract --interactive

# Non-interactive mode
python3 MLPython/main.py --mode extract --non-interactive
```

### Model Training
```bash
# Train all models
python3 MLPython/main.py --mode train

# Train specific model groups
python3 MLPython/scripts/train_models.py --models basic advanced
```

### Predictions
```bash
# Generate mood predictions
python3 MLPython/main.py --mode predict
```

### Automation
```bash
# Run complete training workflow
python3 MLPython/main.py --mode automate --workflow training

# Run data management
python3 MLPython/main.py --mode automate --workflow data-management

# Check system status
python3 MLPython/main.py --mode status
```

## 🎛️ JUCE Plugin Features

### Audio Processing
- **Real-time feature extraction**: Analyzes audio in real-time
- **Mood prediction**: Uses trained ML models to predict musical mood
- **Dynamic processing**: Applies different effects based on predicted mood
- **Traditional EQ**: High-pass and low-pass filters
- **Mid/Side processing**: Stereo image manipulation

### ML Integration
- **10 mood categories**: Chill, energetic, suspenseful, uplifting, ominous, romantic, gritty, dreamy, frantic, focused
- **Real-time analysis**: Processes audio every buffer
- **Configurable sensitivity**: User can control ML processing intensity
- **Live status display**: Shows model status and predictions

### UI Controls
- **High Pass Frequency**: 20Hz - 5kHz
- **Low Pass Frequency**: 5kHz - 22kHz
- **ML Sensitivity**: 0.1x - 2.0x
- **ML Enabled**: Toggle for ML processing
- **Live Status**: Model status, predicted mood, feature extraction status

## 🔧 Development

### Adding New Features
1. **ML Features**: Update `src/core/feature_extractor.py`
2. **Mood Processing**: Update `Source/PluginProcessor.cpp`
3. **UI Controls**: Update `Source/PluginEditor.cpp`
4. **Models**: Add new training scripts in `src/models/`

### Model Updates
1. Retrain models using Python scripts
2. Export to ONNX format
3. Update model loading code if needed
4. Test with the plugin

### Testing
```bash
# Run all tests
python3 test_aamati.py

# Run specific test categories
python3 test_aamati.py --test python
python3 test_aamati.py --test ml
python3 test_aamati.py --test juc
```

## 📊 ML Models

The system uses multiple ML models:

1. **Main Mood Model** (`groove_mood_model.onnx`): Predicts overall mood
2. **Feature Classification Models**:
   - Energy classification
   - Dynamic intensity
   - Swing detection
   - Fill activity
   - Rhythmic density
   - FX character
   - Timing feel

## 🎵 Mood Categories

| Mood | Characteristics | Tempo | Density | Energy |
|------|----------------|-------|---------|--------|
| 🧊 Chill | Loose, minimal, mellow | 60-115 | 2-10 | 2-5 |
| ⚡ Energetic | Tight, aggressive, driving | 120-175 | 20-40 | 13-15 |
| 🕳️ Suspenseful | Tense, minor scales, stabs | 75-125 | 6-18 | 6-9 |
| 🌅 Uplifting | Bright, major harmonies | 100-160 | 10-26 | 7-13 |
| 🌑 Ominous | Brooding, dark, sparse | 55-100 | 4-12 | 5-8 |
| 💘 Romantic | Flowing, expressive, warm | 60-125 | 10-20 | 5-9 |
| 🪓 Gritty | Dirty, mechanical, raw | 135-180 | 15-33 | 10-14 |
| 💭 Dreamy | Reverb-heavy, washed | 70-110 | 5-15 | 5-8 |
| 🌀 Frantic | Chaotic, rapid, wild | 160-250 | 22-40 | 14-17 |
| 🎯 Focused | Steady, repetitive, precise | 83-135 | 8-22 | 8-11 |

## 🛠️ Troubleshooting

### Common Issues

1. **Models not loading**: Check if models exist in `Resources/` folder
2. **Build failures**: Ensure JUCE and ONNX Runtime are properly installed
3. **Import errors**: Run `python3 setup_aamati.py` to install dependencies
4. **Plugin not working**: Check console output for error messages

### Debug Mode
```bash
# Enable verbose output
python3 run_aamati.py --verbose
python3 test_aamati.py --verbose
```

### Logs
Check logs in `MLPython/logs/` for detailed information about ML operations.

## 📚 Documentation

- **Setup Guide**: `JUCE_PLUGIN_SETUP.md`
- **ML Documentation**: `MLPython/README.md`
- **API Reference**: See docstrings in source files

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- JUCE framework for audio plugin development
- ONNX Runtime for model inference
- Pretty MIDI for MIDI file processing
- Scikit-learn for machine learning
- All contributors and testers

---

**🎵 Happy creating with Aamati! 🎵**