# Aamati Complete Usage Guide

## 🎵 The Ultimate AI-Powered Music Production Suite

Aamati is a revolutionary JUCE audio plugin that combines machine learning, real-time MIDI processing, and AI-driven music generation to create an unparalleled music production experience.

## 🚀 Quick Start

### 1. Setup Everything
```bash
# Navigate to the Aamati directory
cd /Users/clairehudson/Documents/Aamati_ws/Aamati

# Run the complete setup
python3 setup_aamati.py

# Or run the automated setup script
./startAamati.sh
```

### 2. Train Your Models
```bash
# Run the complete ML pipeline
python3 run_aamati.py --full-pipeline

# Or run just ML training
python3 run_aamati.py --ml-only
```

### 3. Build and Run the Plugin
```bash
# Build the JUCE plugin
python3 run_aamati.py --build-only

# Or build manually
cd Aamati
cmake -B build -S . -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release
```

## 🎛️ Plugin Features

### Core Features
- **Real-time Mood Analysis**: AI-powered mood detection from MIDI input
- **Emotional Optimization**: Adjust MIDI to make listeners "feel" the intended emotion
- **Dynamic Groove Shaping**: Make rhythm feel more human and natural
- **Instrumentation Guidance**: AI-recommended instrument selection
- **Melodic Contour Adaptation**: Alter melodies to match mood
- **Harmonic Density Control**: Control chord richness and emotional impact

### Advanced AI Features
- **AI MIDI Generation**: Generate new MIDI content based on mood analysis
- **Real-time Key/Tempo Detection**: Automatic musical analysis
- **Visual Analyzer**: AI-driven real-time visualization
- **Mood Remixer**: Transform existing MIDI based on mood
- **AI Mastering Tools**: Intelligent audio mastering
- **Groove Humanizer**: Add human feel to mechanical sequences
- **Dynamic Range Balancer**: Balance energy levels automatically

## 🎨 Modern UI

The plugin features a stunning modern interface with:
- **Black, White, and Gold Theme**: Professional Aamati branding
- **Upload MIDI**: Drag and drop MIDI files for analysis
- **Mood Display**: Real-time primary and secondary mood analysis
- **Feature Buttons**: Easy access to all advanced features
- **Visual Feedback**: Progress bars, confidence indicators, and tags
- **Download Reports**: Export analysis results

## 🧠 Machine Learning Pipeline

### 1. Feature Extraction
```bash
# Extract features from MIDI files
python3 MLPython/extract_groove_features.py --midi-folder MusicGroovesMIDI/TrainingMIDIs

# With custom parameters
python3 MLPython/extract_groove_features.py \
    --midi-folder /path/to/midi/files \
    --batch-size 25 \
    --max-files 100 \
    --interactive
```

### 2. Model Training
```bash
# Train all models
python3 MLPython/train_models.py

# Train specific model
python3 MLPython/optimized_mood_classifier.py
```

### 3. Prediction
```bash
# Predict mood from features
python3 MLPython/predict_groove_mood.py --csv-file data/csv/groove_features_log_for_pred.csv
```

## 📊 Data Management

### CSV Files
- `data/csv/groove_features_log.csv`: Current session data (cleared each time)
- `data/csv/groove_features_log_for_pred.csv`: Accumulated training data
- `data/csv/current_groove_features.csv`: Latest extracted features

### Data Flow
1. Extract features → `groove_features_log.csv`
2. Copy to prediction file → `groove_features_log_for_pred.csv`
3. Clear log file → `groove_features_log.csv` (ready for next session)

### Automation Scripts
```bash
# Copy log to prediction file
python3 MLPython/scripts/copy_groove_features.py

# Clear log file
python3 MLPython/scripts/reset_groove_features.py

# Run full automation
python3 MLPython/scripts/automation_manager.py
```

## 🔧 Configuration

### Environment Variables
```bash
export AAMATI_ML_MODELS_PATH="/path/to/models"
export AAMATI_LOG_LEVEL="INFO"
export AAMATI_MAX_BATCH_SIZE="50"
```

### Configuration Files
- `MLPython/config/settings.json`: ML pipeline settings
- `MLPython/config/mood_mappings.json`: Mood definitions
- `Aamati/Resources/`: Plugin resources and models

## 🎵 Usage Examples

### 1. Basic Mood Analysis
1. Load a MIDI file into your DAW
2. Insert the Aamati plugin
3. Play the MIDI - watch real-time mood analysis
4. Adjust parameters to see mood changes

