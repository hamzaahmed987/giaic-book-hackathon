"""
Content models for caching personalized and translated content.
"""
import uuid
from datetime import datetime

from sqlalchemy import Column, String, Text, DateTime, Index

from app.infrastructure.database import Base


class CachedContent(Base):
    """Cached personalized or translated content."""

    __tablename__ = "cached_content"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True, index=True)
    chapter_id = Column(String, nullable=False, index=True)
    content_type = Column(String, nullable=False)  # "personalized" or "translated_ur"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index('idx_cached_content_lookup', 'user_id', 'chapter_id', 'content_type'),
    )
