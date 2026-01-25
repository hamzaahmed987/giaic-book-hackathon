"""
AI-Powered Book Platform - FastAPI Backend
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, chat, content
from app.core.config import settings
from app.infrastructure.database import init_db

# Import all models to ensure they are registered with Base
from app.models import User, UserProfile, CachedContent, ChatSession, ChatMessage


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting AI Book Platform API...")
    print("Initializing database tables...")
    await init_db()
    print("Database initialized!")
    yield
    # Shutdown
    print("Shutting down AI Book Platform API...")


app = FastAPI(
    title="AI Book Platform API",
    description="Backend API for AI-Powered Learning Platform",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(content.router, prefix="/api/content", tags=["Content"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "AI Book Platform API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
