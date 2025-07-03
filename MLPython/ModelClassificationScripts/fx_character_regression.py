# fx_character_regression.py

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump

df = pd.read_csv("groove_features_log.csv")

features = ['instrument_count', 'onset_entropy', 'pitch_range']
target = 'fx_character_score' 

df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("FX Character Regression Performance:")
print(f"  MSE: {mse:.4f}")
print(f"  R^2: {r2:.4f}")

# Save the trained model to disk to be used in extract_groove_features.py
dump(model, "models/energy_random_forest.joblib")
