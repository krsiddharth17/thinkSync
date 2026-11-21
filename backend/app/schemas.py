from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr

# Auth Schemas
class UserRegister(BaseModel):
    username: str
    email: str
    password: str
    full_name: Optional[str] = None
    role: str = "student" # "student" or "teacher"
    grade: Optional[str] = "Grade 9"

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    full_name: Optional[str]
    grade: Optional[str]

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Topic Schemas
class TopicSummary(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    icon: str
    difficulty_levels: str
    total_questions: int = 0
    mastery_score: float = 0.0
    attempts_count: int = 0
    recurring_misconceptions: Dict[str, int] = {}

class TopicDetail(TopicSummary):
    concept_guide: Optional[str] = None

# Question Schemas
class QuestionResponse(BaseModel):
    id: int
    topic_id: int
    question_text: str
    difficulty: str
    approach_options: List[str] = []
    hint_1: Optional[str] = None
    hint_2: Optional[str] = None

class QuestionDetailResponse(QuestionResponse):
    correct_answer: str
    step_by_step_solution: str
    explanation: str

# Assessment Submission Schema
class AssessmentSubmission(BaseModel):
    question_id: int
    student_answer: str
    intermediate_steps: Optional[str] = ""
    approach_selected: Optional[str] = "standard"
    time_taken_seconds: Optional[int] = 30

class AIFeedback(BaseModel):
    mistake_analysis: str
    conceptual_explanation: str
    socratic_hint: str
    remedial_question: Optional[str] = None
    encouragement: str

class AssessmentResult(BaseModel):
    attempt_id: int
    is_correct: bool
    correct_answer: str
    student_answer: str
    predicted_misconception: str
    misconception_title: str
    misconception_description: str
    ml_confidence: float
    is_uncertain: bool
    class_probabilities: Dict[str, float]
    ai_feedback: AIFeedback
    updated_topic_mastery: float
    adaptive_recommendation: Dict[str, Any]

# ML Prediction Schemas
class MLPredictRequest(BaseModel):
    question: str
    correct_answer: str
    student_answer: str
    steps: Optional[str] = ""
    approach: Optional[str] = "standard"
    topic: Optional[str] = "general"

class MLPredictResponse(BaseModel):
    predicted_misconception: str
    confidence: float
    is_uncertain: bool
    metadata: Dict[str, Any]
    class_probabilities: Dict[str, float]
    reason: str

# Hint Request
class HintRequest(BaseModel):
    question_id: int
    student_current_steps: Optional[str] = ""
    hint_level: int = 1 # 1 or 2
