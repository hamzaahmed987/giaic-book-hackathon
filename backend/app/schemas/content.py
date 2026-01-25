"""
Content schemas.
"""
from pydantic import BaseModel


class PersonalizeRequest(BaseModel):
    """Request to personalize content."""
    chapter_id: str


class TranslateRequest(BaseModel):
    """Request to translate content."""
    chapter_id: str
    target_language: str = "ur"  # Default to Urdu


class ContentResponse(BaseModel):
    """Response with content."""
    content: str
    cached: bool = False
