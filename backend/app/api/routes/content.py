"""
Content API routes for personalization and translation.
"""
from typing import Optional
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.infrastructure.database import get_db
from app.models.user import User
from app.schemas.content import PersonalizeRequest, TranslateRequest, ContentResponse
from app.services.personalization_service import personalization_service
from app.services.translation_service import translation_service

router = APIRouter()

# Map chapter IDs to content (in production, this would come from a CMS or files)
CHAPTER_CONTENT = {
    "chapter-1": "Chapter 1 content about AI Foundations...",
    "chapter-2": "Chapter 2 content about LLM Fundamentals...",
    "chapter-3": "Chapter 3 content about Prompt Engineering...",
    "chapter-4": "Chapter 4 content about RAG Systems...",
    "chapter-5": "Chapter 5 content about AI Agents...",
    "chapter-6": "Chapter 6 content about Building AI Applications...",
}


async def get_chapter_content(chapter_id: str) -> str:
    """Get chapter content from file or cache."""
    # In production, read from docs directory or CMS
    # For now, return placeholder
    return CHAPTER_CONTENT.get(
        chapter_id,
        f"Content for {chapter_id} not found."
    )


@router.post("/personalize", response_model=ContentResponse)
async def personalize_content(
    request: PersonalizeRequest,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    Get personalized version of chapter content.

    Adapts content based on:
    - User's experience level
    - Known programming languages
    - Hardware tier
    - Learning goals
    """
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Authentication required for personalization",
        )

    if not user.profile:
        raise HTTPException(
            status_code=400,
            detail="Please complete your profile first",
        )

    try:
        # Get original content
        original_content = await get_chapter_content(request.chapter_id)

        # Build user profile dict
        user_profile = {
            "user_id": user.id,
            "experience_level": user.profile.experience_level.value if user.profile.experience_level else "beginner",
            "known_languages": user.profile.known_languages or [],
            "hardware_tier": user.profile.hardware_tier.value if user.profile.hardware_tier else "medium",
            "goals": user.profile.goals or [],
        }

        # Personalize
        personalized = await personalization_service.personalize_content(
            content=original_content,
            user_profile=user_profile,
            chapter_id=request.chapter_id,
            db=db,
        )

        return ContentResponse(content=personalized, cached=False)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error personalizing content: {str(e)}",
        )


@router.post("/translate", response_model=ContentResponse)
async def translate_content(
    request: TranslateRequest,
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    """
    Translate chapter content to Urdu.

    Features:
    - Preserves code blocks
    - Maintains structure
    - Caches for performance
    """
    if request.target_language != "ur":
        raise HTTPException(
            status_code=400,
            detail="Only Urdu (ur) translation is currently supported",
        )

    try:
        # Get original content
        original_content = await get_chapter_content(request.chapter_id)

        # Translate
        translated = await translation_service.translate_to_urdu(
            content=original_content,
            chapter_id=request.chapter_id,
            user_id=user.id if user else None,
            db=db,
        )

        return ContentResponse(content=translated, cached=False)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error translating content: {str(e)}",
        )


@router.get("/chapter/{chapter_id}")
async def get_chapter(chapter_id: str):
    """Get original chapter content."""
    content = await get_chapter_content(chapter_id)
    return {"chapter_id": chapter_id, "content": content}
