import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Topic, Question, StudentTopicMastery, User
from ..schemas import TopicSummary, TopicDetail, QuestionResponse
from ..auth import get_current_user

router = APIRouter(prefix="/topics", tags=["Topics"])

@router.get("", response_model=List[TopicSummary])
def list_topics(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    topics = db.query(Topic).all()
    results = []

    for topic in topics:
        total_q = db.query(Question).filter(Question.topic_id == topic.id).count()
        
        mastery_score = 0.0
        attempts_cnt = 0
        recurring_mis = {}

        if current_user:
            m = db.query(StudentTopicMastery).filter(
                StudentTopicMastery.user_id == current_user.id,
                StudentTopicMastery.topic_id == topic.id
            ).first()
            if m:
                mastery_score = m.mastery_score
                attempts_cnt = m.attempts_count
                try:
                    recurring_mis = json.loads(m.recurring_misconceptions or "{}")
                except Exception:
                    recurring_mis = {}

        results.append(TopicSummary(
            id=topic.id,
            name=topic.name,
            slug=topic.slug,
            description=topic.description,
            icon=topic.icon,
            difficulty_levels=topic.difficulty_levels,
            total_questions=total_q,
            mastery_score=mastery_score,
            attempts_count=attempts_cnt,
            recurring_misconceptions=recurring_mis
        ))

    return results

@router.get("/{slug}", response_model=TopicDetail)
def get_topic_detail(
    slug: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    topic = db.query(Topic).filter(Topic.slug == slug).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    total_q = db.query(Question).filter(Question.topic_id == topic.id).count()
    mastery_score = 0.0
    attempts_cnt = 0
    recurring_mis = {}

    if current_user:
        m = db.query(StudentTopicMastery).filter(
            StudentTopicMastery.user_id == current_user.id,
            StudentTopicMastery.topic_id == topic.id
        ).first()
        if m:
            mastery_score = m.mastery_score
            attempts_cnt = m.attempts_count
            try:
                recurring_mis = json.loads(m.recurring_misconceptions or "{}")
            except Exception:
                recurring_mis = {}

    return TopicDetail(
        id=topic.id,
        name=topic.name,
        slug=topic.slug,
        description=topic.description,
        icon=topic.icon,
        difficulty_levels=topic.difficulty_levels,
        total_questions=total_q,
        mastery_score=mastery_score,
        attempts_count=attempts_cnt,
        recurring_misconceptions=recurring_mis,
        concept_guide=topic.concept_guide
    )

@router.get("/{slug}/questions", response_model=List[QuestionResponse])
def get_topic_questions(
    slug: str,
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    topic = db.query(Topic).filter(Topic.slug == slug).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    query = db.query(Question).filter(Question.topic_id == topic.id)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty.lower())

    questions = query.all()
    results = []

    for q in questions:
        try:
            approach_opts = json.loads(q.approach_options or "[]")
        except Exception:
            approach_opts = []

        results.append(QuestionResponse(
            id=q.id,
            topic_id=q.topic_id,
            question_text=q.question_text,
            difficulty=q.difficulty,
            approach_options=approach_opts,
            hint_1=q.hint_1,
            hint_2=q.hint_2
        ))

    return results
