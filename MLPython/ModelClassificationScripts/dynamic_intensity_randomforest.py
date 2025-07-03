# dynamic_intensity_randomforest.py
import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from joblib import dump
from imblearn.over_sampling import SMOTE
from collections import Counter

# Load dataset
df = pd.read_csv("../groove_features_log.csv")

features = ['velocity_mean', 'dynamic_range', 'velocity_std']
target = 'dynamic_intensity'  # target labels like "soft", "medium", "hard"

# Drop rows with missing values in features or target
df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

# Encode target labels as integers
label_enc = LabelEncoder()
y_encoded = label_enc.fit_transform(y)

# Split into training and testing sets (stratified)
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, stratify=y_encoded, test_size=0.2, random_state=42)

# Inspect and print class distribution in training set
class_counts = Counter(y_train)
print("Training class distribution:", class_counts)

# Compute safe k_neighbors for SMOTE
min_class_size = min(class_counts.values())
k_neighbors = min(5, min_class_size - 1) if min_class_size > 1 else 1
print(f"Using SMOTE with k_neighbors={k_neighbors}")

# Apply SMOTE only on training data to balance classes
smote = SMOTE(random_state=42, k_neighbors=k_neighbors)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Setup hyperparameter grid for tuning
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2', None] 
}

# Create RandomForestClassifier instance
rf = RandomForestClassifier(random_state=42)

# Setup GridSearchCV with 3-fold CV
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=3,
    n_jobs=-1,
    verbose=2
)

# Run grid search on resampled training data
print("Starting GridSearchCV for hyperparameter tuning...")
grid_search.fit(X_train_res, y_train_res)

print("Best hyperparameters found:")
print(grid_search.best_params_)

# Use the best estimator from grid search
model = grid_search.best_estimator_

# Predict on test set
y_pred = model.predict(X_test)

# Convert label classes to strings for classification_report
label_names = [str(label) for label in label_enc.classes_]

# Print classification report
print("Dynamic Intensity Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_names))

# Save the trained model for later use
os.makedirs("models", exist_ok=True)
dump(model, "models/dynamic_intensity_randomforest.joblib")

# Optional: save label encoder for later use
# dump(label_enc, "models/dynamic_intensity_encoder.joblib")
