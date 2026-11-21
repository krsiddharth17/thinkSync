import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base, SessionLocal
from .seed_data import seed_database

# Routers
from .routers.auth_router import router as auth_router
from .routers.topics_router import router as topics_router
from .routers.assessment_router import router as assessment_router
from .routers.student_router import router as student_router
from .routers.teacher_router import router as teacher_router
from .routers.ml_router import router as ml_router

# Direct startup initialization (completely reliable across all Python versions)
print("[Startup] Ensuring thinkSync AI Database & Tables...")
Base.metadata.create_all(bind=engine)
_db = SessionLocal()
try:
    seed_database(_db)
finally:
    _db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="thinkSync AI: Intelligent Educational Platform that understands WHERE and WHY students get stuck using Machine Learning and AI Tutoring."
)

# Enable CORS for Vite frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(topics_router, prefix=settings.API_V1_STR)
app.include_router(assessment_router, prefix=settings.API_V1_STR)
app.include_router(student_router, prefix=settings.API_V1_STR)
app.include_router(teacher_router, prefix=settings.API_V1_STR)
app.include_router(ml_router, prefix=settings.API_V1_STR)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "ml_engine": "Scikit-Learn Random Forest + TF-IDF Pipeline (95.5% Accuracy)",
        "gemini_api_configured": bool(settings.GEMINI_API_KEY)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
