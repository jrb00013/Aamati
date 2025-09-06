# 🎵 Aamati Complete Usage Guide

This is your comprehensive guide to using the entire Aamati system - from setup to advanced usage.

## 🚀 Quick Start (5 Minutes)

### 1. Initial Setup
```bash
# Clone and setup everything
git clone <your-repo> aamati
cd aamati

# Install dependencies and setup
python3 setup_aamati.py

# Run complete pipeline
python3 run_aamati.py --full-pipeline
```

### 2. Test the System
```bash
# Test everything
python3 test_aamati.py

# Build and test JUCE plugin
python3 run_aamati.py --build-only
```

## 📁 Project Structure Overview

```
Aamati/
├── 🎵 MLPython/                    # Machine Learning System
│   ├── extract_groove_features.py  # Main feature extraction
│   ├── train_models.py             # Model training
│   ├── predict_groove_mood.py      # Mood prediction
│   ├── main.py                     # ML system entry point
│   ├── data/                       # Training data
│   ├── models/                     # Trained models
│   └── scripts/                    # Automation scripts
├── 🎛️ Source/                      # JUCE Plugin Source
│   ├── PluginProcessor.cpp         # Audio processing
│   ├── PluginEditor.cpp            # UI components
│   ├── FeatureExtractor.cpp        # Feature extraction
│   └── ModelRunner.cpp             # ML model integration
├── 📦 Resources/                   # Plugin resources
│   └── groove_mood_model.onnx      # Main ML model
├── 🔧 setup_aamati.py              # Complete setup
├── 🚀 run_aamati.py                # Master run script
└── 🧪 test_aamati.py               # Comprehensive testing
```

## 🎯 Usage Scenarios

### Scenario 1: First Time Setup
```bash
# 1. Complete system setup
python3 setup_aamati.py

# 2. Add your MIDI files
cp your_midi_files/*.mid MLPython/MusicGroovesMIDI/TrainingMIDIs/

# 3. Train the system
python3 run_aamati.py --full-pipeline

# 4. Build the plugin
python3 run_aamati.py --build-only
```

### Scenario 2: Adding New Training Data
```bash
# 1. Add new MIDI files
cp new_midi_files/*.mid MLPython/MusicGroovesMIDI/TrainingMIDIs/

# 2. Extract features from new data
python3 MLPython/main.py --mode extract --interactive

# 3. Retrain models
python3 MLPython/train_models.py

# 4. Update plugin
python3 setup_ml_models.py
```

### Scenario 3: Batch Processing
```bash
# Process large datasets without interaction
python3 MLPython/main.py --mode full-pipeline --non-interactive
```

### Scenario 4: Development/Testing
```bash
# Test individual components
python3 test_aamati.py --component ml
python3 test_aamati.py --component juce
python3 test_aamati.py --component integration
```

## 🎵 ML System Usage

### Feature Extraction

#### Interactive Mode (Recommended)
```bash
cd MLPython
python3 extract_groove_features.py --interactive
```

**What you'll do:**
1. System processes each MIDI file
2. You label each file with primary/secondary mood
3. Features are extracted and saved
4. Files are moved to processed folder

#### Batch Mode
```bash
python3 extract_groove_features.py --non-interactive --midi-folder MusicGroovesMIDI/TrainingMIDIs
```

#### Custom Parameters
```bash
python3 extract_groove_features.py \
  --midi-folder /path/to/your/midis \
  --output-csv my_features.csv \
  --log-csv my_log.csv \
  --interactive
```

### Model Training

#### Train All Models
```bash
python3 train_models.py
```

#### Train Specific Models
```bash
# Train only classification models
python3 train_models.py --models classification

# Train only main mood model
python3 train_models.py --models main
```

#### Advanced Training
```bash
# Train with verbose output
python3 train_models.py --verbose

# Train specific models
python3 ModelClassificationScripts/energy_randomforest.py
python3 ModelClassificationScripts/swing_randomforest.py
```

### Mood Prediction

#### Predict from CSV
```bash
python3 predict_groove_mood.py --csv-file groove_features_log_for_pred.csv
```

#### Predict Single File
```bash
python3 -c "
from src.core.extract_groove_features import extract_features
from predict_groove_mood import predict_mood_from_features, load_prediction_models

# Extract features
features = extract_features('path/to/your/file.mid')
models = load_prediction_models()
mood = predict_mood_from_features(features, models)
print(f'Predicted mood: {mood}')
"
```

