"""
Chat schemas.
"""
from typing import Optional, List
from datetime import datetime

from pydantic import BaseModel


class Citation(BaseModel):
    """Citation reference."""
    id: int
    source: str
    chapter: str
    score: float


class ChatMessage(BaseModel):
    """A single chat message."""
    role: str  # 'user' or 'assistant'
    content: str


class ChatRequest(BaseModel):
    """Chat request schema."""
    query: str
    selected_text: Optional[str] = None
    chapter_id: Optional[str] = None
    session_id: Optional[str] = None  # For persistent chat
    conversation_history: Optional[List[ChatMessage]] = None  # Previous messages for memory


class ChatResponse(BaseModel):
    """Chat response schema."""
    answer: str
    citations: List[Citation] = []


# Session-related schemas
class ChatSessionCreate(BaseModel):
    """Create a new chat session."""
    title: Optional[str] = "New Chat"


class ChatMessageResponse(BaseModel):
    """Response for a single message."""
    id: str
    role: str
    content: str
    model: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    """Response for a chat session."""
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

    class Config:
        from_attributes = True


class ChatSessionDetail(BaseModel):
    """Detailed chat session with messages."""
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True
