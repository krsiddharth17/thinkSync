import json
from collections import Counter
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Topic, Question, AssessmentAttempt, StudentTopicMastery
from ..auth import get_current_user

router = APIRouter(prefix="/student", tags=["Student Analytics"])

@router.get("/dashboard")
def get_student_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Topic Masteries
    topics = db.query(Topic).all()
    masteries = db.query(StudentTopicMastery).filter(StudentTopicMastery.user_id == current_user.id).all()
    mastery_map = {m.topic_id: m for m in masteries}

    topic_summaries = []
    total_mastery_sum = 0.0
    topics_mastered = 0
    topics_improving = 0

    for t in topics:
        m = mastery_map.get(t.id)
        score = m.mastery_score if m else 0.0
        attempts_cnt = m.attempts_count if m else 0
        correct_cnt = m.correct_count if m else 0
        
        try:
            mis_dict = json.loads(m.recurring_misconceptions or "{}") if m else {}
        except Exception:
            mis_dict = {}

        total_mastery_sum += score
        if score >= 75.0:
            topics_mastered += 1
        elif score > 0:
            topics_improving += 1

        topic_summaries.append({
            "topic_id": t.id,
            "topic_name": t.name,
            "topic_slug": t.slug,
            "icon": t.icon,
            "mastery_score": score,
            "attempts_count": attempts_cnt,
            "correct_count": correct_cnt,
            "accuracy": round((correct_cnt / attempts_cnt * 100), 1) if attempts_cnt > 0 else 0.0,
            "recurring_misconceptions": mis_dict
        })

    avg_mastery = round(total_mastery_sum / len(topics), 1) if topics else 0.0

    # 2. All Attempts & Misconception Breakdown
    attempts = (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.user_id == current_user.id)
        .order_by(AssessmentAttempt.created_at.asc())
        .all()
    )

    total_attempts = len(attempts)
    correct_attempts = sum(1 for a in attempts if a.is_correct)
    overall_accuracy = round((correct_attempts / total_attempts * 100), 1) if total_attempts > 0 else 0.0

    # Misconception counts
    misconception_counter = Counter()
    for a in attempts:
        if not a.is_correct and a.predicted_misconception and a.predicted_misconception not in ["correct", "none"]:
            misconception_counter[a.predicted_misconception] += 1

    # Format for Recharts radar/bar chart
    misconception_labels = {
        "inverse_operation_error": "Inverse Op Errors",
        "sign_error": "Sign / Integer Errors",
        "arithmetic_calculation_error": "Arithmetic Slips",
        "multiplication_division_error": "Mult / Div Inversions",
        "conceptual_misunderstanding": "Conceptual Misunderstandings",
        "fraction_operation_error": "Fraction Op Errors",
        "uncertain_insufficient_evidence": "Uncertain Steps"
    }

    misconception_chart_data = [
        {
            "category": key,
            "name": name,
            "count": misconception_counter[key]
        }
        for key, name in misconception_labels.items()
    ]

    # 3. Learning Progress Timeline (Chronological Attempts)
    timeline_data = []
    running_correct = 0
    for idx, a in enumerate(attempts):
        if a.is_correct:
            running_correct += 1
        cum_acc = round((running_correct / (idx + 1)) * 100, 1)
        timeline_data.append({
            "attempt_number": idx + 1,
            "date": a.created_at.strftime("%b %d, %H:%M"),
            "is_correct": a.is_correct,
            "misconception": a.predicted_misconception,
            "cumulative_accuracy": cum_acc,
            "confidence": round(a.ml_confidence * 100, 1)
        })

    # 4. Recent Diagnostic Activity (last 10 reverse order)
    recent_attempts = (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.user_id == current_user.id)
        .order_by(AssessmentAttempt.created_at.desc())
        .limit(10)
        .all()
    )

    recent_activity = []
    for a in recent_attempts:
        q = db.query(Question).filter(Question.id == a.question_id).first()
        t = db.query(Topic).filter(Topic.id == q.topic_id).first() if q else None
        
        try:
            feedback_data = json.loads(a.ai_feedback or "{}")
        except Exception:
            feedback_data = {}

        recent_activity.append({
            "attempt_id": a.id,
            "question_text": q.question_text if q else "Question",
            "topic_name": t.name if t else "Mathematics",
            "student_answer": a.student_answer,
            "intermediate_steps": a.intermediate_steps,
            "is_correct": a.is_correct,
            "predicted_misconception": a.predicted_misconception,
            "ml_confidence": round(a.ml_confidence * 100, 1),
            "created_at": a.created_at.strftime("%b %d, %I:%M %p"),
            "feedback": feedback_data
        })

    # 5. Top Cognitive Bottleneck for Student
    top_misconception = None
    if misconception_counter:
        most_common = misconception_counter.most_common(1)[0]
        top_misconception = {
            "key": most_common[0],
            "name": misconception_labels.get(most_common[0], most_common[0].replace("_", " ").title()),
            "count": most_common[1]
        }

    return {
        "user_profile": {
            "id": current_user.id,
            "username": current_user.username,
            "full_name": current_user.full_name,
            "grade": current_user.grade,
            "role": current_user.role
        },
        "overview": {
            "average_mastery": avg_mastery,
            "total_attempts": total_attempts,
            "correct_attempts": correct_attempts,
            "overall_accuracy": overall_accuracy,
            "topics_mastered": topics_mastered,
            "topics_improving": topics_improving,
            "total_topics": len(topics),
            "top_bottleneck": top_misconception
        },
        "topics": topic_summaries,
        "misconception_distribution": misconception_chart_data,
        "timeline": timeline_data,
        "recent_activity": recent_activity
    }