### Data Management

#### Copy Log to Prediction File
```bash
python3 main.py --mode copy-log
```

#### Clear Current Log
```bash
python3 main.py --mode clear-log
```

#### Full Data Pipeline
```bash
# Complete data processing pipeline
python3 main.py --mode full-pipeline --interactive
```

## 🎛️ JUCE Plugin Usage

### Building the Plugin

#### Build All Formats
```bash
python3 run_aamati.py --build-only
```

#### Build Specific Format
```bash
# Build VST3
python3 run_aamati.py --build-only --format vst3

# Build AU (macOS)
python3 run_aamati.py --build-only --format au

# Build Standalone
python3 run_aamati.py --build-only --format standalone
```

### Plugin Parameters

The Aamati plugin has these controls:

| Parameter | Range | Description |
|-----------|-------|-------------|
| **High Pass** | 20-20000 Hz | High-pass filter frequency |
| **Low Pass** | 20-20000 Hz | Low-pass filter frequency |
| **ML Enabled** | On/Off | Enable machine learning processing |
| **ML Sensitivity** | 0-100% | How much ML affects the audio |

### Real-Time Usage

1. **Load the plugin** in your DAW
2. **Enable ML processing** (ML Enabled = On)
3. **Adjust sensitivity** (start with 50%)
4. **Play MIDI** - the plugin will:
   - Extract features from incoming MIDI
   - Predict mood in real-time
   - Apply mood-appropriate audio processing
   - Display current mood and features

### Plugin UI Features

- **Real-time mood display** - Shows current predicted mood
- **Feature visualization** - Live feature extraction display
- **Model status** - Shows if ML model is loaded
- **Processing indicators** - Visual feedback for ML processing

## 🔧 Advanced Usage

### Custom Model Training

#### Train with Custom Data
```bash
# 1. Prepare your data
cp your_data/*.mid MLPython/MusicGroovesMIDI/TrainingMIDIs/

# 2. Extract features
python3 MLPython/extract_groove_features.py --interactive

# 3. Train models
python3 MLPython/train_models.py

# 4. Export for plugin
python3 setup_ml_models.py
```

#### Custom Feature Extraction
```python
# Custom extraction script
from src.core.extract_groove_features import extract_features

# Extract from specific file
features = extract_features('path/to/file.mid')
print(f"Tempo: {features['tempo']}")
print(f"Swing: {features['swing']}")
print(f"Density: {features['density']}")
```

### Batch Processing

#### Process Multiple Folders
```bash
# Process different folders
for folder in folder1 folder2 folder3; do
    python3 MLPython/extract_groove_features.py \
        --midi-folder "MusicGroovesMIDI/$folder" \
        --output-csv "features_$folder.csv" \
        --non-interactive
done
```

#### Automated Retraining
```bash
# Set up automated retraining
crontab -e
# Add: 0 2 * * * cd /path/to/aamati && python3 run_aamati.py --full-pipeline --non-interactive
```

### Integration with Other Tools

#### Export Features for Analysis
```python
import pandas as pd

# Load features
df = pd.read_csv('MLPython/groove_features_log_for_pred.csv')

# Export for external analysis
df.to_csv('exported_features.csv', index=False)

# Create summary statistics
summary = df.groupby('primary_mood').agg({
    'tempo': ['mean', 'std'],
    'energy': ['mean', 'std'],
    'density': ['mean', 'std']
})
print(summary)
```

#### Custom Mood Categories
```python
# Modify mood labels in src/utils/mood_mappings.py
mood_labels = [
    "your_custom_mood_1",
    "your_custom_mood_2",
    # ... etc
]
```

## 🧪 Testing and Validation

### Run All Tests
```bash
python3 test_aamati.py
```

### Test Individual Components
```bash
# Test ML system
python3 test_aamati.py --component ml

# Test JUCE plugin
python3 test_aamati.py --component juce

# Test integration
python3 test_aamati.py --component integration
```

### Performance Testing
```bash
# Test with large dataset
python3 test_aamati.py --performance-test

# Benchmark feature extraction
python3 test_aamati.py --benchmark
```

## 📊 Monitoring and Debugging

