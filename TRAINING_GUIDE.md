# Aamati Training Guide

## 🧠 Complete Machine Learning Training Guide

This guide will walk you through training the Aamati machine learning models for optimal mood analysis and MIDI processing.

## 📋 Prerequisites

### System Requirements
- Python 3.8+
- 8GB+ RAM (16GB recommended)
- 10GB+ free disk space
- MIDI files for training (100+ files recommended)

### Dependencies
```bash
# Install required packages
pip install -r MLPython/requirements.txt

# Or install individually
pip install pandas numpy scikit-learn joblib onnx pretty_midi scipy imbalanced-learn
```

## 🎵 Training Data Preparation

### 1. MIDI File Organization
```
MusicGroovesMIDI/
├── TrainingMIDIs/          # Your training MIDI files
├── ProcessedMIDIs/         # Processed files (auto-created)
└── InactiveMIDIs/          # Moved after processing
```

### 2. MIDI File Requirements
- **Format**: Standard MIDI (.mid, .midi)
- **Quality**: Well-structured, clean MIDI
- **Diversity**: Various genres, tempos, and styles
- **Quantity**: Minimum 100 files, 500+ recommended

### 3. Mood Labeling Strategy
Create a consistent mood labeling system:

#### Primary Moods
- **Chill**: Relaxed, ambient, slow tempo
- **Energetic**: Fast, upbeat, high energy
- **Suspenseful**: Tense, mysterious, building
- **Uplifting**: Positive, bright, major keys
- **Ominous**: Dark, foreboding, minor keys
- **Romantic**: Warm, emotional, expressive
- **Gritty**: Raw, aggressive, distorted
- **Dreamy**: Ethereal, floating, reverb-heavy
- **Frantic**: Chaotic, complex, high tempo
- **Focused**: Clear, precise, steady

#### Secondary Moods
- Use same categories as primary
- Represents subtle emotional undertones
- Example: "Energetic" + "Romantic" = upbeat love song

## 🚀 Training Process

### Step 1: Feature Extraction
```bash
# Navigate to MLPython directory
cd MLPython

# Run feature extraction
python3 extract_groove_features.py \
    --midi-folder ../MusicGroovesMIDI/TrainingMIDIs \
    --interactive \
    --batch-size 25 \
    --max-files 100
```

#### Interactive Mode
When prompted, label each MIDI file:
```
🎯 Choose **primary** mood (chill/energetic/suspenseful/...): energetic
🎨 Choose **secondary** mood (chill/energetic/suspenseful/...): romantic
```

#### Non-Interactive Mode
```bash
python3 extract_groove_features.py \
    --midi-folder ../MusicGroovesMIDI/TrainingMIDIs \
    --non-interactive \
    --batch-size 50
```

### Step 2: Data Validation
```bash
# Check extracted features
python3 -c "
import pandas as pd
df = pd.read_csv('data/csv/groove_features_log_for_pred.csv')
print(f'Total samples: {len(df)}')
print(f'Features: {list(df.columns)}')
print(f'Mood distribution:')
print(df['primary_mood'].value_counts())
"
```

### Step 3: Model Training
```bash
# Train all models
python3 train_models.py

# Or train specific models
python3 optimized_mood_classifier.py
```

### Step 4: Model Validation
```bash
# Test model accuracy
python3 predict_groove_mood.py \
    --csv-file data/csv/groove_features_log_for_pred.csv \
    --test-mode
```

## 🔧 Advanced Training Options

### Custom Feature Engineering
Edit `MLPython/src/core/extract_groove_features.py`:

```python
def extract_custom_feature(midi_data):
    """Add your custom feature extraction logic here."""
    # Example: Extract harmonic complexity
    chords = extract_chord_progression(midi_data)
    complexity = calculate_harmonic_complexity(chords)
    return complexity

# Add to features dictionary
features['harmonic_complexity'] = extract_custom_feature(pm)
```

