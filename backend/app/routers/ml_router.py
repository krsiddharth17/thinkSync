import os
import json
import sys
from fastapi import APIRouter, HTTPException
from ..schemas import MLPredictRequest, MLPredictResponse

ml_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "ml"))
if ml_dir not in sys.path:
    sys.path.insert(0, ml_dir)

try:
    from backend.ml.predictor import predict_misconception
except (ImportError, ValueError):
    from predictor import predict_misconception

router = APIRouter(prefix="/ml", tags=["Machine Learning Engine"])

METRICS_PATH = os.path.join(ml_dir, "metrics.json")

@router.post("/predict", response_model=MLPredictResponse)
def predict_live(req: MLPredictRequest):
    result = predict_misconception(
        question=req.question,
        correct_answer=req.correct_answer,
        student_answer=req.student_answer,
        steps=req.steps or "",
        approach=req.approach or "standard",
        topic=req.topic or "general"
    )
    return MLPredictResponse(
        predicted_misconception=result["predicted_misconception"],
        confidence=result["confidence"],
        is_uncertain=result.get("is_uncertain", False),
        metadata=result["metadata"],
        class_probabilities=result["class_probabilities"],
        reason=result["reason"]
    )

@router.get("/metrics")
def get_model_metrics():
    if not os.path.exists(METRICS_PATH):
        raise HTTPException(status_code=404, detail="Model metrics file not found. Please train model first.")
    with open(METRICS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