### 2. Emotional Optimization
1. Set your target mood (e.g., "energetic")
2. Enable Emotional Optimization
3. Adjust energy and tension parameters
4. Hear the MIDI transform to match the mood

### 3. AI MIDI Generation
1. Set generation context (mood, tempo, key)
2. Click "Generate MIDI"
3. Choose length and complexity
4. Export generated MIDI

### 4. Groove Shaping
1. Enable Groove Shaping
2. Adjust humanization and swing
3. Set accent patterns
4. Hear more natural, human-like rhythm

## 🧪 Testing and Validation

### Run Integration Tests
```bash
# Run all tests
python3 run_aamati.py --test-only

# Run specific test suite
python3 test_aamati.py --suite mood_analysis
python3 test_aamati.py --suite feature_extraction
python3 test_aamati.py --suite model_training
```

### System Health Check
```bash
# Check system status
python3 system_health.py

# Monitor in real-time
python3 system_health.py --monitor
```

## 📈 Performance Optimization

### ML Pipeline
- Use `--batch-size` parameter for memory management
- Enable `--non-interactive` mode for faster processing
- Use `--max-files` to limit processing scope

### Plugin Performance
- Adjust buffer size in your DAW
- Use Release build for production
- Monitor CPU usage with system health tools

## 🐛 Troubleshooting

### Common Issues

#### 1. Model Loading Failed
```bash
# Check model files exist
ls -la Aamati/Resources/*.onnx
ls -la MLPython/models/trained/*.joblib

# Re-export models
python3 setup_ml_models.py
```

#### 2. Feature Extraction Errors
```bash
# Check MIDI file format
file /path/to/midi/file.mid

# Verify dependencies
pip install -r MLPython/requirements.txt
```

#### 3. Plugin Not Loading
```bash
# Check JUCE build
cd Aamati
cmake --build build --config Release

# Verify plugin format
ls -la build/Aamati_artefacts/Release/
```

### Debug Mode
```bash
# Enable debug logging
export AAMATI_LOG_LEVEL="DEBUG"
python3 run_aamati.py --verbose
```

## 📚 Advanced Usage

### Custom Mood Definitions
Edit `MLPython/config/mood_mappings.json`:
```json
{
  "custom_mood": {
    "energy": 0.8,
    "tension": 0.6,
    "complexity": 0.7,
    "danceability": 0.9
  }
}
```

### Custom Feature Extraction
```python
# Add custom features in MLPython/src/core/extract_groove_features.py
def extract_custom_feature(midi_data):
    # Your custom feature extraction logic
    return feature_value
```

### Plugin Parameter Automation
```python
# Automate plugin parameters via MIDI CC
# CC 1: Emotional Optimization Intensity
# CC 2: Groove Shaping Amount
# CC 3: AI Generation Level
```

## 🎯 Best Practices

### 1. Training Data
- Use diverse MIDI files for better model accuracy
- Include various genres and styles
- Ensure proper mood labeling

### 2. Real-time Processing
- Start with lower sensitivity settings
- Gradually increase complexity
- Monitor CPU usage

### 3. Workflow Integration
- Use Aamati early in your production process
- Experiment with different mood combinations
- Save successful presets

## 📞 Support

### Documentation
- `README.md`: Project overview
- `TRAINING_GUIDE.md`: Detailed training instructions
- `INTEGRATION_TESTING_GUIDE.md`: Testing procedures
- `PROJECT_SUMMARY.md`: Complete feature list

### Logs
- `data/logs/`: Application logs
- `MLPython/logs/`: ML pipeline logs
- `Aamati/logs/`: Plugin logs

### Performance Monitoring
```bash
# Monitor system resources
python3 system_health.py --monitor --interval 5

# Check plugin performance
python3 test_aamati.py --suite performance
```

## 🚀 Future Features

- **Cloud Integration**: Upload models and presets to cloud
- **Collaborative Features**: Share mood analyses with team
- **Advanced Visualization**: 3D mood space visualization
- **Mobile App**: Companion app for mobile devices
- **API Integration**: Connect with other music software

---

## 🎉 Ready to Create Amazing Music?

Aamati is your gateway to AI-powered music production. With its advanced machine learning capabilities and intuitive interface, you can create music that truly resonates with emotions and connects with listeners.

**Start your journey today:**
```bash
python3 run_aamati.py --full-pipeline
```

*Happy creating! 🎵✨*