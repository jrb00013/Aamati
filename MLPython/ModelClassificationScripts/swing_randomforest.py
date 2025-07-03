# swing_randomforest.py
import os
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump
import numpy as np

# Load dataset — make sure it has swing labels (0 to 1 float or continuous)
df = pd.read_csv("../groove_features_log.csv")

# List of features for swing prediction
features = [
    'density', 'velocity_mean', 'dynamic_range', 'avg_polyphony',
    'syncopation', 'onset_entropy', 'rhythmic_density'  # Ensure rhythmic_density is numeric
]

target = 'swing'  # Continuous swing value (0 to 1 float)

# Drop rows with missing values in features or target
df = df.dropna(subset=features + [target])

# Encode rhythmic_density if it's categorical string
if df['rhythmic_density'].dtype == object:
    mapping = {'low': 0, 'medium': 1, 'high': 2, 'very_high': 3}
    df['rhythmic_density'] = df['rhythmic_density'].map(mapping)
    if df['rhythmic_density'].isnull().any():
        print("Warning: Some rhythmic_density values could not be mapped and are NaN.")
        df = df.dropna(subset=['rhythmic_density'])

X = df[features]
y = df[target]

print(f"Features shape: {X.shape}")
print(f"Target shape: {y.shape}")
print(f"Feature types:\n{X.dtypes}")

# Split dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Setup hyperparameter grid for tuning
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
}

# Initialize Random Forest Regressor
rf = RandomForestRegressor(random_state=42, n_jobs=-1)

# Setup GridSearchCV
grid_search = GridSearchCV(
    estimator=rf,
    param_grid=param_grid,
    cv=3,
    n_jobs=-1,
    verbose=2,
    scoring='neg_mean_squared_error'  # minimize MSE
)

print("Starting GridSearchCV for hyperparameter tuning...")
grid_search.fit(X_train, y_train)

print("Best hyperparameters found:")
print(grid_search.best_params_)

# Use best estimator from GridSearchCV
model = grid_search.best_estimator_

# Predict on test set
y_pred = model.predict(X_test)

# Evaluate performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Swing Model MSE: {mse:.4f}")
print(f"Swing Model R2: {r2:.4f}")

# Feature importance
importances = model.feature_importances_
for f, imp in sorted(zip(features, importances), key=lambda x: x[1], reverse=True):
    print(f"Feature: {f}, Importance: {imp:.4f}")

# Ensure models directory exists before saving
os.makedirs("models", exist_ok=True)
dump(model, "models/swing_random_forest.joblib")
print("Model saved to models/swing_random_forest.joblib")