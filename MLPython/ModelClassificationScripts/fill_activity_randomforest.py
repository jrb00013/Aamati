import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from joblib import dump
from imblearn.over_sampling import SMOTE
import numpy as np

# Config
csv_path = "../groove_features_log.csv"
model_dir = "models"
model_path = os.path.join(model_dir, "fill_activity_randomforest.joblib")
random_seed = 42

features = [
    'pitch_range', 'velocity_std', 'onset_entropy',
    'syncopation', 'density', 'avg_polyphony',
    'std_note_length', 'energy'
]
target = 'fill_activity'

# Load dataset
if not os.path.exists(csv_path):
    print(f"❌ Error: CSV file not found: {csv_path}")
    sys.exit(1)

df = pd.read_csv(csv_path)
df = df.dropna(subset=features + [target])
y = df[target].astype(int)

# Filter classes with < 2 samples for stratified split
valid_classes = y.value_counts()[y.value_counts() >= 2].index
if len(valid_classes) < y.nunique():
    print("⚠️ Warning: Removing classes with <2 samples for stratified split.")
df = df[df[target].isin(valid_classes)]
X = df[features]
y = df[target].astype(int)

if len(y) == 0:
    print("❌ Error: No data left after filtering classes.")
    sys.exit(1)

# Train/test split with stratification and fixed random state
X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=random_seed
)

# SMOTE oversampling with consistent random state
min_class_count = y_train.value_counts().min()
smote_k = min(5, min_class_count - 1) if min_class_count > 1 else 1
print(f"Using SMOTE with k_neighbors={smote_k}")
smote = SMOTE(random_state=random_seed, k_neighbors=smote_k)
X_train_res, y_train_res = smote.fit_resample(X_train, y_train)

# Pipeline: Scaling + Random Forest
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('clf', RandomForestClassifier(class_weight='balanced', random_state=random_seed))
])

# Expanded hyperparameter grid for more tuning
param_grid = {
    'clf__n_estimators': [100, 200, 300],
    'clf__max_depth': [None, 20, 30, 40],
    'clf__min_samples_split': [2, 5, 10],
    'clf__min_samples_leaf': [1, 2, 4],
    'clf__max_features': ['sqrt', 'log2', None]
}

cv_strategy = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_seed)

grid = GridSearchCV(
    pipeline,
    param_grid=param_grid,
    scoring='f1_weighted',
    cv=cv_strategy,
    n_jobs=-1,
    verbose=2,
    refit=True
)

grid.fit(X_train_res, y_train_res)
model = grid.best_estimator_

print(f"Best hyperparameters:\n{grid.best_params_}")
print(f"Best cross-validation weighted F1 score: {grid.best_score_:.4f}")

# Predict and evaluate on test set
y_pred = model.predict(X_test)
print("Fill Activity Classification Report:")
print(classification_report(y_test, y_pred, zero_division=1))

# Confusion matrix plot
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=sorted(y.unique()), yticklabels=sorted(y.unique()))
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix - Fill Activity')
plt.tight_layout()
os.makedirs(model_dir, exist_ok=True)
plt.savefig(os.path.join(model_dir, "fill_activity_confusion_matrix.png"))
plt.close()

# Feature importance plot
importances = model.named_steps['clf'].feature_importances_
feat_imp = pd.Series(importances, index=X.columns).sort_values(ascending=True)
plt.figure(figsize=(8, 6))
feat_imp.plot(kind='barh')
plt.title("Feature Importance - Fill Activity")
plt.xlabel("Importance")
plt.tight_layout()
plt.savefig(os.path.join(model_dir, "fill_activity_feature_importance.png"))
plt.close()

# Save the trained model
dump(model, model_path)
print(f"✅ Model saved to {model_path}")
