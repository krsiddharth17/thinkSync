"""
thinkSync AI - Adaptive Learning Engine
Maintains student mastery profiles, monitors recurring cognitive bottlenecks,
and dynamically adjusts learning pathways and question difficulty.
"""

import json
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import StudentTopicMastery, AssessmentAttempt, Question, Topic

DIFFICULTY_LADDER = ["easy", "medium", "hard"]

def update_student_mastery_profile(
    db: Session,
    user_id: int,
    topic_id: int,
    is_correct: bool,
    predicted_misconception: str,
    difficulty: str = "medium"
) -> dict:
    """
    Updates the student's mastery score and misconception frequency vector.
    Returns adaptive recommendations for the student's next step.
    """
    # Find or create mastery record
    mastery_record = (
        db.query(StudentTopicMastery)
        .filter(StudentTopicMastery.user_id == user_id, StudentTopicMastery.topic_id == topic_id)
        .first()
    )
    
    if not mastery_record:
        mastery_record = StudentTopicMastery(
            user_id=user_id,
            topic_id=topic_id,
            mastery_score=10.0 if not is_correct else 25.0,
            attempts_count=0,
            correct_count=0,
            recurring_misconceptions="{}"
        )
        db.add(mastery_record)
        db.flush()

    # Parse recurring misconceptions
    try:
        misconception_dict = json.loads(mastery_record.recurring_misconceptions or "{}")
    except Exception:
        misconception_dict = {}

    mastery_record.attempts_count += 1
    mastery_record.last_practiced = datetime.utcnow()

    difficulty_weights = {"easy": 1.0, "medium": 1.5, "hard": 2.0}
    weight = difficulty_weights.get(difficulty.lower(), 1.0)

    if is_correct:
        mastery_record.correct_count += 1
        # Boost score with diminishing returns as it nears 100
        gain = 15.0 * weight * (1.0 - (mastery_record.mastery_score / 120.0))
        mastery_record.mastery_score = min(100.0, mastery_record.mastery_score + gain)
    else:
        # Increment misconception count
        if predicted_misconception and predicted_misconception not in ["none", "correct", "uncertain_insufficient_evidence"]:
            misconception_dict[predicted_misconception] = misconception_dict.get(predicted_misconception, 0) + 1
        
        # Moderate penalty
        loss = 8.0 * weight
        mastery_record.mastery_score = max(5.0, mastery_record.mastery_score - loss)

    mastery_record.recurring_misconceptions = json.dumps(misconception_dict)
    mastery_record.mastery_score = round(mastery_record.mastery_score, 1)
    db.commit()
    db.refresh(mastery_record)

    # Generate Adaptive Recommendation
    recommendation = generate_adaptive_path(
        mastery_score=mastery_record.mastery_score,
        misconception_dict=misconception_dict,
        current_difficulty=difficulty,
        last_is_correct=is_correct,
        last_misconception=predicted_misconception
    )

    return {
        "updated_mastery_score": mastery_record.mastery_score,
        "attempts_count": mastery_record.attempts_count,
        "correct_count": mastery_record.correct_count,
        "recurring_misconceptions": misconception_dict,
        "recommendation": recommendation
    }

def generate_adaptive_path(
    mastery_score: float,
    misconception_dict: dict,
    current_difficulty: str,
    last_is_correct: bool,
    last_misconception: str
) -> dict:
    """
    Computes optimal next difficulty, recommended remediation, and instructional flags.
    """
    # 1. Check for recurring cognitive bottlenecks (threshold >= 2 occurrences)
    top_recurring = None
    max_count = 0
    for mis, cnt in misconception_dict.items():
        if cnt >= 2 and cnt > max_count:
            top_recurring = mis
            max_count = cnt

    if top_recurring:
        # Student is caught in a recurring trap
        return {
            "status": "remediation_needed",
            "recommended_difficulty": "easy",
            "recurring_bottleneck": top_recurring,
            "bottleneck_count": max_count,
            "action": "concept_review",
            "title": "Conceptual Remediation Recommended",
            "message": f"You've encountered {top_recurring.replace('_', ' ').title()} {max_count} times. We recommend reviewing the foundational concept guide before continuing to harder questions.",
            "next_step": "Review the concept summary and attempt 2 foundational practice problems."
        }

    # 2. Ladder adaptation based on mastery score
    if mastery_score >= 80.0:
        recommended_diff = "hard"
        status_msg = "Advanced Mastery Track"
        action = "advance"
        detail = "You have demonstrated strong conceptual understanding. Leveling up to challenge problems!"
    elif mastery_score >= 45.0:
        recommended_diff = "medium"
        status_msg = "Core Practice Track"
        action = "reinforce"
        detail = "Keep building consistency with intermediate application questions."
    else:
        recommended_diff = "easy"
        status_msg = "Foundational Track"
        action = "scaffold"
        detail = "Focusing on core foundational questions to solidify essential principles."

    return {
        "status": status_msg,
        "recommended_difficulty": recommended_diff,
        "recurring_bottleneck": None,
        "bottleneck_count": 0,
        "action": action,
        "title": f"Adaptive Recommendation: {recommended_diff.capitalize()}",
        "message": detail,
        "next_step": f"Continue with {recommended_diff} level questions."
    }
