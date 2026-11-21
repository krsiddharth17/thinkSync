import json
import sys
import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Question, AssessmentAttempt, User, Topic
from ..schemas import AssessmentSubmission, AssessmentResult, AIFeedback, HintRequest
from ..auth import get_current_user
from ..services.tutor_service import generate_ai_tutor_feedback, generate_step_hint
from ..services.adaptive_engine import update_student_mastery_profile

# Add ml folder to sys.path
ml_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ml"))
if ml_dir not in sys.path:
    sys.path.insert(0, ml_dir)

from predictor import predict_misconception, is_exact_match, MISCONCEPTION_METADATA

router = APIRouter(prefix="/assessment", tags=["Assessment & Diagnosis"])

@router.post("/evaluate", response_model=AssessmentResult)
def evaluate_submission(
    submission: AssessmentSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = db.query(Question).filter(Question.id == submission.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    topic = db.query(Topic).filter(Topic.id == question.topic_id).first()
    topic_slug = topic.slug if topic else "general"

    # 1. Exact Answer Correctness Check
    is_correct = is_exact_match(submission.student_answer, question.correct_answer)

    # 2. ML Misconception Detection Engine (Real Scikit-learn Classifier)
    ml_result = predict_misconception(
        question=question.question_text,
        correct_answer=question.correct_answer,
        student_answer=submission.student_answer,
        steps=submission.intermediate_steps or "",
        approach=submission.approach_selected or "standard",
        topic=topic_slug
    )

    predicted_label = ml_result["predicted_misconception"]
    confidence = ml_result["confidence"]
    is_uncertain = ml_result.get("is_uncertain", False)
    class_probs = ml_result["class_probabilities"]
    meta = ml_result["metadata"]

    # If exact answer is correct, force correct label
    if is_correct:
        predicted_label = "correct"
        confidence = max(confidence, 0.95)
        meta = MISCONCEPTION_METADATA["correct"]

    # 3. AI Tutor Feedback (Gemini or Fallback Pedagogy)
    tutor_feedback = generate_ai_tutor_feedback(
        question_text=question.question_text,
        student_answer=submission.student_answer,
        intermediate_steps=submission.intermediate_steps or "",
        predicted_misconception=predicted_label,
        ml_confidence=confidence,
        topic=topic.name if topic else "Mathematics",
        is_correct=is_correct
    )

    # 4. Adaptive Learning Engine Update
    adaptive_profile = update_student_mastery_profile(
        db=db,
        user_id=current_user.id,
        topic_id=question.topic_id,
        is_correct=is_correct,
        predicted_misconception=predicted_label,
        difficulty=question.difficulty
    )

    # 5. Persist Attempt Record in Database
    attempt = AssessmentAttempt(
        user_id=current_user.id,
        question_id=question.id,
        student_answer=submission.student_answer,
        intermediate_steps=submission.intermediate_steps,
        approach_selected=submission.approach_selected,
        is_correct=is_correct,
        predicted_misconception=predicted_label,
        ml_confidence=confidence,
        class_probabilities=json.dumps(class_probs),
        ai_feedback=json.dumps(tutor_feedback),
        time_taken_seconds=submission.time_taken_seconds or 30
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return AssessmentResult(
        attempt_id=attempt.id,
        is_correct=is_correct,
        correct_answer=question.correct_answer,
        student_answer=submission.student_answer,
        predicted_misconception=predicted_label,
        misconception_title=meta["title"],
        misconception_description=meta["description"],
        ml_confidence=confidence,
        is_uncertain=is_uncertain,
        class_probabilities=class_probs,
        ai_feedback=AIFeedback(
            mistake_analysis=tutor_feedback.get("mistake_analysis", ""),
            conceptual_explanation=tutor_feedback.get("conceptual_explanation", ""),
            socratic_hint=tutor_feedback.get("socratic_hint", ""),
            remedial_question=tutor_feedback.get("remedial_question"),
            encouragement=tutor_feedback.get("encouragement", "")
        ),
        updated_topic_mastery=adaptive_profile["updated_mastery_score"],
        adaptive_recommendation=adaptive_profile["recommendation"]
    )

@router.post("/hint")
def request_hint(
    hint_req: HintRequest,
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == hint_req.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    hint_response = generate_step_hint(
        question_text=question.question_text,
        current_steps=hint_req.student_current_steps or "",
        hint_level=hint_req.hint_level
    )

    # Also augment with question-specific hints if available
    if hint_req.hint_level == 1 and question.hint_1:
        hint_response["question_hint"] = question.hint_1
    elif hint_req.hint_level == 2 and question.hint_2:
        hint_response["question_hint"] = question.hint_2

    return hint_response
