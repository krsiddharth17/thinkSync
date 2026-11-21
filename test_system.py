"""
thinkSync AI - Full End-to-End Test Suite
Tests API endpoints, database operations, auth tokens, ML misconception classification,
AI tutor responses, and adaptive engine updates directly.
"""

import sys
import os

# Add workspace to path
sys.path.insert(0, os.path.abspath("."))

from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.database import SessionLocal, Base, engine
from backend.app.seed_data import seed_database

def run_tests():
    print("=" * 60)
    print("      thinkSync AI - End-to-End System Test Suite")
    print("=" * 60)

    # Initialize DB & Seed
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_database(db)
    db.close()

    client = TestClient(app)

    # 1. Health check
    print("\n[1] Testing Health Check (/api/health)...")
    res = client.get("/api/health")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.text}"
    health_data = res.json()
    print(f"    Status: {health_data['status']} | ML Engine: {health_data['ml_engine']}")

    # 2. Student Authentication
    print("\n[2] Testing Student Login (/api/auth/login)...")
    res = client.post("/api/auth/login", json={"username": "alex_student", "password": "student123"})
    assert res.status_code == 200, f"Login failed: {res.text}"
    login_data = res.json()
    student_token = login_data["access_token"]
    student_headers = {"Authorization": f"Bearer {student_token}"}
    print(f"    Authenticated as: {login_data['user']['full_name']} (Role: {login_data['user']['role']})")

    # 3. Teacher Authentication
    print("\n[3] Testing Teacher Login (/api/auth/login)...")
    res = client.post("/api/auth/login", json={"username": "sarah_teacher", "password": "teacher123"})
    assert res.status_code == 200, f"Teacher login failed: {res.text}"
    teacher_token = res.json()["access_token"]
    teacher_headers = {"Authorization": f"Bearer {teacher_token}"}
    print(f"    Authenticated as: {res.json()['user']['full_name']} (Role: {res.json()['user']['role']})")

    # 4. Topics Listing
    print("\n[4] Testing Topics Listing (/api/topics)...")
    res = client.get("/api/topics", headers=student_headers)
    assert res.status_code == 200
    topics = res.json()
    print(f"    Loaded {len(topics)} topics: {[t['name'] for t in topics]}")

    # 5. Fetch Topic Questions
    print("\n[5] Testing Questions Retrieval (/api/topics/linear-equations/questions)...")
    res = client.get("/api/topics/linear-equations/questions")
    assert res.status_code == 200
    questions = res.json()
    assert len(questions) > 0
    target_q = questions[0]
    print(f"    Question 1: {target_q['question_text']}")

    # 6. Submit Assessment with Inverse Operation Misconception
    print("\n[6] Testing ML Misconception Evaluation (/api/assessment/evaluate)...")
    # Solving 2x + 7 = 19 with 2x = 26 -> x = 13
    eval_payload = {
        "question_id": target_q["id"],
        "student_answer": "13",
        "intermediate_steps": "2x = 19 + 7\n2x = 26\nx = 13",
        "approach_selected": "Isolate variable using inverse operations",
        "time_taken_seconds": 35
    }
    res = client.post("/api/assessment/evaluate", json=eval_payload, headers=student_headers)
    assert res.status_code == 200, f"Evaluation failed: {res.text}"
    eval_res = res.json()
    print(f"    Correct: {eval_res['is_correct']}")
    print(f"    ML Diagnosed Misconception: {eval_res['misconception_title']} (Confidence: {eval_res['ml_confidence']:.1%})")
    assert eval_res["predicted_misconception"] == "inverse_operation_error", f"Expected inverse_operation_error, got {eval_res['predicted_misconception']}"
    print(f"    AI Tutor Mistake Analysis: {eval_res['ai_feedback']['mistake_analysis'][:80]}...")
    print(f"    Updated Mastery Score: {eval_res['updated_topic_mastery']}")

    # 7. Submit Assessment with Exact Correct Answer
    print("\n[7] Testing Correct Answer Submission...")
    eval_payload_correct = {
        "question_id": target_q["id"],
        "student_answer": "6",
        "intermediate_steps": "2x = 19 - 7\n2x = 12\nx = 6",
        "approach_selected": "Isolate variable using inverse operations",
        "time_taken_seconds": 22
    }
    res = client.post("/api/assessment/evaluate", json=eval_payload_correct, headers=student_headers)
    assert res.status_code == 200
    eval_res_correct = res.json()
    print(f"    Correct: {eval_res_correct['is_correct']}")
    print(f"    Predicted Label: {eval_res_correct['predicted_misconception']}")
    assert eval_res_correct["is_correct"] is True

    # 8. Student Dashboard Analytics
    print("\n[8] Testing Student Dashboard (/api/student/dashboard)...")
    res = client.get("/api/student/dashboard", headers=student_headers)
    assert res.status_code == 200
    dash_data = res.json()
    print(f"    Student Overall Accuracy: {dash_data['overview']['overall_accuracy']}%")
    print(f"    Total Recorded Attempts: {dash_data['overview']['total_attempts']}")
    print(f"    Top Bottleneck: {dash_data['overview']['top_bottleneck']}")

    # 9. Teacher Dashboard Analytics
    print("\n[9] Testing Teacher Dashboard (/api/teacher/dashboard)...")
    res = client.get("/api/teacher/dashboard", headers=teacher_headers)
    assert res.status_code == 200
    t_dash = res.json()
    print(f"    Total Students: {t_dash['overview']['total_students']}")
    print(f"    Classroom Average Mastery: {t_dash['overview']['average_mastery']}%")
    print(f"    Classroom Top Misconception: {t_dash['overview']['top_recurring_misconception']}")
    print(f"    Student Roster Count: {len(t_dash['students'])}")

    # 10. ML Metrics & Direct Predict
    print("\n[10] Testing Direct ML Metrics & Predict (/api/ml/metrics)...")
    res = client.get("/api/ml/metrics")
    assert res.status_code == 200
    metrics = res.json()
    print(f"    Architecture: {metrics['model_architecture']}")
    print(f"    Accuracy: {metrics['performance']['accuracy_percent']}%")
    print(f"    Macro F1: {metrics['performance']['macro_f1']}")

    # Direct predict live endpoint
    predict_payload = {
        "topic": "fractions",
        "question": "Evaluate: 1/3 + 1/4",
        "correct_answer": "7/12",
        "student_answer": "2/7",
        "steps": "(1 + 1) / (3 + 4) = 2/7",
        "approach": "direct_addition"
    }
    res = client.post("/api/ml/predict", json=predict_payload)
    assert res.status_code == 200
    pred = res.json()
    print(f"    Live ML Direct Predict: {pred['predicted_misconception']} ({pred['confidence']:.1%})")
    assert pred["predicted_misconception"] == "fraction_operation_error"

    print("\n" + "=" * 60)
    print("  ALL 10 VERIFICATION TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
