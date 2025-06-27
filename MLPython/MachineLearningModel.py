# MachineLearningModel.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import classification_report
import joblib
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType

# Load data
data = pd.read_csv('groove_features_log.csv')

print("Total samples:", len(data))
print("Class distribution:\n", data['mood'].value_counts())

numerical_features = [
    'tempo', 'swing', 'density', 'dynamic_range', 'energy',
    'mean_note_length', 'std_note_length', 'velocity_mean', 'velocity_std',
    'pitch_mean', 'pitch_range', 'avg_polyphony', 'syncopation',
    'onset_entropy', 'instrument_count'
]

categorical_features = [
    'timing_feel', 'rhythmic_density', 'dynamic_intensity',
    'fill_activity', 'fx_character'
]

# Drop rows with missing values in features or label
data = data.dropna(subset=numerical_features + categorical_features + ['mood'])

X_num = data[numerical_features].values
X_cat = data[categorical_features]

y = data['mood']

# Fit OneHotEncoder on categorical features
encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
X_cat_encoded = encoder.fit_transform(X_cat)

# Combine encoded categorical features and numerical features
X_all = np.hstack([X_cat_encoded, X_num])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X_all, y, test_size=0.2, random_state=42)

# Train RandomForestClassifier on numeric input only
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model as .pkl and encoder for later use in prediction
joblib.dump(model, 'groove_mood_model.pkl')
joblib.dump(encoder, 'categorical_encoder.pkl')
print("Model and encoder saved.")

# Convert to ONNX format 
initial_type = [('float_input', FloatTensorType([None, X_all.shape[1]]))]
onnx_model = convert_sklearn(model, initial_types=initial_type)

with open("groove_mood_model.onnx", "wb") as f:
    f.write(onnx_model.SerializeToString())
print("Model exported to ONNX format.")
