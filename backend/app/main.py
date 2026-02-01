"""
AI-Powered Book Platform - FastAPI Backend
Optimized for Vercel serverless deployment
"""
from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, chat, content
from app.core.config import settings


# Initialize database connection globally to reuse between requests
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Starting AI Book Platform API on Vercel...")
    
    # Initialize any required resources here
    # Note: In serverless environment, we minimize startup operations
    
    yield
    
    # Shutdown
    print("Shutting down AI Book Platform API...")


app = FastAPI(
    title="AI Book Platform API",
    description="Backend API for AI-Powered Learning Platform (Vercel Optimized)",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - configured for Vercel deployment
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
        "status": "running",
        "deployment": "vercel"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "deployment": "vercel"}


# Add exception handlers for better serverless error reporting
@app.exception_handler(500)
async def internal_exception_handler(request, exc):
    logging.error(f"Internal server error: {exc}")
    return {"error": "Internal server error"}