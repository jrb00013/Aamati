# train_groove_model.py

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


# Load your dataset (you can build this as CSV or auto-generate from grooves later)
data = pd.read_csv('groove_features.csv')

# Features and labels
X = data[['tempo', 'swing', 'density', 'dynamic_range', 'energy']]
y = data['mood']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model (Random Forest for now — flexible and interpretable)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model as pkl
joblib.dump(model, 'groove_mood_model.pkl')
print("Model saved as groove_mood_model.pkl")

# Define the initial type (input shape)
initial_type = [('float_input', FloatTensorType([None, X.shape[1]]))]

# Convert to ONNX
onnx_model = convert_sklearn(model, initial_types=initial_type)

# Save model to file as .onnx
with open("groove_mood_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
print("Model exported to ONNX format as groove_mood_model.onnx")

