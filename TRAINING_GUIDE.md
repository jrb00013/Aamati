# 🎵 Aamati ML Training Guide

This comprehensive guide will walk you through training the Aamati machine learning system from start to finish.

## 📋 Prerequisites

### System Requirements
- **Python 3.8+** with pip
- **JUCE Framework** (for plugin development)
- **ONNX Runtime** (for C++ integration)
- **MIDI files** for training data
- **8GB+ RAM** (recommended for large datasets)

### Required Python Packages
```bash
pip install pandas numpy scikit-learn joblib pretty_midi scipy matplotlib seaborn onnx
```

## 🎯 Training Overview

The Aamati ML system consists of **7 classification models** plus **1 main mood model**:

### Classification Models (Individual Features)
1. **Energy Classification** (0-17 levels)
2. **Dynamic Intensity** (0-9 levels) 
3. **Swing Detection** (0-1 continuous)
4. **Fill Activity** (0-7 levels)
5. **Rhythmic Density** (0-3 levels)
6. **FX Character** (0-9 categories)
7. **Timing Feel** (0-3 levels)

### Main Mood Model (Final Output)
- **Input**: 5 core features (tempo, swing, density, dynamic_range, energy)
- **Output**: 10 mood categories
- **Formats**: `.joblib` (Python) + `.onnx` (JUCE plugin)

## 🚀 Complete Training Workflow

### Step 1: Prepare Training Data

#### 1.1 Organize MIDI Files
```bash
# Place your MIDI files in the training directory
cp your_midi_files/*.mid MLPython/MusicGroovesMIDI/TrainingMIDIs/
```

#### 1.2 Verify Data Structure
```
MLPython/MusicGroovesMIDI/
├── TrainingMIDIs/          # Input MIDI files
├── ProcessedMIDIs/         # Processed files (auto-moved)
├── InputMIDI/             # Alternative input folder
└── FixedMIDIs/            # Fixed/corrected files
```

### Step 2: Run Feature Extraction

#### 2.1 Interactive Mode (Recommended for First Time)
```bash
cd MLPython
python3 extract_groove_features.py --interactive
```

**What happens:**
- Processes each MIDI file in `TrainingMIDIs/`
- Extracts 12+ musical features per file
- Prompts you to label each file with primary/secondary mood
- Saves features to `groove_features_log.csv`
- Moves processed files to `ProcessedMIDIs/`

#### 2.2 Non-Interactive Mode (Batch Processing)
```bash
python3 extract_groove_features.py --non-interactive --midi-folder MusicGroovesMIDI/TrainingMIDIs
```

#### 2.3 Data Management
```bash
# Copy current session to training data
python3 main.py --mode copy-log

# Clear current session (prevents duplicates)
python3 main.py --mode clear-log
```

### Step 3: Train Individual Classification Models

#### 3.1 Train All Models
```bash
python3 train_models.py
```

**This trains:**
- Energy Random Forest
- Dynamic Intensity Random Forest  
- Swing Random Forest
- Fill Activity Random Forest
- Rhythmic Density Ordinal Regression
- FX Character Random Forest
- Timing Feel Random Forest

#### 3.2 Train Individual Models
```bash
# Train specific models
python3 ModelClassificationScripts/energy_randomforest.py
python3 ModelClassificationScripts/dynamic_intensity_randomforest.py
python3 ModelClassificationScripts/swing_randomforest.py
# ... etc
```

### Step 4: Train Main Mood Model

#### 4.1 Generate Main Model
```bash
python3 MachineLearningModel.py
```

**This creates:**
- `groove_mood_model.joblib` (Python format)
- `groove_mood_model.onnx` (JUCE plugin format)

### Step 5: Export Models for JUCE

#### 5.1 Copy Models to Resources
```bash
cd ..
python3 setup_ml_models.py
```

**This copies:**
- `groove_mood_model.onnx` → `Resources/`
- All `.joblib` models → `Resources/`

## 📊 Training Data Requirements

### Minimum Dataset Size
- **50+ MIDI files** (minimum)
- **200+ MIDI files** (recommended)
- **500+ MIDI files** (optimal)

### Data Quality Guidelines

#### Good Training Data
- ✅ **Diverse genres** (classical, rock, electronic, jazz, etc.)
- ✅ **Varied tempos** (60-200 BPM)
- ✅ **Different moods** (energetic, calm, dramatic, etc.)
- ✅ **Clean MIDI files** (no corruption)
- ✅ **Multiple instruments** (not just piano)

#### Avoid These
- ❌ **Corrupted MIDI files**
- ❌ **Very short files** (< 10 seconds)
- ❌ **Single instrument only**
- ❌ **Same genre only**
- ❌ **Very similar tempos**

### Mood Labeling Guidelines

When labeling moods during extraction, consider:

