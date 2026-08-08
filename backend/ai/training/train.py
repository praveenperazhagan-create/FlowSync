"""
Model Training Script for Traffic Digital Twin Dataset
======================================================

This script loads preprocessed features and target using `preprocess.py`,
saves all fitted LabelEncoders to `ai/models/encoders.pkl`,
trains multiple algorithms (RandomForest, GradientBoosting, XGBoost if available),
compares performance metrics, selects the highest accuracy model,
saves the winning model to `ai/models/traffic_model.pkl`, and exports a detailed report
to `reports/training_report.json`.
"""

import os
import sys
import json
import joblib
import pandas as pd
import numpy as np

# Ensure current directory is in sys.path for importing preprocess module
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from preprocess import preprocess_data
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Optional XGBoost import
try:
    from xgboost import XGBClassifier
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("[INFO] XGBoost is not installed. Will compare RandomForest and GradientBoosting.")


def get_models_dir() -> str:
    base_dir = os.path.abspath(os.path.join(current_dir, ".."))
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)
    return models_dir


def get_reports_dir() -> str:
    base_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
    reports_dir = os.path.join(base_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    return reports_dir


def train_and_evaluate_model(
    test_size: float = 0.2,
    random_state: int = 42
) -> tuple[object, dict]:
    """
    Trains RandomForest, GradientBoosting, and optional XGBoost models,
    compares accuracy, precision, recall, f1, feature importance, and confusion matrix.
    Saves encoders, best model, and training_report.json.
    """
    print("="*60)
    print(" 1. LOADING & PREPROCESSING DATA ")
    print("="*60)

    # Step 1: Preprocess Data and obtain encoders
    X, y, encoders = preprocess_data(target_col="congestion_level")

    if X is None or y is None:
        raise ValueError("Preprocessing failed to return valid features (X) and target (y).")

    # Save Encoders to models/encoders.pkl
    models_dir = get_models_dir()
    encoders_path = os.path.join(models_dir, "encoders.pkl")
    joblib.dump(encoders, encoders_path)
    print(f"[SUCCESS] Saved label encoders to: {encoders_path}")

    print("\n" + "="*60)
    print(" 2. SPLITTING DATASET ")
    print("="*60)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    print(f"[INFO] Train set shape: X_train = {X_train.shape}, y_train = {y_train.shape}")
    print(f"[INFO] Test set shape : X_test  = {X_test.shape}, y_test  = {y_test.shape}")

    # Define candidate models
    candidate_models = {
        "RandomForest": RandomForestClassifier(
            n_estimators=100, max_depth=20, random_state=random_state, n_jobs=-1
        ),
        "GradientBoosting": GradientBoostingClassifier(
            n_estimators=100, max_depth=6, random_state=random_state
        )
    }

    if HAS_XGBOOST:
        candidate_models["XGBoost"] = XGBClassifier(
            n_estimators=100, max_depth=6, random_state=random_state, eval_metric="mlogloss"
        )

    print("\n" + "="*60)
    print(" 3. TRAINING & COMPARING CANDIDATE MODELS ")
    print("="*60)

    best_model_name = None
    best_model_obj = None
    best_accuracy = -1.0
    evaluation_results = {}

    for name, model in candidate_models.items():
        print(f"\n[INFO] Training model: {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        cm = confusion_matrix(y_test, y_pred).tolist()

        # Feature Importance
        feat_importance = {}
        if hasattr(model, "feature_importances_"):
            for col, imp in zip(X.columns, model.feature_importances_):
                feat_importance[col] = float(round(imp, 6))

        evaluation_results[name] = {
            "accuracy": float(round(acc, 4)),
            "precision": float(round(prec, 4)),
            "recall": float(round(rec, 4)),
            "f1_score": float(round(f1, 4)),
            "confusion_matrix": cm,
            "feature_importance": feat_importance
        }

        print(f"[{name}] Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1: {f1:.4f}")

        if acc > best_accuracy:
            best_accuracy = acc
            best_model_name = name
            best_model_obj = model

    print("\n" + "="*60)
    print(f" BEST MODEL SELECTED: {best_model_name} (Accuracy: {best_accuracy*100:.2f}%) ")
    print("="*60)

    # Save Best Model to ai/models/traffic_model.pkl
    best_model_path = os.path.join(models_dir, "traffic_model.pkl")
    joblib.dump(best_model_obj, best_model_path)
    print(f"[SUCCESS] Saved best model ({best_model_name}) to: {best_model_path}")

    # Generate reports/training_report.json
    reports_dir = get_reports_dir()
    report_path = os.path.join(reports_dir, "training_report.json")

    report_payload = {
        "best_model": best_model_name,
        "best_accuracy": best_accuracy,
        "models_evaluated": evaluation_results
    }

    with open(report_path, "w") as f:
        json.dump(report_payload, f, indent=2)

    print(f"[SUCCESS] Training report saved to: {report_path}")

    return best_model_obj, evaluation_results[best_model_name]


if __name__ == "__main__":
    train_and_evaluate_model()