### Hyperparameter Tuning
Edit `MLPython/optimized_mood_classifier.py`:

```python
# Adjust Random Forest parameters
RandomForestClassifier(
    n_estimators=300,        # Increase for better accuracy
    max_depth=20,            # Increase for complex patterns
    min_samples_split=3,     # Decrease for more sensitivity
    min_samples_leaf=1,      # Decrease for more detail
    max_features='sqrt',     # Feature selection strategy
    random_state=42
)
```

### Cross-Validation
```python
# Add cross-validation to training
from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(classifier, X, y, cv=10, scoring='accuracy')
print(f"Cross-validation accuracy: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
```

## 📊 Training Monitoring

### Real-time Progress
```bash
# Monitor training progress
tail -f data/logs/training.log

# Check system resources
python3 system_health.py --monitor
```

### Performance Metrics
```python
# Evaluate model performance
from sklearn.metrics import classification_report, confusion_matrix

# Generate detailed report
y_pred = classifier.predict(X_test)
print(classification_report(y_test, y_pred))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)
```

## 🎯 Optimizing Training Results

### 1. Data Quality
- **Clean MIDI**: Remove corrupted or incomplete files
- **Balanced Dataset**: Ensure equal representation of all moods
- **Diverse Sources**: Include various artists, genres, and styles

### 2. Feature Selection
```python
# Analyze feature importance
feature_importance = classifier.feature_importances_
feature_names = X.columns

# Sort by importance
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': feature_importance
}).sort_values('importance', ascending=False)

print(importance_df.head(10))
```

### 3. Model Ensemble
```python
# Combine multiple models for better accuracy
from sklearn.ensemble import VotingClassifier

ensemble = VotingClassifier([
    ('rf', RandomForestClassifier()),
    ('gb', GradientBoostingClassifier()),
    ('svm', SVC(probability=True))
], voting='soft')

ensemble.fit(X_train, y_train)
```

## 🔄 Iterative Training

### 1. Initial Training
```bash
# Start with basic training
python3 extract_groove_features.py --interactive --batch-size 10
python3 train_models.py
```

### 2. Evaluate Results
```bash
# Test on new data
python3 predict_groove_mood.py --csv-file test_data.csv
```

### 3. Refine and Retrain
- Add more training data
- Adjust feature extraction
- Tune hyperparameters
- Retrain models

### 4. Validation Loop
```bash
# Continuous validation
while true; do
    python3 extract_groove_features.py --non-interactive
    python3 train_models.py
    python3 predict_groove_mood.py --test-mode
    sleep 3600  # Wait 1 hour
done
```

## 📈 Training Best Practices

### 1. Data Augmentation
```python
# Augment training data
def augment_midi_data(midi_file, variations=5):
    """Create variations of MIDI data for training."""
    variations = []
    for i in range(variations):
        # Transpose to different keys
        transposed = transpose_midi(midi_file, i * 2)
        variations.append(transposed)
    return variations
```

### 2. Feature Scaling
```python
# Scale features for better training
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
```

### 3. Handling Imbalanced Data
```python
# Use SMOTE for imbalanced classes
from imblearn.over_sampling import SMOTE

smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)
```

## 🧪 Testing and Validation

### 1. Holdout Validation
```bash
# Split data into train/test sets
python3 -c "
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv('data/csv/groove_features_log_for_pred.csv')
train, test = train_test_split(df, test_size=0.2, random_state=42)
train.to_csv('data/csv/train_data.csv', index=False)
test.to_csv('data/csv/test_data.csv', index=False)
"
```

### 2. Cross-Validation
```python
# 10-fold cross-validation
from sklearn.model_selection import cross_val_score

scores = cross_val_score(classifier, X, y, cv=10)
print(f"Accuracy: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
```

### 3. Real-world Testing
```bash
# Test with live MIDI input
python3 run_aamati.py --test-only --suite real_time
```

