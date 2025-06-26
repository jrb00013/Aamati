# MachineLearningModel.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import torch
import torch.nn as nn
import torch.optim as optim
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType


# Load datasheet
data = pd.read_csv('groove_features_log.csv')

# Features and labels and use all extracted features except mood and timestamp
feature_columns = [
    'tempo', 'swing', 'density', 'dynamic_range', 'energy',
    'mean_note_length', 'std_note_length', 'velocity_mean', 'velocity_std',
    'pitch_mean', 'pitch_range', 'avg_polyphony', 'syncopation',
    'onset_entropy', 'instrument_count'
]
X = data[feature_columns]
y = data['mood']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, 'groove_mood_model.pkl')
print("Model saved as groove_mood_model.pkl")

# Convert to ONNX format
initial_type = [('float_input', FloatTensorType([None, X.shape[1]]))]
onnx_model = convert_sklearn(model, initial_types=initial_type)

with open("groove_mood_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
print("Model exported to ONNX format as groove_mood_model.onnx")