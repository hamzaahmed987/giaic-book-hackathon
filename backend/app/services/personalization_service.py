"""
Content personalization service.
"""
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.content import CachedContent


class PersonalizationService:
    """Service for personalizing book content."""

    def __init__(self):
        # Use OpenRouter or OpenAI based on LLM_PROVIDER setting
        if settings.LLM_PROVIDER == "openrouter" and settings.OPENROUTER_API_KEY:
            self.client = AsyncOpenAI(
                api_key=settings.OPENROUTER_API_KEY,
                base_url=settings.OPENROUTER_BASE_URL,
            )
            self.model = settings.OPENROUTER_MODEL
        else:
            # Fallback to direct OpenAI
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.OPENAI_MODEL

    async def personalize_content(
        self,
        content: str,
        user_profile: Dict[str, Any],
        chapter_id: str,
        db: AsyncSession,
    ) -> str:
        """
        Personalize content based on user profile.

        Args:
            content: Original chapter content
            user_profile: User's profile data
            chapter_id: Chapter identifier
            db: Database session

        Returns:
            Personalized content
        """
        user_id = user_profile.get("user_id")

        # Check cache first
        cached = await self._get_cached(db, user_id, chapter_id, "personalized")
        if cached:
            return cached

        # Generate personalized content
        prompt = self._build_personalization_prompt(content, user_profile)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert educational content adapter.
Your task is to personalize educational content based on the learner's profile.

Rules:
- Keep all code blocks unchanged
- Maintain the original structure (headings, sections)
- Adjust explanations for the learner's level
- Use relevant examples based on their known languages
- Keep the content length similar to the original
"""
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,  # Limited to stay within OpenRouter free tier
        )

        personalized = response.choices[0].message.content

        # Cache the result
        await self._cache_content(
            db,
            user_id,
            chapter_id,
            "personalized",
            personalized
        )

        return personalized

    def _build_personalization_prompt(
        self,
        content: str,
        user_profile: Dict[str, Any],
    ) -> str:
        """Build the personalization prompt."""
        level = user_profile.get("experience_level", "beginner")
        languages = user_profile.get("known_languages", [])
        hardware = user_profile.get("hardware_tier", "medium")
        goals = user_profile.get("goals", [])

        return f"""Personalize the following educational content for a learner with this profile:

- Experience Level: {level}
- Programming Languages Known: {', '.join(languages) if languages else 'None specified'}
- Hardware: {hardware} tier
- Learning Goals: {', '.join(goals) if goals else 'General learning'}

Instructions:
1. For beginners: Add more context, simpler explanations, more analogies
2. For intermediate: Balance theory and practice
3. For advanced: Focus on nuances, edge cases, and advanced patterns

If they know specific languages, use comparisons to those languages where helpful.

Original Content:
{content}

Personalized Content:"""

    async def _get_cached(
        self,
        db: AsyncSession,
        user_id: str,
        chapter_id: str,
        content_type: str,
    ) -> Optional[str]:
        """Get cached content if exists and not expired."""
        result = await db.execute(
            select(CachedContent).where(
                CachedContent.user_id == user_id,
                CachedContent.chapter_id == chapter_id,
                CachedContent.content_type == content_type,
            )
        )
        cached = result.scalar_one_or_none()

        if cached:
            if cached.expires_at and cached.expires_at < datetime.utcnow():
                await db.delete(cached)
                await db.commit()
                return None
            return cached.content

        return None

    async def _cache_content(
        self,
        db: AsyncSession,
        user_id: str,
        chapter_id: str,
        content_type: str,
        content: str,
        ttl_days: int = 7,
    ):
        """Cache content with expiration."""
        cached = CachedContent(
            user_id=user_id,
            chapter_id=chapter_id,
            content_type=content_type,
            content=content,
            expires_at=datetime.utcnow() + timedelta(days=ttl_days),
        )
        db.add(cached)
        await db.commit()


# Global instance
personalization_service = PersonalizationService()
