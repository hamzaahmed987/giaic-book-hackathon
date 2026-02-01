"""
Database configuration and session management.
Optimized for serverless/Vercel deployment.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Global engine and session maker for reuse across requests
_engine = None
_async_session_maker = None


def get_engine():
    global _engine
    if _engine is None:
        # For serverless environments, use NullPool to avoid connection issues
        _engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DEBUG,
            poolclass=NullPool,  # Use NullPool for serverless environments
            connect_args={
                "server_settings": {
                    "application_name": "ai-book-platform-vercel",
                },
            },
        )
    return _engine


def get_async_session_maker():
    global _async_session_maker
    if _async_session_maker is None:
        _async_session_maker = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _async_session_maker


# Base class for models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get database session."""
    async with get_async_session_maker()() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    # In serverless environments, avoid running DDL operations in request handlers
    # This should be handled separately during deployment
    pass