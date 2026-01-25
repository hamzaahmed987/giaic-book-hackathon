"""
Dependency injection for FastAPI.
"""
from typing import Optional

from fastapi import Depends, HTTPException, status, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.security import decode_token
from app.infrastructure.database import get_db
from app.models.user import User, UserProfile


async def get_current_user(
    session: AsyncSession = Depends(get_db),
    access_token: Optional[str] = Cookie(default=None)
) -> Optional[User]:
    """Get the current authenticated user from the access token cookie."""
    if not access_token:
        return None

    payload = decode_token(access_token)
    if not payload:
        return None

    user_id = payload.get("sub")
    if not user_id:
        return None

    # Get user from database with profile
    result = await session.execute(
        select(User)
        .options(selectinload(User.profile))
        .where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    return user


async def get_current_user_required(
    user: Optional[User] = Depends(get_current_user)
) -> User:
    """Require an authenticated user."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
