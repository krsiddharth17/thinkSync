import os
import sys

# Ensure sys.path contains root, backend, and backend/app
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CURRENT_DIR)
ROOT_DIR = os.path.dirname(BACKEND_DIR)

for p in [CURRENT_DIR, BACKEND_DIR, ROOT_DIR]:
    if p not in sys.path:
        sys.path.insert(0, p)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from .config import settings
    from .database import engine, Base, SessionLocal
    from .seed_data import seed_database
    from .routers.auth_router import router as auth_router
    from .routers.topics_router import router as topics_router
    from .routers.assessment_router import router as assessment_router
    from .routers.student_router import router as student_router
    from .routers.teacher_router import router as teacher_router
    from .routers.ml_router import router as ml_router
except ImportError:
    try:
        from app.config import settings
        from app.database import engine, Base, SessionLocal
        from app.seed_data import seed_database
        from app.routers.auth_router import router as auth_router
        from app.routers.topics_router import router as topics_router
        from app.routers.assessment_router import router as assessment_router
        from app.routers.student_router import router as student_router
        from app.routers.teacher_router import router as teacher_router
        from app.routers.ml_router import router as ml_router
    except ImportError:
        from backend.app.config import settings
        from backend.app.database import engine, Base, SessionLocal
        from backend.app.seed_data import seed_database
        from backend.app.routers.auth_router import router as auth_router
        from backend.app.routers.topics_router import router as topics_router
        from backend.app.routers.assessment_router import router as assessment_router
        from backend.app.routers.student_router import router as student_router
        from backend.app.routers.teacher_router import router as teacher_router
        from backend.app.routers.ml_router import router as ml_router

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

# Enable CORS for Vite frontend and deployed frontend domains
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*",
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

# Mount Frontend Static Assets & SPA Fallback
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))

@app.get("/", include_in_schema=False)
def root():
    index_html = os.path.join(frontend_dist, "index.html")
    if os.path.exists(index_html):
        return FileResponse(index_html)
    return {
        "app": settings.PROJECT_NAME,
        "status": "online",
        "docs": "/docs",
        "health": "/api/health",
        "version": settings.VERSION
    }

if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    def serve_frontend_spa(full_path: str):
        file_path = os.path.join(frontend_dist, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        index_html = os.path.join(frontend_dist, "index.html")
        if os.path.exists(index_html):
            return FileResponse(index_html)
        return {"error": "Not found", "path": full_path}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
