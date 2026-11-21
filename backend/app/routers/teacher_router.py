import json
from collections import Counter
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User, Topic, Question, AssessmentAttempt, StudentTopicMastery
from ..auth import get_current_teacher

router = APIRouter(prefix="/teacher", tags=["Teacher & Administrator Analytics"])

@router.get("/dashboard")
def get_teacher_dashboard(
    current_teacher: User = Depends(get_current_teacher),
    db: Session = Depends(get_db)
):
    # 1. High-Level Metrics
    students = db.query(User).filter(User.role == "student").all()
    total_students = len(students)
    all_attempts = db.query(AssessmentAttempt).all()
    total_assessments = len(all_attempts)
    correct_count = sum(1 for a in all_attempts if a.is_correct)
    class_accuracy = round((correct_count / total_assessments * 100), 1) if total_assessments > 0 else 0.0

    all_masteries = db.query(StudentTopicMastery).all()
    avg_mastery = (
        round(sum(m.mastery_score for m in all_masteries) / len(all_masteries), 1)
        if all_masteries else 0.0
    )

    # 2. Classroom-Wide Misconception Aggregation
    misconception_counter = Counter()
    for a in all_attempts:
        if not a.is_correct and a.predicted_misconception and a.predicted_misconception not in ["correct", "none"]:
            misconception_counter[a.predicted_misconception] += 1

    misconception_names = {
        "inverse_operation_error": "Inverse Op Errors",
        "sign_error": "Sign / Integer Errors",
        "arithmetic_calculation_error": "Arithmetic Slips",
        "multiplication_division_error": "Mult / Div Inversions",
        "conceptual_misunderstanding": "Conceptual Misunderstandings",
        "fraction_operation_error": "Fraction Op Errors",
        "uncertain_insufficient_evidence": "Uncertain / Insufficient"
    }

    class_misconception_data = [
        {
            "category": k,
            "name": misconception_names.get(k, k.replace("_", " ").title()),
            "count": v,
            "percentage": round((v / (total_assessments - correct_count) * 100), 1) if (total_assessments - correct_count) > 0 else 0.0
        }
        for k, v in misconception_counter.most_common()
    ]

    # 3. Topic & Question Difficulty Breakdown (Where students get stuck)
    topics = db.query(Topic).all()
    topic_difficulty_stats = []
    for t in topics:
        q_ids = [q.id for q in db.query(Question.id).filter(Question.topic_id == t.id).all()]
        t_attempts = [a for a in all_attempts if a.question_id in q_ids]
        t_total = len(t_attempts)
        t_correct = sum(1 for a in t_attempts if a.is_correct)
        t_acc = round((t_correct / t_total * 100), 1) if t_total > 0 else 0.0
        
        # Primary misconception in this topic
        t_mis_counter = Counter(a.predicted_misconception for a in t_attempts if not a.is_correct and a.predicted_misconception != "correct")
        top_topic_mis = t_mis_counter.most_common(1)[0][0] if t_mis_counter else "None"

        topic_difficulty_stats.append({
            "topic_id": t.id,
            "name": t.name,
            "total_attempts": t_total,
            "accuracy": t_acc,
            "error_rate": round(100.0 - t_acc, 1) if t_total > 0 else 0.0,
            "primary_misconception": misconception_names.get(top_topic_mis, top_topic_mis)
        })

    # Sort topics by highest error rate first
    topic_difficulty_stats.sort(key=lambda x: x["error_rate"], reverse=True)

    # 4. Student Roster with Diagnostic Alerts
    student_roster = []
    for s in students:
        s_attempts = [a for a in all_attempts if a.user_id == s.id]
        s_total = len(s_attempts)
        s_correct = sum(1 for a in s_attempts if a.is_correct)
        s_acc = round((s_correct / s_total * 100), 1) if s_total > 0 else 0.0

        s_masteries = [m for m in all_masteries if m.user_id == s.id]
        s_avg_mastery = round(sum(m.mastery_score for m in s_masteries) / len(s_masteries), 1) if s_masteries else 0.0

        # Find student's primary bottleneck
        s_mis_counter = Counter(a.predicted_misconception for a in s_attempts if not a.is_correct and a.predicted_misconception != "correct")
        top_s_mis = s_mis_counter.most_common(1)[0] if s_mis_counter else None
        
        # Determine intervention recommendation
        needs_intervention = False
        intervention_action = "On Track"
        if s_avg_mastery < 50.0 or (top_s_mis and top_s_mis[1] >= 2):
            needs_intervention = True
            if top_s_mis:
                intervention_action = f"Targeted review on {misconception_names.get(top_s_mis[0], top_s_mis[0])}"
            else:
                intervention_action = "General foundational concept review"

        student_roster.append({
            "student_id": s.id,
            "username": s.username,
            "full_name": s.full_name or s.username,
            "grade": s.grade,
            "total_attempts": s_total,
            "accuracy": s_acc,
            "average_mastery": s_avg_mastery,
            "top_bottleneck": misconception_names.get(top_s_mis[0], top_s_mis[0]) if top_s_mis else "None detected",
            "bottleneck_count": top_s_mis[1] if top_s_mis else 0,
            "needs_intervention": needs_intervention,
            "intervention_action": intervention_action
        })

    # Sort students so those needing intervention appear first
    student_roster.sort(key=lambda x: (not x["needs_intervention"], x["average_mastery"]))

    # 5. Recent Submissions Stream
    recent_stream = (
        db.query(AssessmentAttempt)
        .order_by(AssessmentAttempt.created_at.desc())
        .limit(12)
        .all()
    )
    stream_data = []
    for a in recent_stream:
        u = db.query(User).filter(User.id == a.user_id).first()
        q = db.query(Question).filter(Question.id == a.question_id).first()
        t = db.query(Topic).filter(Topic.id == q.topic_id).first() if q else None

        stream_data.append({
            "attempt_id": a.id,
            "student_name": u.full_name or u.username if u else "Student",
            "topic_name": t.name if t else "Math",
            "question_text": q.question_text if q else "Question",
            "student_answer": a.student_answer,
            "is_correct": a.is_correct,
            "predicted_misconception": a.predicted_misconception,
            "ml_confidence": round(a.ml_confidence * 100, 1),
            "created_at": a.created_at.strftime("%b %d, %I:%M %p")
        })

    return {
        "overview": {
            "total_students": total_students,
            "total_assessments": total_assessments,
            "class_accuracy": class_accuracy,
            "average_mastery": avg_mastery,
            "top_recurring_misconception": class_misconception_data[0]["name"] if class_misconception_data else "None"
        },
        "misconception_distribution": class_misconception_data,
        "topics_difficulty": topic_difficulty_stats,
        "students": student_roster,
        "recent_stream": stream_data
    }
