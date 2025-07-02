# energy_linear_regression.py
# Linear Regression
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
df = pd.read_csv("groove_features_log.csv")

# Drop rows with missing values in relevant columns
features = ['density', 'velocity_mean', 'dynamic_range', 'avg_polyphony']
target = 'energy'
df = df.dropna(subset=features + [target])

X = df[features]
y = df[target]

# Split data for evaluation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on test set
y_pred = model.predict(X_test)

# Evaluate model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Learned Energy Equation:")
terms = [f"({coef:.4f} * {feat})" for coef, feat in zip(model.coef_, features)]
equation = " + ".join(terms) + f" + {model.intercept_:.4f}"
print(f"energy = {equation}\n")

print(f"Model Performance on Test Set:")
print(f"  Mean Squared Error: {mse:.4f}")
print(f"  R^2 Score: {r2:.4f}")
