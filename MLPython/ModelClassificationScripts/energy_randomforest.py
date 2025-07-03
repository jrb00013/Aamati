# energy_random_forest.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump

# Load the dataset
df = pd.read_csv("../raw_features.csv")

# Drop rows with missing values
features = ['density', 'velocity_mean', 'dynamic_range', 'avg_polyphony']
target = 'energy'
df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Fit Random Forest Regressor
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

# Save the trained model to disk to be used in extract_groove_features.py
dump(model, "models/energy_random_forest.joblib")

# Predict
y_pred = model.predict(X_test)

# Evaluate
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n🌲 Random Forest Energy Regressor Results:")
print(f"  Mean Squared Error: {mse:.4f}")
print(f"  R^2 Score: {r2:.4f}")

# Feature importance
print("\n🔍 Feature Importances:")
for feature, importance in zip(features, model.feature_importances_):
    print(f"  {feature}: {importance:.4f}")
