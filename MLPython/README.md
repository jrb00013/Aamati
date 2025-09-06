# 🎵 Aamati ML Python System

This is the machine learning component of the Aamati project, responsible for training mood classification models and extracting musical features from MIDI files.

## 📁 Project Structure

```
MLPython/
├── extract_groove_features.py          # Main feature extraction script
├── train_models.py                     # Model training script
├── predict_groove_mood.py              # Mood prediction script
├── main.py                             # Main entry point
├── MachineLearningModel.py             # Main mood model training
├── src/
│   └── core/
│       └── extract_groove_features.py  # Core extraction engine
├── scripts/
│   ├── copy_groove_features.py         # Copy log to pred
│   └── reset_groove_features.py        # Clear log file
├── ModelClassificationScripts/
│   ├── models/                         # Trained .joblib models
│   └── *.py                           # Individual model training scripts
├── MusicGroovesMIDI/                   # MIDI training data
│   ├── TrainingMIDIs/                  # Input MIDI files
│   ├── ProcessedMIDIs/                 # Processed MIDI files
│   └── ...
├── groove_features_log.csv             # Current session log (cleared each time)
├── groove_features_log_for_pred.csv    # Accumulated training data
└── groove_mood_model.onnx              # Main ONNX model for JUCE
```

## 🚀 Quick Start

### 1. Extract Features and Train Models
```bash
# Run the complete ML pipeline
python3 main.py --mode full-pipeline --interactive

# Or run steps individually:
python3 main.py --mode extract --interactive
python3 main.py --mode train
python3 main.py --mode predict
```

### 2. Individual Operations
```bash
# Extract features only
python3 extract_groove_features.py --interactive

# Train models only
python3 train_models.py

# Predict moods only
python3 predict_groove_mood.py --csv-file groove_features_log_for_pred.csv

# Data management
python3 main.py --mode copy-log    # Copy log to pred
python3 main.py --mode clear-log   # Clear log file
```

## 📊 Data Flow

### Feature Extraction Process
1. **Input**: MIDI files from `MusicGroovesMIDI/TrainingMIDIs/`
2. **Processing**: Extract musical features using `extract_groove_features.py`
3. **Output**: Features saved to `groove_features_log.csv`
4. **Data Management**: 
   - Copy log to `groove_features_log_for_pred.csv` (preserves training data)
   - Clear `groove_features_log.csv` (prevents duplicates)

### Model Training Process
1. **Input**: `groove_features_log_for_pred.csv` (accumulated training data)
2. **Training**: Train individual classification models
3. **Output**: 
   - `.joblib` files in `ModelClassificationScripts/models/`
   - `groove_mood_model.joblib` (main model)
   - `groove_mood_model.onnx` (for JUCE plugin)

### JUCE Communication
- **ONNX Model**: `groove_mood_model.onnx` → `../Resources/` → JUCE plugin
- **Real-time**: JUCE plugin processes MIDI input and uses ONNX model for mood prediction

## 🎯 Key Features

### Main Extraction Script (`extract_groove_features.py`)
- **Primary script** for feature extraction
- Interactive mood labeling
- Automatic model loading and prediction
- Data management (copy/clear log files)
- MIDI file processing and organization

### Model Training (`train_models.py`)
- Trains all classification models
- Uses accumulated training data
- Generates both `.joblib` and `.onnx` formats
- Error handling and progress tracking

### Data Management
- **`groove_features_log.csv`**: Current session data (cleared each time)
- **`groove_features_log_for_pred.csv`**: Accumulated training data
- **Automation scripts**: Copy and clear operations

## 🧠 ML Models

### Classification Models (`.joblib`)
- **Energy Classification**: Predicts energy level (0-17)
- **Dynamic Intensity**: Predicts dynamic intensity (0-9)
- **Swing Detection**: Predicts swing amount (0-1)
- **Fill Activity**: Predicts fill activity level (0-7)
- **Rhythmic Density**: Predicts rhythmic density (0-3)
- **FX Character**: Predicts FX character (0-9)
- **Timing Feel**: Predicts timing feel (0-3)

### Main Mood Model
- **Input**: 5 core features (tempo, swing, density, dynamic_range, energy)
- **Output**: 10 mood categories
- **Formats**: `.joblib` (Python) and `.onnx` (JUCE)

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

## 🔧 Usage Examples

### Complete Training Session
```bash
# 1. Extract features from new MIDI files
python3 main.py --mode full-pipeline --interactive

# 2. Copy models to JUCE Resources
python3 ../setup_ml_models.py

# 3. Build JUCE plugin
cd .. && python3 run_aamati.py --build-only
```

### Batch Processing
```bash
# Non-interactive mode for automation
python3 main.py --mode full-pipeline --non-interactive
```

### Data Management
```bash
# Copy current log to prediction file
python3 main.py --mode copy-log

# Clear current log
python3 main.py --mode clear-log
```

## 📈 Training Data

### Input Requirements
- **MIDI files**: Place in `MusicGroovesMIDI/TrainingMIDIs/`
- **Format**: `.mid` or `.midi` files
- **Content**: Any musical content for mood analysis

### Data Processing
1. **Feature Extraction**: 12+ musical features per file
2. **Mood Labeling**: Interactive user input for mood classification
3. **Model Prediction**: Use trained models for additional features
4. **Data Storage**: Save to CSV with timestamps and metadata

### Quality Control
- **Duplicate Prevention**: Log file cleared each session
- **Data Preservation**: Copy to prediction file before clearing
- **Error Handling**: Robust error handling for malformed MIDI files
- **Progress Tracking**: Real-time progress updates

## 🛠️ Troubleshooting

### Common Issues

1. **Models not loading**: Check if `.joblib` files exist in `ModelClassificationScripts/models/`
2. **MIDI processing errors**: Ensure MIDI files are valid and not corrupted
3. **Memory issues**: Process MIDI files in smaller batches
4. **Permission errors**: Check file permissions for MIDI directories

### Debug Mode
```bash
# Enable verbose output
python3 main.py --mode extract --verbose
```

### Log Files
- Check console output for detailed error messages
- MIDI processing errors are logged with file names
- Model loading status is displayed during startup

## 🔄 Integration with JUCE

### Model Export
- **ONNX Model**: `groove_mood_model.onnx` → `../Resources/`
- **Feature Mapping**: 5 core features for real-time prediction
- **Mood Labels**: 10 mood categories for UI display

### Real-time Processing
- **Input**: MIDI data from JUCE plugin
- **Processing**: Feature extraction + mood prediction
- **Output**: Mood classification for audio processing

## 📚 Next Steps

1. **Train Models**: Run `python3 main.py --mode full-pipeline --interactive`
2. **Export Models**: Run `python3 ../setup_ml_models.py`
3. **Build Plugin**: Run `cd .. && python3 run_aamati.py --build-only`
4. **Test Integration**: Load plugin in DAW and test with MIDI input

---

**🎵 Happy training with Aamati! 🎵**
