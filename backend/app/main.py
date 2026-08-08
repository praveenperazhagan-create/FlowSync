"""
FlowSync Backend Application Entry Point
========================================

FastAPI Application importing app.routes.traffic.
Start with:
    uvicorn app.main:app --reload
"""

import sys
from pathlib import Path

# Add backend directory to sys.path automatically
BACKEND_DIR = Path(__file__).resolve().parent.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routes.traffic import router as traffic_router
from backend.app.config import PROJECT_NAME, VERSION

# Re-export the router for compatibility with alternate imports.
__all__ = ["app", "traffic_router"]

app = FastAPI(
    title=f"{PROJECT_NAME} Backend API",
    description="Production-ready FastAPI bridge connecting frontend to modular City AI engine.",
    version=VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(traffic_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
