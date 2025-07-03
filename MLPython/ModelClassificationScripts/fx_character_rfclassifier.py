# good_enough_fx_character.py

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
from imblearn.combine import SMOTETomek
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.preprocessing import PowerTransformer, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif
from joblib import dump
import matplotlib.pyplot as plt
import warnings

# CONFIG
CV_FOLDS = 5
MIN_SAMPLES_PER_CLASS = CV_FOLDS

# Load data
df = pd.read_csv("../groove_features_log.csv")

# Drop ultra-rare fx_character labels (less than CV_FOLDS samples)
label_counts = df['fx_character'].value_counts()
valid_labels = label_counts[label_counts >= MIN_SAMPLES_PER_CLASS].index
df = df[df['fx_character'].isin(valid_labels)]

# Feature engineering - add interaction terms
features = ['instrument_count', 'onset_entropy', 'pitch_range']
df['entropy_pitch_interaction'] = df['onset_entropy'] * df['pitch_range']
df['instr_entropy_interaction'] = df['instrument_count'] * df['onset_entropy']
features += ['entropy_pitch_interaction', 'instr_entropy_interaction']

# Drop rows with missing values
df = df.dropna(subset=features + ['fx_character'])

# Encode target labels
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(df['fx_character'])
X = df[features]

# Save label class mapping
np.save("models/fx_character_label_classes.npy", label_encoder.classes_)
print("✅ Saved label encoder classes.")

# Save feature names
with open("models/fx_character_features.txt", "w") as f:
    f.write("\n".join(features))
print("✅ Saved feature names.")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# Recalculate minimum class count in training set
train_class_counts = pd.Series(y_train).value_counts()
min_class_count = train_class_counts.min()

# Determine SMOTE k_neighbors
smote_k = min(5, max(min_class_count - 1, 2))  # ensure k >= 2

# Define stratified CV with safe folds
cv_folds = min(CV_FOLDS, min_class_count)
print(f"\n✅ Using {cv_folds}-fold Stratified Cross-Validation")
cv = StratifiedKFold(n_splits=cv_folds, shuffle=True, random_state=42)

# Define pipeline
pipeline = Pipeline([
    ('scaler', PowerTransformer()),
    ('feature_select', SelectKBest(score_func=f_classif, k='all')),
    ('resample', SMOTETomek(smote=SMOTE(k_neighbors=smote_k, random_state=42), random_state=42)),
    ('clf', GradientBoostingClassifier(random_state=42))  # placeholder
])

# Define parameter grid
param_grid = [
    {
        'clf': [GradientBoostingClassifier(random_state=42)],
        'clf__n_estimators': [100, 200],
        'clf__max_depth': [3, 5, 7],
        'clf__learning_rate': [0.05, 0.1],
        'clf__subsample': [0.8, 1.0],
    },
    {
        'clf': [RandomForestClassifier(class_weight='balanced', random_state=42)],
        'clf__n_estimators': [100, 200],
        'clf__max_depth': [None, 20, 30],
        'clf__min_samples_split': [2, 5],
        'clf__max_features': ['sqrt', 'log2'],
    }
]

# Suppress CV-related warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Run GridSearchCV
grid = GridSearchCV(
    pipeline,
    param_grid,
    scoring='f1_macro',
    cv=cv,
    n_jobs=-1,
    verbose=2
)

print("\nStarting Grid Search...")
grid.fit(X_train, y_train)
print(f"\n✅ Best CV macro F1 score: {grid.best_score_:.4f}")
print(f"✅ Best estimator: {grid.best_params_}")

# Test set evaluation
y_pred = grid.predict(X_test)
print("\nClassification Report on Test Set:")
print(classification_report(y_test, y_pred, zero_division=0))

# Confusion matrix
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=label_encoder.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()

# Feature importance display
clf = grid.best_estimator_.named_steps['clf']
if hasattr(clf, 'feature_importances_'):
    importances = clf.feature_importances_
    feat_imp = pd.Series(importances, index=features).sort_values(ascending=False)
    print("\nFeature Importances:")
    print(feat_imp)

# Save model
dump(grid.best_estimator_, "models/fx_character_classifier.joblib")
print("✅ Model saved as models/fx_character_classifier.joblib")
