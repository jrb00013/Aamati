# rhythmic_density_ordinal_regression.py
# Ordinal Regression
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Load dataset
df = pd.read_csv("groove_features_log.csv")

# Features to predict rhythmic_density (ordinal: e.g. 0,1,2,3)
features = ['density', 'syncopation', 'std_note_length']
target = 'rhythmic_density'  # Should be ordinal encoded (0,1,2,3)

# Drop missing rows
df = df.dropna(subset=features + [target])

X = df[features]
y = df[target].astype(int)  # Ensure integer class labels

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42, test_size=0.2)

# Train classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
print("Rhythmic Density Classification Report:")
print(classification_report(y_test, y_pred))
