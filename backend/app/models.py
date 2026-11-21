import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="student", nullable=False) # "student" or "teacher"
    full_name = Column(String(100), nullable=True)
    grade = Column(String(50), default="Grade 8-10", nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    attempts = relationship("AssessmentAttempt", back_populates="user", cascade="all, delete-orphan")
    masteries = relationship("StudentTopicMastery", back_populates="user", cascade="all, delete-orphan")

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(50), default="Calculator", nullable=False)
    difficulty_levels = Column(String(100), default="Easy,Medium,Hard", nullable=False)
    concept_guide = Column(Text, nullable=True) # Markdown guide of the core concepts

    questions = relationship("Question", back_populates="topic", cascade="all, delete-orphan")
    masteries = relationship("StudentTopicMastery", back_populates="topic", cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    correct_answer = Column(String(100), nullable=False)
    step_by_step_solution = Column(Text, nullable=False)
    explanation = Column(Text, nullable=False)
    difficulty = Column(String(20), default="medium", nullable=False) # "easy", "medium", "hard"
    approach_options = Column(Text, default="[]", nullable=False) # JSON array of approach choices
    hint_1 = Column(Text, nullable=True)
    hint_2 = Column(Text, nullable=True)
    common_misconceptions = Column(Text, default="[]", nullable=False) # JSON array

    topic = relationship("Topic", back_populates="questions")
    attempts = relationship("AssessmentAttempt", back_populates="question")

class AssessmentAttempt(Base):
    __tablename__ = "assessment_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    student_answer = Column(String(200), nullable=False)
    intermediate_steps = Column(Text, nullable=True)
    approach_selected = Column(String(100), default="standard", nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    predicted_misconception = Column(String(100), default="none", nullable=False)
    ml_confidence = Column(Float, default=0.0, nullable=False)
    class_probabilities = Column(Text, default="{}", nullable=False) # JSON
    ai_feedback = Column(Text, default="{}", nullable=False) # JSON containing explanation, hint, remedial question
    time_taken_seconds = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="attempts")
    question = relationship("Question", back_populates="attempts")

class StudentTopicMastery(Base):
    __tablename__ = "student_topic_masteries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    mastery_score = Column(Float, default=0.0, nullable=False) # 0 to 100
    attempts_count = Column(Integer, default=0, nullable=False)
    correct_count = Column(Integer, default=0, nullable=False)
    recurring_misconceptions = Column(Text, default="{}", nullable=False) # JSON: {"sign_error": 3, "inverse_op": 1}
    last_practiced = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="masteries")
    topic = relationship("Topic", back_populates="masteries")
