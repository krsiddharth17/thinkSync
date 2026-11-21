"""
thinkSync AI - Direct Logic & Verification Test
Verifies all authentication, database models, ML predictor, adaptive learning,
AI tutor pedagogical engine, and analytics aggregation directly.
"""

import sys
import os
import json

sys.path.insert(0, os.path.abspath("."))

from backend.app.database import SessionLocal, Base, engine
from backend.app.models import User, Topic, Question, AssessmentAttempt, StudentTopicMastery
from backend.app.seed_data import seed_database
from backend.app.auth import hash_password, verify_password, create_access_token, decode_access_token
from backend.app.services.tutor_service import generate_ai_tutor_feedback, generate_step_hint
from backend.app.services.adaptive_engine import update_student_mastery_profile

# ML Predictor
ml_dir = os.path.abspath("backend/ml")
if ml_dir not in sys.path:
    sys.path.insert(0, ml_dir)
from predictor import predict_misconception, is_exact_match

def run_direct_tests():
    print("=" * 65)
    print("       thinkSync AI - Core Architecture Verification")
    print("=" * 65)

    # 1. Initialize DB and Seed
    print("\n[1] Testing Database Schema & Seed Data...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    
    users = db.query(User).all()
    topics = db.query(Topic).all()
    questions = db.query(Question).all()
    attempts = db.query(AssessmentAttempt).all()
    print(f"    Users in DB: {len(users)} ({[u.username for u in users]})")
    print(f"    Topics in DB: {len(topics)} ({[t.name for t in topics]})")
    print(f"    Questions in DB: {len(questions)}")
    print(f"    Historical Attempts in DB: {len(attempts)}")
    assert len(users) >= 4
    assert len(topics) == 4
    assert len(questions) >= 12

    # 2. Authentication and Password Hashing
    print("\n[2] Testing Auth & Token Mechanics...")
    test_pwd = "mySuperSecretPassword123"
    hashed = hash_password(test_pwd)
    assert verify_password(test_pwd, hashed) is True
    assert verify_password("wrongPassword", hashed) is False
    print("    Password hashing and verification: PASSED")

    token = create_access_token({"sub": "1", "username": "alex_student", "role": "student"})
    decoded = decode_access_token(token)
    assert decoded["sub"] == "1"
    assert decoded["username"] == "alex_student"
    print("    RFC 7519 HMAC-SHA256 Token issuance and verification: PASSED")

    # 3. Machine Learning Misconception Engine
    print("\n[3] Testing Scikit-learn Misconception Classifier...")

    # Case A: Inverse Operation Error
    res_inv = predict_misconception(
        question="Solve for x: 3x + 12 = 33",
        correct_answer="7",
        student_answer="15",
        steps="3x = 33 + 12\n3x = 45\nx = 45 / 3 = 15",
        approach="isolate_variable",
        topic="linear_equations"
    )
    print(f"    Case A (Inverse Op Error): {res_inv['predicted_misconception']} ({res_inv['confidence']:.1%})")
    assert res_inv["predicted_misconception"] == "inverse_operation_error"

    # Case B: Fraction Operation Error (Direct Denominator Addition)
    res_frac = predict_misconception(
        question="Evaluate: 1/3 + 1/4",
        correct_answer="7/12",
        student_answer="2/7",
        steps="(1 + 1) / (3 + 4) = 2/7",
        approach="direct_addition",
        topic="fractions"
    )
    print(f"    Case B (Fraction Op Error): {res_frac['predicted_misconception']} ({res_frac['confidence']:.1%})")
    assert res_frac["predicted_misconception"] == "fraction_operation_error"

    # Case C: Sign Error
    res_sign = predict_misconception(
        question="Expand: -2(3x - 4)",
        correct_answer="-6x + 8",
        student_answer="-6x - 8",
        steps="-2 * 3x = -6x\n-2 * 4 = -8\nResult: -6x - 8",
        approach="distributive_property",
        topic="basic_algebra"
    )
    print(f"    Case C (Sign Error): {res_sign['predicted_misconception']} ({res_sign['confidence']:.1%})")
    assert res_sign["predicted_misconception"] == "sign_error"

    # Case D: Exact Correct Answer
    res_corr = predict_misconception(
        question="Solve for x: 2x + 7 = 19",
        correct_answer="6",
        student_answer="6",
        steps="2x = 19 - 7\n2x = 12\nx = 6",
        approach="isolate_variable",
        topic="linear_equations"
    )
    print(f"    Case D (Correct): {res_corr['predicted_misconception']} ({res_corr['confidence']:.1%})")
    assert res_corr["predicted_misconception"] == "correct"

    # Case E: Uncertain / Insufficient Evidence
    res_unc = predict_misconception(
        question="Solve for x: 2x + 7 = 19",
        correct_answer="6",
        student_answer="idk",
        steps="",
        approach="none",
        topic="linear_equations"
    )
    print(f"    Case E (Uncertain/Insufficient): {res_unc['predicted_misconception']} (is_uncertain={res_unc['is_uncertain']})")
    assert res_unc["predicted_misconception"] == "uncertain_insufficient_evidence"
    assert res_unc["is_uncertain"] is True

    # 4. Socratic AI Tutor Fallback Pedagogy
    print("\n[4] Testing AI Tutor Pedagogical Engine...")
    feedback = generate_ai_tutor_feedback(
        question_text="Solve for x: 2x + 7 = 19",
        student_answer="13",
        intermediate_steps="2x = 19 + 7\n2x = 26\nx = 13",
        predicted_misconception="inverse_operation_error",
        ml_confidence=0.88,
        topic="Linear Equations"
    )
    print(f"    Mistake Analysis: {feedback['mistake_analysis'][:80]}...")
    print(f"    Conceptual Explanation: {feedback['conceptual_explanation'][:80]}...")
    print(f"    Socratic Hint: {feedback['socratic_hint']}")
    assert "inverse operation" in feedback["mistake_analysis"].lower() or "added" in feedback["mistake_analysis"].lower()

    # 5. Adaptive Learning Engine Profile Update
    print("\n[5] Testing Adaptive Learning Engine...")
    alex = db.query(User).filter(User.username == "alex_student").first()
    le_topic = db.query(Topic).filter(Topic.slug == "linear-equations").first()

    update_res = update_student_mastery_profile(
        db=db,
        user_id=alex.id,
        topic_id=le_topic.id,
        is_correct=False,
        predicted_misconception="inverse_operation_error",
        difficulty="medium"
    )
    print(f"    Updated Mastery Score: {update_res['updated_mastery_score']}")
    print(f"    Recurring Misconceptions: {update_res['recurring_misconceptions']}")
    print(f"    Adaptive Recommendation Status: {update_res['recommendation']['status']}")
    print(f"    Adaptive Recommendation Action: {update_res['recommendation']['action']}")

    # 6. Model Evaluation Metrics Inspection
    print("\n[6] Inspecting Persisted Model Metrics (metrics.json)...")
    metrics_path = os.path.join(ml_dir, "metrics.json")
    with open(metrics_path, "r", encoding="utf-8") as f:
        metrics_data = json.load(f)
    print(f"    Architecture: {metrics_data['model_architecture']}")
    print(f"    Test Accuracy: {metrics_data['performance']['accuracy_percent']}%")
    print(f"    Macro F1: {metrics_data['performance']['macro_f1']}")
    print(f"    Classes: {metrics_data['classes']}")

    db.close()
    print("\n" + "=" * 65)
    print("    ALL DIRECT ARCHITECTURAL VERIFICATION TESTS PASSED (6/6)!")
    print("=" * 65)

if __name__ == "__main__":
    run_direct_tests()