### View Logs
```bash
# ML system logs
tail -f MLPython/groove_features_log.csv

# Training logs
ls MLPython/ModelClassificationScripts/models/*.txt

# Plugin logs (if available)
tail -f ~/Library/Logs/Aamati.log
```

### Debug Mode
```bash
# Enable debug output
python3 MLPython/extract_groove_features.py --interactive --verbose
python3 MLPython/train_models.py --verbose
```

### Performance Monitoring
```bash
# Monitor system resources
python3 -c "
import psutil
print(f'CPU: {psutil.cpu_percent()}%')
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'Disk: {psutil.disk_usage(\"/\").percent}%')
"
```

## 🚨 Troubleshooting

### Common Issues

#### 1. "No MIDI files found"
```bash
# Check file locations
ls -la MLPython/MusicGroovesMIDI/TrainingMIDIs/
find . -name "*.mid" -type f
```

#### 2. "Model training failed"
```bash
# Check data quality
python3 -c "
import pandas as pd
df = pd.read_csv('MLPython/groove_features_log_for_pred.csv')
print(f'Data points: {len(df)}')
print(f'Missing values: {df.isnull().sum().sum()}')
print(f'Mood distribution: {df[\"primary_mood\"].value_counts()}')
"
```

#### 3. "Plugin not loading"
```bash
# Check model files
ls -la Resources/
ls -la MLPython/groove_mood_model.*

# Rebuild plugin
python3 run_aamati.py --build-only --clean
```

#### 4. "Memory errors"
```bash
# Process smaller batches
python3 MLPython/extract_groove_features.py --non-interactive --batch-size 10
```

### Getting Help

#### Check System Status
```bash
python3 test_aamati.py --status
```

#### Generate Debug Report
```bash
python3 test_aamati.py --debug-report
```

#### View Configuration
```bash
python3 -c "
import sys
print(f'Python version: {sys.version}')
print(f'Platform: {sys.platform}')
"
```

## 📚 Best Practices

### 1. Data Management
- **Organize MIDI files** by genre/mood
- **Keep backups** of training data
- **Document your labeling** decisions
- **Regular cleanup** of processed files

### 2. Model Training
- **Start small** with 50-100 files
- **Validate regularly** on new data
- **Monitor performance** metrics
- **Keep model versions** for comparison

### 3. Plugin Usage
- **Test with different** MIDI sources
- **Adjust sensitivity** based on content
- **Monitor CPU usage** during real-time processing
- **Keep models updated** with new training data

### 4. System Maintenance
- **Regular updates** of dependencies
- **Clean up logs** periodically
- **Monitor disk space** usage
- **Backup configurations** and models

## 🎯 Performance Optimization

### For Large Datasets
```bash
# Use non-interactive mode
python3 MLPython/main.py --mode full-pipeline --non-interactive

# Process in batches
python3 MLPython/extract_groove_features.py --batch-size 50 --non-interactive
```

### For Real-Time Processing
```bash
# Optimize plugin settings
# - Lower ML sensitivity for better performance
# - Use fewer features for faster processing
# - Enable only necessary audio processing
```

### For Development
```bash
# Use smaller datasets for testing
python3 MLPython/extract_groove_features.py --max-files 10 --interactive
```

## 🔄 Workflow Examples

### Daily Workflow
```bash
# 1. Add new MIDI files
cp new_files/*.mid MLPython/MusicGroovesMIDI/TrainingMIDIs/

# 2. Extract features
python3 MLPython/extract_groove_features.py --interactive

# 3. Train models
python3 MLPython/train_models.py

# 4. Update plugin
python3 setup_ml_models.py
```

### Weekly Workflow
```bash
# 1. Full system test
python3 test_aamati.py

# 2. Performance check
python3 test_aamati.py --performance-test

# 3. Clean up old data
python3 MLPython/main.py --mode clear-log
```

### Monthly Workflow
```bash
# 1. Complete retraining
python3 run_aamati.py --full-pipeline

# 2. Update all models
python3 MLPython/train_models.py

# 3. Rebuild plugin
python3 run_aamati.py --build-only --clean
```

---

**🎵 Welcome to Aamati! 🎵**

*This guide covers everything you need to know about using the Aamati system. For specific questions, check the troubleshooting section or refer to the individual component documentation.*
