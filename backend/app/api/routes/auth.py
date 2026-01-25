"""
Authentication API routes.
"""
from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.deps import get_current_user
from app.infrastructure.database import get_db
from app.models.user import User, UserProfile
from app.schemas.auth import UserCreate, UserLogin, UserResponse, ProfileUpdate, ProfileResponse

router = APIRouter()


def user_to_response(user: User) -> dict:
    """Convert User ORM object to response dict (avoids async serialization issues)."""
    profile_data = None
    if user.profile:
        profile_data = {
            "experience_level": user.profile.experience_level.value if user.profile.experience_level else "beginner",
            "known_languages": user.profile.known_languages or [],
            "hardware_tier": user.profile.hardware_tier.value if user.profile.hardware_tier else "medium",
            "goals": user.profile.goals or [],
        }

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "profile": profile_data,
    }


@router.post("/signup", response_model=UserResponse)
async def signup(
    user_data: UserCreate,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user."""
    # Check if user exists
    result = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Create user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        name=user_data.name,
    )
    db.add(user)
    await db.flush()

    # Create default profile
    profile = UserProfile(user_id=user.id)
    db.add(profile)
    await db.commit()

    # Reload user with profile
    result = await db.execute(
        select(User)
        .options(selectinload(User.profile))
        .where(User.id == user.id)
    )
    user = result.scalar_one()

    # Set access token cookie
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    # Return dict, not ORM object
    return user_to_response(user)


@router.post("/signin", response_model=UserResponse)
async def signin(
    user_data: UserLogin,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    """Sign in a user."""
    # Find user with profile
    result = await db.execute(
        select(User)
        .options(selectinload(User.profile))
        .where(User.email == user_data.email)
    )
    user = result.scalar_one_or_none()

    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Set access token cookie
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=not settings.DEBUG,
        samesite="lax",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

    # Return dict, not ORM object
    return user_to_response(user)


@router.post("/signout")
async def signout(response: Response):
    """Sign out a user."""
    response.delete_cookie(key="access_token")
    return {"message": "Signed out successfully"}


@router.get("/me")
async def get_me(
    user: Optional[User] = Depends(get_current_user),
):
    """Get current user."""
    if not user:
        return None
    # Return dict, not ORM object
    return user_to_response(user)


@router.patch("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: ProfileUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Update user profile."""
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )

    # Get or create profile
    result = await db.execute(
        select(UserProfile).where(UserProfile.user_id == user.id)
    )
    profile = result.scalar_one_or_none()

    if not profile:
        profile = UserProfile(user_id=user.id)
        db.add(profile)

    # Update fields
    if profile_data.experience_level:
        profile.experience_level = profile_data.experience_level
    if profile_data.known_languages is not None:
        profile.known_languages = profile_data.known_languages
    if profile_data.hardware_tier:
        profile.hardware_tier = profile_data.hardware_tier
    if profile_data.goals is not None:
        profile.goals = profile_data.goals

    await db.commit()

    # Reload user with updated profile
    result = await db.execute(
        select(User)
        .options(selectinload(User.profile))
        .where(User.id == user.id)
    )
    user = result.scalar_one()

    # Return dict, not ORM object
    return user_to_response(user)