## 📊 Model Export and Deployment

### 1. Export Models
```bash
# Export all models
python3 setup_ml_models.py

# Check exported models
ls -la Aamati/Resources/*.onnx
ls -la MLPython/models/trained/*.joblib
```

### 2. Model Versioning
```bash
# Create model backup
cp -r MLPython/models/trained MLPython/models/backup_$(date +%Y%m%d)

# Tag model version
git tag -a v1.0.0 -m "Trained models v1.0.0"
```

### 3. Performance Monitoring
```bash
# Monitor model performance in production
python3 system_health.py --monitor --check-models
```

## 🚨 Troubleshooting

### Common Training Issues

#### 1. Low Accuracy
- **Cause**: Insufficient training data
- **Solution**: Add more diverse MIDI files
- **Check**: Feature quality and relevance

#### 2. Overfitting
- **Cause**: Model too complex for data
- **Solution**: Reduce model complexity, add regularization
- **Check**: Training vs validation accuracy

#### 3. Underfitting
- **Cause**: Model too simple
- **Solution**: Increase model complexity, add features
- **Check**: Feature engineering and selection

#### 4. Memory Issues
- **Cause**: Large dataset or complex model
- **Solution**: Reduce batch size, use data streaming
- **Check**: System resources and model parameters

### Debug Commands
```bash
# Check data quality
python3 -c "
import pandas as pd
df = pd.read_csv('data/csv/groove_features_log_for_pred.csv')
print(df.describe())
print(df.isnull().sum())
"

# Check model performance
python3 -c "
import joblib
model = joblib.load('MLPython/models/trained/primary_mood_classifier.joblib')
print(f'Model type: {type(model)}')
print(f'Feature count: {model.n_features_in_}')
"
```

## 📚 Advanced Topics

### 1. Transfer Learning
```python
# Use pre-trained models as starting point
from sklearn.base import BaseEstimator

class TransferLearningClassifier(BaseEstimator):
    def __init__(self, base_model, fine_tune_layers=2):
        self.base_model = base_model
        self.fine_tune_layers = fine_tune_layers
```

### 2. Multi-task Learning
```python
# Train multiple related tasks simultaneously
def multi_task_loss(y_true, y_pred):
    primary_loss = cross_entropy(y_true['primary'], y_pred['primary'])
    secondary_loss = cross_entropy(y_true['secondary'], y_pred['secondary'])
    return primary_loss + 0.5 * secondary_loss
```

### 3. Active Learning
```python
# Select most informative samples for labeling
def select_informative_samples(model, unlabeled_data, n_samples=10):
    predictions = model.predict_proba(unlabeled_data)
    uncertainty = np.max(predictions, axis=1)
    return np.argsort(uncertainty)[:n_samples]
```

## 🎯 Success Metrics

### Target Performance
- **Accuracy**: >85% for primary mood classification
- **Confidence**: >80% average confidence score
- **Latency**: <50ms for real-time prediction
- **Memory**: <500MB for model loading

### Monitoring Dashboard
```bash
# Create training dashboard
python3 -c "
import matplotlib.pyplot as plt
import pandas as pd

# Plot training progress
df = pd.read_csv('data/logs/training_progress.csv')
plt.plot(df['epoch'], df['accuracy'])
plt.title('Training Accuracy Over Time')
plt.savefig('training_progress.png')
"
```

## 🚀 Next Steps

### 1. Production Deployment
- Export optimized models
- Deploy to JUCE plugin
- Monitor real-time performance

### 2. Continuous Learning
- Collect user feedback
- Retrain with new data
- Update models regularly

### 3. Feature Expansion
- Add new musical features
- Experiment with deep learning
- Integrate external data sources

---

## 🎉 Training Complete!

You now have a fully trained Aamati system ready for production use. The models will provide accurate mood analysis and enable all the advanced features of the plugin.

**Start creating amazing music with AI! 🎵✨**