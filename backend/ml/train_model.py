"""
thinkSync AI - ML Training Pipeline
Trains, evaluates, and persists the Misconception Detection Classifier.
Combines TF-IDF n-gram text representations with domain-engineered mathematical features.
Outputs model artifact (model.joblib) and comprehensive metrics (metrics.json).
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
import joblib

from dataset_generator import save_dataset_csv

DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset.csv")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")
METRICS_PATH = os.path.join(os.path.dirname(__file__), "metrics.json")

def engineer_features(df):
    """
    Extracts text context and engineered behavioral/mathematical indicators.
    """
    df = df.copy()
    
    # 1. Combined text context for TF-IDF
    df["steps_clean"] = df["steps"].fillna("").astype(str)
    df["ans_clean"] = df["student_answer"].fillna("").astype(str)
    df["q_clean"] = df["question"].fillna("").astype(str)
    df["approach_clean"] = df["approach"].fillna("").astype(str)
    df["topic_clean"] = df["topic"].fillna("").astype(str)
    
    df["text_combined"] = (
        "topic: " + df["topic_clean"] + " " +
        "question: " + df["q_clean"] + " " +
        "approach: " + df["approach_clean"] + " " +
        "answer: " + df["ans_clean"] + " " +
        "steps: " + df["steps_clean"]
    )
    
    # 2. Domain & behavioral numerical features
    df["step_count"] = df["steps_clean"].apply(lambda s: len([line for line in s.split("\n") if line.strip()])).astype(float)
    df["has_negative"] = (df["ans_clean"].str.contains("-", regex=False) | df["steps_clean"].str.contains("-", regex=False)).astype(float)
    df["has_fraction"] = (df["ans_clean"].str.contains("/", regex=False) | df["steps_clean"].str.contains("/", regex=False)).astype(float)
    df["has_multiply"] = df["steps_clean"].apply(lambda s: 1.0 if ("*" in s or "x " in s or "times" in s) else 0.0)
    df["has_equal"] = df["steps_clean"].str.contains("=", regex=False).astype(float)
    df["has_percent"] = (df["ans_clean"].str.contains("%", regex=False) | df["q_clean"].str.contains("%", regex=False)).astype(float)
    df["len_answer"] = df["ans_clean"].str.len().astype(float)
    df["len_steps"] = df["steps_clean"].str.len().astype(float)
    
    # Exact match check
    df["exact_match"] = (df["ans_clean"].str.strip().str.lower() == df["correct_answer"].fillna("").astype(str).str.strip().str.lower()).astype(float)
    
    return df

def train_and_evaluate():
    print("=" * 65)
    print("      thinkSync AI - Misconception Classifier Training Pipeline")
    print("=" * 65)
    
    # Generate dataset if not present
    if not os.path.exists(DATASET_PATH):
        print(f"Generating synthetic + empirical dataset at {DATASET_PATH}...")
        save_dataset_csv(DATASET_PATH, target_size=900)
    
    df = pd.read_csv(DATASET_PATH)
    print(f"Loaded dataset: {len(df)} samples across {df['label'].nunique()} classes.")
    
    # Feature engineering
    df_feat = engineer_features(df)
    
    feature_cols = [
        "text_combined",
        "step_count",
        "has_negative",
        "has_fraction",
        "has_multiply",
        "has_equal",
        "has_percent",
        "len_answer",
        "len_steps",
        "exact_match"
    ]
    
    X = df_feat[feature_cols]
    y = df_feat["label"]
    
    # Split train/test (80/20) with stratification
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    print(f"Training set: {len(X_train)} samples | Test set: {len(X_test)} samples")
    
    # Build preprocessor
    num_cols = ["step_count", "has_negative", "has_fraction", "has_multiply", "has_equal", "has_percent", "len_answer", "len_steps", "exact_match"]
    
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "tfidf",
                TfidfVectorizer(
                    ngram_range=(1, 2),
                    max_features=2500,
                    sublinear_tf=True,
                    min_df=2
                ),
                "text_combined"
            ),
            (
                "num",
                StandardScaler(),
                num_cols
            )
        ]
    )
    
    # Model candidate 1: Logistic Regression
    pipe_lr = Pipeline([
        ("preprocessor", preprocessor),
        ("clf", LogisticRegression(C=1.5, max_iter=1000, class_weight="balanced", random_state=42))
    ])
    
    # Model candidate 2: Random Forest
    pipe_rf = Pipeline([
        ("preprocessor", preprocessor),
        ("clf", RandomForestClassifier(n_estimators=150, max_depth=16, random_state=42, class_weight="balanced"))
    ])
    
    print("\nEvaluating Model Architectures via 5-Fold Stratified Cross Validation...")
    cv_scores_lr = cross_val_score(pipe_lr, X_train, y_train, cv=5, scoring="f1_macro")
    cv_scores_rf = cross_val_score(pipe_rf, X_train, y_train, cv=5, scoring="f1_macro")
    
    print(f"Logistic Regression Macro F1: {cv_scores_lr.mean():.4f} (+/- {cv_scores_lr.std():.4f})")
    print(f"Random Forest Macro F1:       {cv_scores_rf.mean():.4f} (+/- {cv_scores_rf.std():.4f})")
    
    # Select best model
    if cv_scores_lr.mean() >= cv_scores_rf.mean():
        selected_pipe = pipe_lr
        selected_model_name = "TF-IDF + Domain Features + Logistic Regression"
    else:
        selected_pipe = pipe_rf
        selected_model_name = "TF-IDF + Domain Features + Random Forest Classifier"
        
    print(f"\n[Selection] Deploying: {selected_model_name}")
    
    # Fit selected model on full train set
    selected_pipe.fit(X_train, y_train)
    
    # Test set predictions
    y_pred = selected_pipe.predict(X_test)
    y_pred_proba = selected_pipe.predict_proba(X_test)
    
    # Metrics computation
    accuracy = accuracy_score(y_test, y_pred)
    prec_macro, rec_macro, f1_macro, _ = precision_recall_fscore_support(y_test, y_pred, average="macro", zero_division=0)
    prec_weighted, rec_weighted, f1_weighted, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted", zero_division=0)
    
    labels_order = sorted(list(selected_pipe.classes_))
    cm = confusion_matrix(y_test, y_pred, labels=labels_order).tolist()
    
    class_report_dict = classification_report(y_test, y_pred, target_names=labels_order, output_dict=True, zero_division=0)
    
    print("\n--- Test Set Classification Report ---")
    print(classification_report(y_test, y_pred, target_names=labels_order, zero_division=0))
    print(f"Overall Accuracy: {accuracy:.4f} ({accuracy * 100:.2f}%)")
    
    # Save model artifact
    joblib.dump(selected_pipe, MODEL_PATH)
    print(f"\nModel pipeline saved to: {MODEL_PATH}")
    
    # Prepare exportable metrics dictionary
    metrics_data = {
        "model_architecture": selected_model_name,
        "classes": labels_order,
        "sample_counts": {
            "total_dataset_size": len(df),
            "training_samples": len(X_train),
            "test_samples": len(X_test)
        },
        "performance": {
            "accuracy": round(float(accuracy), 4),
            "accuracy_percent": round(float(accuracy * 100), 2),
            "macro_precision": round(float(prec_macro), 4),
            "macro_recall": round(float(rec_macro), 4),
            "macro_f1": round(float(f1_macro), 4),
            "weighted_f1": round(float(f1_weighted), 4)
        },
        "confusion_matrix": {
            "labels": labels_order,
            "matrix": cm
        },
        "per_class_metrics": {
            k: {
                "precision": round(v.get("precision", 0), 4),
                "recall": round(v.get("recall", 0), 4),
                "f1_score": round(v.get("f1-score", 0), 4),
                "support": v.get("support", 0)
            }
            for k, v in class_report_dict.items() if k in labels_order
        },
        "feature_types": [
            "TF-IDF n-grams (1, 2) on Question, Answer, Steps, and Approach",
            "Domain features: step_count, has_negative, has_fraction, has_multiply, has_equal, has_percent",
            "Behavioral features: len_answer, len_steps, exact_match"
        ]
    }
    
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_data, f, indent=2)
    print(f"Model evaluation metrics saved to: {METRICS_PATH}")
    
    return selected_pipe, metrics_data

if __name__ == "__main__":
    train_and_evaluate()
