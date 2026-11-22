"""
thinkSync AI - ML Misconception Predictor Service
Provides production inference for student submissions.
Performs feature engineering, handles edge cases, applies probability calibration,
and detects uncertain / insufficient evidence.
"""

import os
import re
import numpy as np
import pandas as pd
import joblib

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.joblib")
DATASET_PATH = os.path.join(os.path.dirname(__file__), "dataset.csv")

# Global cached model
_cached_pipeline = None

try:
    from .train_model import engineer_features, train_and_evaluate
except (ImportError, ValueError):
    try:
        from backend.ml.train_model import engineer_features, train_and_evaluate
    except (ImportError, ValueError):
        from train_model import engineer_features, train_and_evaluate

MISCONCEPTION_METADATA = {
    "inverse_operation_error": {
        "title": "Inverse Operation Error",
        "description": "Student performed the inverse of the required mathematical operation (e.g., adding instead of subtracting to isolate a variable, or multiplying instead of dividing).",
        "severity": "medium",
        "prerequisite_concept": "Balancing Equations & Inverse Operations"
    },
    "sign_error": {
        "title": "Sign / Integer Arithmetic Error",
        "description": "Student dropped, misapplied, or incorrectly combined negative signs (e.g. failing to distribute negatives or incorrect negative division).",
        "severity": "medium",
        "prerequisite_concept": "Negative Numbers & Distributive Property"
    },
    "arithmetic_calculation_error": {
        "title": "Arithmetic Calculation Slip",
        "description": "The student set up the algebraic logic correctly, but made an inadvertent computational slip in basic mental math or multiplication tables.",
        "severity": "low",
        "prerequisite_concept": "Careful Scratchpad Verification"
    },
    "multiplication_division_error": {
        "title": "Multiplication / Division Inversion",
        "description": "Inverted numerator and denominator, inverted division order, or failed to multiply by the reciprocal.",
        "severity": "high",
        "prerequisite_concept": "Reciprocals & Fraction Scaling"
    },
    "conceptual_misunderstanding": {
        "title": "Core Conceptual Misunderstanding",
        "description": "Fundamental misunderstanding of rules (e.g. combining unlike terms like 3x + 4 = 7x, violating PEMDAS order of operations, or treating percent as simple subtraction).",
        "severity": "high",
        "prerequisite_concept": "Terms, Coefficients, and Mathematical Meaning"
    },
    "fraction_operation_error": {
        "title": "Fraction Operation Error",
        "description": "Direct addition/subtraction of denominators across fractions without finding a common denominator, or multiplying across in division.",
        "severity": "high",
        "prerequisite_concept": "Common Denominators & Visual Fraction Parts"
    },
    "correct": {
        "title": "Correct Solution",
        "description": "The student reached the correct answer through a valid mathematical sequence.",
        "severity": "none",
        "prerequisite_concept": "Mastered"
    },
    "uncertain_insufficient_evidence": {
        "title": "Uncertain / Insufficient Evidence",
        "description": "The student provided an ambiguous, incomplete, or uninformative response that lacks enough diagnostic steps to isolate a root misconception.",
        "severity": "informational",
        "prerequisite_concept": "Show Intermediate Steps"
    }
}

def get_model():
    global _cached_pipeline
    if _cached_pipeline is None:
        if not os.path.exists(MODEL_PATH):
            pipe, _ = train_and_evaluate()
            _cached_pipeline = pipe
        else:
            _cached_pipeline = joblib.load(MODEL_PATH)
    return _cached_pipeline

def clean_num_str(val):
    if not val:
        return ""
    return str(val).strip().replace(" ", "")

def is_exact_match(student_ans, correct_ans):
    s = clean_num_str(student_ans).lower()
    c = clean_num_str(correct_ans).lower()
    if not s or not c:
        return False
    if s == c:
        return True
    # Try float parsing
    try:
        if abs(float(s) - float(c)) < 1e-4:
            return True
    except (ValueError, TypeError):
        pass
    return False

