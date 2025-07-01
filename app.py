#!/usr/bin/env python3
"""
Production deployment entry point
Serves both backend API and frontend static files
"""

import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Import backend modules
from routes.resume_routes import router as resume_router
from models import create_tables

app = FastAPI(title="Resume Intelligence API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(resume_router, prefix="/api", tags=["resumes"])

# Serve static frontend files
frontend_path = Path(__file__).parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_path)), name="static")

@app.get("/")
def serve_frontend():
    """Serve the main frontend HTML file"""
    return FileResponse(str(frontend_path / "index.html"))

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Resume Intelligence API is running"}

@app.on_event("startup")
def startup_event():
    create_tables()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
