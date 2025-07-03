# rhythmic_density_ordinal_regression.py

import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from joblib import dump
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def main(input_csv, model_path, do_tune=False):
    print(f"Loading data from {input_csv} ...")
    df = pd.read_csv(input_csv)

    features = ['density', 'syncopation', 'std_note_length']
    target = 'rhythmic_density'

    # Drop missing values in features or target
    df = df.dropna(subset=features + [target])

    # Convert target to int
    df[target] = df[target].astype(int)

    X = df[features]
    y = df[target]

    print("Class distribution before split:")
    print(y.value_counts(normalize=True).sort_index())

    # Stratified train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, stratify=y, test_size=0.2, random_state=42
    )

    print("Class distribution in train set:")
    print(y_train.value_counts(normalize=True).sort_index())
    print("Class distribution in test set:")
    print(y_test.value_counts(normalize=True).sort_index())

    # Initialize Random Forest with class_weight balanced to help minority class
    model = RandomForestClassifier(
        random_state=42, n_jobs=-1, n_estimators=200, class_weight='balanced'
    )

    if do_tune:
        print("Performing hyperparameter tuning with GridSearchCV...")
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 5, 10],
            'min_samples_split': [2, 5, 10]
        }
        grid = GridSearchCV(model, param_grid, cv=5, n_jobs=-1, scoring='f1_macro')
        grid.fit(X_train, y_train)
        model = grid.best_estimator_
        print(f"Best parameters: {grid.best_params_}")

    print("Training model ...")
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    print("Rhythmic Density Classification Report:")
    print(classification_report(y_test, y_pred, zero_division=1))

    # Confusion matrix plot — save to file for headless environments
    cm = confusion_matrix(y_test, y_pred, labels=sorted(y.unique()))
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d',
                xticklabels=sorted(y.unique()), yticklabels=sorted(y.unique()),
                cmap="Blues")
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig("rhythmic_density_confusion_matrix.png")
    plt.close()
    print("Confusion matrix saved as rhythmic_density_confusion_matrix.png in the models folder")

    # Feature importance with sorted features
    importances = model.feature_importances_
    feat_imp = sorted(zip(features, importances), key=lambda x: x[1], reverse=True)
    print("Feature Importances:")
    for f, imp in feat_imp:
        print(f"  {f}: {imp:.4f}")

    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    dump(model, model_path)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Rhythmic Density Classifier")
    parser.add_argument(
        "--input_csv", default="../groove_features_log.csv",
        help="Path to groove features CSV file"
    )
    parser.add_argument(
        "--model_path", default="models/rhythmic_density_ordinal_regression.joblib",
        help="Path to save trained model"
    )
    parser.add_argument(
        "--tune", action='store_true',
        help="Enable hyperparameter tuning"
    )
    args = parser.parse_args()

    main(args.input_csv, args.model_path, args.tune)
