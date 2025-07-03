# fill_activity_randomforest.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from joblib import dump

df = pd.read_csv("groove_features_log.csv")

features = ['pitch_range', 'velocity_std', 'onset_entropy']
target = 'fill_activity'  # ordinal encoded: e.g. 0=sparse, 1=moderate, 2=dense

df = df.dropna(subset=features + [target])

X = df[features]
y = df[target].astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Fill Activity Classification Report:")
print(classification_report(y_test, y_pred))

# Save the trained model to disk to be used in extract_groove_features.py
dump(model, "models/energy_random_forest.joblib")