def predict_misconception(
    question: str,
    correct_answer: str,
    student_answer: str,
    steps: str = "",
    approach: str = "standard",
    topic: str = "general"
) -> dict:
    """
    Evaluates student submission using the trained Scikit-learn model.
    Returns predicted misconception category, confidence score, and explainability breakdown.
    """
    model = get_model()
    
    # 1. Edge Case: Empty or Insufficient Evidence Check
    clean_ans = (student_answer or "").strip()
    clean_steps = (steps or "").strip()
    
    if len(clean_ans) == 0:
        return {
            "predicted_misconception": "uncertain_insufficient_evidence",
            "confidence": 1.0,
            "is_uncertain": True,
            "metadata": MISCONCEPTION_METADATA["uncertain_insufficient_evidence"],
            "class_probabilities": {"uncertain_insufficient_evidence": 1.0},
            "reason": "No student answer was provided."
        }
        
    # Check for gibberish / low-effort tokens
    low_effort_tokens = ["idk", "dont know", "don't know", "?", "help", "pass", "abc", "asdf"]
    if clean_ans.lower() in low_effort_tokens and len(clean_steps) < 5:
        return {
            "predicted_misconception": "uncertain_insufficient_evidence",
            "confidence": 0.95,
            "is_uncertain": True,
            "metadata": MISCONCEPTION_METADATA["uncertain_insufficient_evidence"],
            "class_probabilities": {"uncertain_insufficient_evidence": 0.95},
            "reason": "Insufficient intermediate steps or answer detail to identify a misconception pattern."
        }
        
    # 2. Check for exact correct match
    exact_correct = is_exact_match(clean_ans, correct_answer)
    
    # 3. Engineer row for model input
    df_single = pd.DataFrame([{
        "topic": topic,
        "question": question,
        "correct_answer": correct_answer,
        "student_answer": clean_ans,
        "steps": clean_steps,
        "approach": approach
    }])
    
    df_feat = engineer_features(df_single)
    
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
    
    X_input = df_feat[feature_cols]
    
    # 4. Model Prediction
    classes = list(model.classes_)
    proba = model.predict_proba(X_input)[0]
    pred_idx = int(np.argmax(proba))
    top_class = classes[pred_idx]
    top_conf = float(proba[pred_idx])
    
    proba_dict = {cls_name: round(float(p), 4) for cls_name, p in sorted(zip(classes, proba), key=lambda x: x[1], reverse=True)}
    
    # If the answer is demonstrably correct, ensure "correct" is assigned unless strong step error
    if exact_correct and top_class != "correct":
        # Check if probability of correct is reasonably high or steps look normal
        if proba_dict.get("correct", 0) > 0.20 or len(clean_steps) < 15:
            top_class = "correct"
            top_conf = max(top_conf, 0.90)
            proba_dict["correct"] = 0.90
            
    # 5. Check Uncertainty Threshold
    # If the top confidence is lower than 0.35, the model is not confident enough
    is_uncertain = False
    if top_conf < 0.35 and not exact_correct:
        top_class = "uncertain_insufficient_evidence"
        is_uncertain = True
        
    meta = MISCONCEPTION_METADATA.get(top_class, MISCONCEPTION_METADATA["uncertain_insufficient_evidence"])
    
    return {
        "predicted_misconception": top_class,
        "confidence": round(top_conf, 4),
        "is_uncertain": is_uncertain,
        "metadata": meta,
        "class_probabilities": proba_dict,
        "reason": f"Classified with {round(top_conf * 100, 1)}% confidence based on intermediate steps, sign analysis, and operation pattern."
    }

if __name__ == "__main__":
    # Quick sanity test
    test_res = predict_misconception(
        question="Solve for x: 2x + 7 = 19",
        correct_answer="6",
        student_answer="13",
        steps="2x = 19 + 7\n2x = 26\nx = 13",
        approach="isolate_variable",
        topic="linear_equations"
    )
    print("Test Prediction:")
    print(test_res)
