"""
FlowSync Backend — FastAPI Application Entry Point
===================================================

Production-ready FastAPI server with:
- CORS middleware for frontend connectivity
- YOLO + ML model preloaded at startup (once, not per request)
- Modular route registration
- Structured logging
- Proper exception handling and HTTP status codes

Start with:
    uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
"""

import sys
from pathlib import Path

# Ensure FlowSync/ root is on sys.path so backend.* imports work
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# Keep the backend bootstrap stable for both direct and package-based imports.
__all__ = ["app"]

from backend.config.config import PROJECT_NAME, VERSION, STATUS, OUTPUT_DIR
from backend.routes.traffic import router as traffic_router
from backend.services.ai_service import ai_service
from backend.utils.logger import logger


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------
app = FastAPI(
    title=f"{PROJECT_NAME} API",
    description="AI-powered traffic management backend — vehicle detection, congestion prediction, signal decision engine.",
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# ---------------------------------------------------------------------------
# CORS Middleware — Allow frontend team to connect
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Tighten in production to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Serve annotated output images as static files
# ---------------------------------------------------------------------------
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

# ---------------------------------------------------------------------------
# Register Routers
# ---------------------------------------------------------------------------
app.include_router(traffic_router, tags=["Traffic Analysis"])


# ---------------------------------------------------------------------------
# Startup Event — Preload AI Models
# ---------------------------------------------------------------------------
@app.on_event("startup")
async def startup_event():
    """
    Triggered once when the server starts.
    Preloads YOLOv8 and Random Forest model into memory.
    """
    logger.info(f"Starting {PROJECT_NAME} Backend v{VERSION}...")
    try:
        ai_service.load_models()
        logger.info("All AI models loaded and ready.")
    except Exception as e:
        logger.error(f"CRITICAL: AI model loading failed at startup: {e}")
        # Don't crash — let individual requests handle 503 if model is unavailable


# ---------------------------------------------------------------------------
# Core Routes
# ---------------------------------------------------------------------------
@app.get("/", tags=["System"])
def root():
    """
    Root health check endpoint.
    """
    return {
        "project": PROJECT_NAME,
        "version": VERSION,
        "status": STATUS
    }


@app.get("/health", tags=["System"])
def health_check():
    """
    Lightweight health check endpoint for monitoring and load balancers.
    """
    return {"status": "healthy"}


# ---------------------------------------------------------------------------
# Global Exception Handler
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception at {request.url}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


# ---------------------------------------------------------------------------
# Run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    from backend.config.config import HOST, PORT
    logger.info(f"Launching {PROJECT_NAME} on http://{HOST}:{PORT}")
    uvicorn.run("backend.main:app", host=HOST, port=PORT, reload=True)