| Mood | Characteristics | Tempo Range | Energy Level |
|------|----------------|-------------|--------------|
| 🧊 **Chill** | Relaxed, mellow, ambient | 60-115 BPM | 2-5 |
| ⚡ **Energetic** | Fast, driving, intense | 120-175 BPM | 13-15 |
| 🕳️ **Suspenseful** | Tense, minor keys, stabs | 75-125 BPM | 6-9 |
| 🌅 **Uplifting** | Bright, major keys, happy | 100-160 BPM | 7-13 |
| 🌑 **Ominous** | Dark, brooding, sparse | 55-100 BPM | 5-8 |
| 💘 **Romantic** | Flowing, expressive, warm | 60-125 BPM | 5-9 |
| 🪓 **Gritty** | Raw, mechanical, dirty | 135-180 BPM | 10-14 |
| 💭 **Dreamy** | Reverb-heavy, ethereal | 70-110 BPM | 5-8 |
| 🌀 **Frantic** | Chaotic, rapid, wild | 160-250 BPM | 14-17 |
| 🎯 **Focused** | Steady, precise, repetitive | 83-135 BPM | 8-11 |

## 🔧 Advanced Training Techniques

### Incremental Training
```bash
# Add new data to existing training set
python3 main.py --mode copy-log    # Preserve existing data
python3 extract_groove_features.py --interactive  # Add new data
python3 train_models.py            # Retrain with all data
```

### Cross-Validation
```bash
# The training scripts automatically use cross-validation
# Check ModelClassificationScripts/models/ for validation reports
```

### Hyperparameter Tuning
Edit individual model scripts to adjust:
- **Random Forest**: `n_estimators`, `max_depth`, `min_samples_split`
- **Ordinal Regression**: `alpha`, `learning_rate`
- **Feature Selection**: Remove less important features

## 📈 Monitoring Training Progress

### Real-Time Monitoring
```bash
# Watch training progress
tail -f MLPython/ModelClassificationScripts/models/classification_reports.txt
```

### Model Performance Metrics
Check these files after training:
- `classification_reports.txt` - Overall performance
- `*_confusion_matrix.png` - Classification accuracy
- `*_feature_importance.png` - Feature importance

### Expected Performance
- **Accuracy**: 80-95% (varies by model)
- **Precision**: 0.8-0.95
- **Recall**: 0.8-0.95
- **F1-Score**: 0.8-0.95

## 🚨 Troubleshooting

### Common Issues

#### 1. "No MIDI files found"
```bash
# Check if files are in correct directory
ls MLPython/MusicGroovesMIDI/TrainingMIDIs/
```

#### 2. "Model training failed"
```bash
# Check if you have enough data
wc -l MLPython/groove_features_log_for_pred.csv
# Should have 50+ lines (excluding header)
```

#### 3. "Memory error during training"
```bash
# Process smaller batches
python3 extract_groove_features.py --non-interactive --midi-folder MusicGroovesMIDI/TrainingMIDIs
# Then train models
```

#### 4. "ONNX model not generated"
```bash
# Check if main model training completed
ls -la MLPython/groove_mood_model.*
```

### Debug Mode
```bash
# Enable verbose output
python3 extract_groove_features.py --interactive --verbose
python3 train_models.py --verbose
```

## 📊 Data Analysis

### Analyze Your Training Data
```bash
# View feature distributions
python3 -c "
import pandas as pd
df = pd.read_csv('MLPython/groove_features_log_for_pred.csv')
print('Dataset size:', len(df))
print('Mood distribution:')
print(df['primary_mood'].value_counts())
print('Feature ranges:')
print(df[['tempo', 'swing', 'density', 'energy']].describe())
"
```

### Feature Correlation Analysis
```bash
# Check feature correlations
python3 -c "
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('MLPython/groove_features_log_for_pred.csv')
corr = df[['tempo', 'swing', 'density', 'dynamic_range', 'energy']].corr()
sns.heatmap(corr, annot=True)
plt.savefig('feature_correlation.png')
print('Correlation matrix saved to feature_correlation.png')
"
```

## 🎯 Best Practices

### 1. Data Collection
- **Start small**: Begin with 50-100 files
- **Diverse selection**: Include multiple genres and moods
- **Quality over quantity**: Better to have 100 good files than 500 poor ones

### 2. Labeling Strategy
- **Be consistent**: Use the same criteria for similar files
- **Trust your instincts**: Your musical intuition is valuable
- **Document decisions**: Note why you chose specific moods

### 3. Training Strategy
- **Incremental approach**: Add data gradually
- **Regular validation**: Test models frequently
- **Backup data**: Keep copies of your training data

### 4. Model Evaluation
- **Test on new data**: Don't just rely on training accuracy
- **Check confusion matrices**: Look for systematic errors
- **Monitor feature importance**: Understand what drives predictions

## 📚 Next Steps

After completing training:

1. **Export models**: `python3 setup_ml_models.py`
2. **Build JUCE plugin**: `python3 run_aamati.py --build-only`
3. **Test integration**: Load plugin in your DAW
4. **Iterate**: Add more data and retrain as needed

## 🆘 Getting Help

### Check Logs
```bash
# View extraction logs
cat MLPython/groove_features_log.csv

# View training logs
ls MLPython/ModelClassificationScripts/models/*.txt
```

### Common Commands Reference
```bash
# Complete training pipeline
python3 MLPython/main.py --mode full-pipeline --interactive

# Individual steps
python3 MLPython/extract_groove_features.py --interactive
python3 MLPython/train_models.py
python3 MLPython/predict_groove_mood.py

# Data management
python3 MLPython/main.py --mode copy-log
python3 MLPython/main.py --mode clear-log
```

---

**🎵 Happy Training with Aamati! 🎵**

*Remember: Good training data leads to great models. Take your time to collect diverse, high-quality MIDI files and label them thoughtfully.*
