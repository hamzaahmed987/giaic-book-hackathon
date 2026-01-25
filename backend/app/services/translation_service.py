"""
Translation service for Urdu support.
"""
import re
from typing import Optional
from datetime import datetime, timedelta

from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models.content import CachedContent


class TranslationService:
    """Service for translating book content to Urdu."""

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

    async def translate_to_urdu(
        self,
        content: str,
        chapter_id: str,
        user_id: Optional[str],
        db: AsyncSession,
    ) -> str:
        """
        Translate content to Urdu while preserving code blocks.

        Args:
            content: Original content
            chapter_id: Chapter identifier
            user_id: Optional user ID for caching
            db: Database session

        Returns:
            Translated content
        """
        # Check cache first
        if user_id:
            cached = await self._get_cached(db, user_id, chapter_id, "translated_ur")
            if cached:
                return cached

        # Extract and protect code blocks
        code_blocks = re.findall(r'```[\s\S]*?```', content)
        placeholders = [f"__CODE_BLOCK_{i}__" for i in range(len(code_blocks))]

        protected_content = content
        for block, placeholder in zip(code_blocks, placeholders):
            protected_content = protected_content.replace(block, placeholder)

        # Translate
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert translator specializing in technical content translation to Urdu.

Rules:
1. Translate all text content to Urdu
2. Keep technical terms in English with Urdu explanation if needed
3. Preserve all placeholders like __CODE_BLOCK_0__
4. Maintain markdown formatting (headings, lists, bold, etc.)
5. Keep the document structure intact
6. Translate naturally, not word-by-word
"""
                },
                {
                    "role": "user",
                    "content": f"Translate this content to Urdu:\n\n{protected_content}"
                }
            ],
            temperature=0.3,  # Lower temperature for more consistent translation
            max_tokens=1000,  # Limited to stay within OpenRouter free tier
        )

        translated = response.choices[0].message.content

        # Restore code blocks
        for placeholder, block in zip(placeholders, code_blocks):
            translated = translated.replace(placeholder, block)

        # Cache the result
        if user_id:
            await self._cache_content(
                db,
                user_id,
                chapter_id,
                "translated_ur",
                translated
            )

        return translated

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
        ttl_days: int = 30,  # Longer cache for translations
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
translation_service = TranslationService()
