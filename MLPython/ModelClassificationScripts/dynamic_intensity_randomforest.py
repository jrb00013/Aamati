# dynamic_intensity_randomforest.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
from joblib import dump

df = pd.read_csv("../groove_features_log.csv")

features = ['velocity_mean', 'dynamic_range', 'velocity_std']
target = 'dynamic_intensity'  # e.g. labels like "soft", "medium", "hard"

df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

# Encode labels to integers
label_enc = LabelEncoder()
y_encoded = label_enc.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, stratify=y_encoded, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Dynamic Intensity Classification Report:")
print(classification_report(y_test, y_pred, target_names=label_enc.classes_))

# Save the trained model to disk to be used in extract_groove_features.py
dump(model, "models/energy_random_forest.joblib")
