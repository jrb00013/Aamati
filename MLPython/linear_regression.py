import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the dataset
df = pd.read_csv("groove_features_log.csv")

# Select input features and the target 'energy'
features = ['density', 'velocity_mean', 'dynamic_range', 'avg_polyphony']
X = df[features]
y = df['energy']

# Train linear regression model
model = LinearRegression()
model.fit(X, y)

# Output weights
print("Learned Energy Equation:")
terms = []
for feature, coef in zip(features, model.coef_):
    terms.append(f"({coef:.4f} * {feature})")
equation = " + ".join(terms) + f" + {model.intercept_:.4f}"
print(f"energy = {equation}")
