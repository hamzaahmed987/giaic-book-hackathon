"""
Chat API routes for RAG-powered Q&A using OpenAI Agents SDK.
Includes persistent chat history support.
"""
from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.deps import get_current_user, get_current_user_required
from app.infrastructure.database import get_db
from app.models.user import User
from app.models.chat import ChatSession, ChatMessage as ChatMessageModel, MessageRole
from app.schemas.chat import (
    ChatRequest, ChatResponse, Citation,
    ChatSessionCreate, ChatSessionResponse, ChatSessionDetail, ChatMessageResponse
)

router = APIRouter()


# New schema for agent response
class AgentChatResponse(BaseModel):
    """Response from the agent-based chat."""
    answer: str
    tool_calls: List[dict] = []
    model: str
    agent: str
    session_id: Optional[str] = None  # Return session ID for persistence


# ==================== SESSION MANAGEMENT ====================

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_session(
    session_data: ChatSessionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_required),
):
    """Create a new chat session."""
    session = ChatSession(
        user_id=user.id,
        title=session_data.title or "New Chat"
    )
    db.add(session)
    await db.commit()
    await db.refresh(session)

    return ChatSessionResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        message_count=0
    )


@router.get("/sessions", response_model=List[ChatSessionResponse])
async def list_sessions(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_required),
    limit: int = 20,
    offset: int = 0,
):
    """List all chat sessions for the current user."""
    # Get sessions with message count
    result = await db.execute(
        select(
            ChatSession,
            func.count(ChatMessageModel.id).label("message_count")
        )
        .outerjoin(ChatMessageModel)
        .where(ChatSession.user_id == user.id)
        .group_by(ChatSession.id)
        .order_by(ChatSession.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )

    sessions = []
    for row in result.all():
        session = row[0]
        count = row[1]
        sessions.append(ChatSessionResponse(
            id=session.id,
            title=session.title,
            created_at=session.created_at,
            updated_at=session.updated_at,
            message_count=count
        ))

    return sessions


@router.get("/sessions/{session_id}", response_model=ChatSessionDetail)
async def get_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_required),
):
    """Get a chat session with all messages."""
    result = await db.execute(
        select(ChatSession)
        .options(selectinload(ChatSession.messages))
        .where(ChatSession.id == session_id, ChatSession.user_id == user.id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return ChatSessionDetail(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        messages=[
            ChatMessageResponse(
                id=msg.id,
                role=msg.role.value,
                content=msg.content,
                model=msg.model,
                created_at=msg.created_at
            )
            for msg in session.messages
        ]
    )


@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user_required),
):
    """Delete a chat session."""
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.id == session_id, ChatSession.user_id == user.id)
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    await db.delete(session)
    await db.commit()

    return {"message": "Session deleted"}


# ==================== CHAT QUERY ====================

@router.post("/query", response_model=AgentChatResponse)
async def chat_query(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    """
    Process a chat query using OpenAI Agents SDK.
    Saves messages to session if user is authenticated.

    Features:
    - Multi-step reasoning with tool calling
    - Book search using semantic search
    - Chapter content retrieval
    - Concept explanations adapted to user level
    - Persistent chat history (for authenticated users)
    """
    try:
        from app.agents.book_agent import run_book_agent

        session_id = request.session_id
        conversation_history = []

        # If authenticated, handle session and get history
        if user:
            is_new_session = False

            # Get or create session
            if session_id:
                result = await db.execute(
                    select(ChatSession)
                    .options(selectinload(ChatSession.messages))
                    .where(ChatSession.id == session_id, ChatSession.user_id == user.id)
                )
                session = result.scalar_one_or_none()
                if not session:
                    raise HTTPException(status_code=404, detail="Session not found")

                # Get conversation history from loaded messages
                if session.messages:
                    conversation_history = [
                        {"role": msg.role.value, "content": msg.content}
                        for msg in session.messages[-10:]  # Last 10 messages
                    ]
            else:
                # Create new session with title from first message
                is_new_session = True
                title = request.query[:50] + "..." if len(request.query) > 50 else request.query
                session = ChatSession(user_id=user.id, title=title)
                db.add(session)
                await db.flush()
                session_id = session.id
                # New session has no history

            # Save user message
            user_message = ChatMessageModel(
                session_id=session.id,
                role=MessageRole.USER,
                content=request.query
            )
            db.add(user_message)
        else:
            # For unauthenticated users, use provided history
            if request.conversation_history:
                conversation_history = [msg.model_dump() for msg in request.conversation_history]

        # Get user profile for personalization
        user_profile = None
        if user and hasattr(user, 'profile') and user.profile:
            user_profile = {
                "user_id": str(user.id),
                "experience_level": user.profile.experience_level.value if user.profile.experience_level else "beginner",
                "known_languages": user.profile.known_languages or [],
                "hardware_tier": user.profile.hardware_tier.value if user.profile.hardware_tier else "medium",
                "goals": user.profile.goals or [],
            }

        # Run the agent
        result = await run_book_agent(
            query=request.query,
            selected_text=request.selected_text,
            chapter_filter=request.chapter_id,
            user_profile=user_profile,
            conversation_history=conversation_history,
        )

        # Save assistant response if authenticated
        if user and session_id:
            assistant_message = ChatMessageModel(
                session_id=session_id,
                role=MessageRole.ASSISTANT,
                content=result["answer"],
                model=result.get("model")
            )
            db.add(assistant_message)
            await db.commit()

        return AgentChatResponse(
            answer=result["answer"],
            tool_calls=result.get("tool_calls", []),
            model=result.get("model", "unknown"),
            agent=result.get("agent", "BookAssistant"),
            session_id=session_id
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}",
        )


@router.post("/query/legacy", response_model=ChatResponse)
async def chat_query_legacy(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_current_user),
):
    """
    Legacy RAG query endpoint (without agent framework).
    Kept for backwards compatibility.
    """
    try:
        from app.services.rag_service import rag_service

        # Get user profile for personalization
        user_profile = None
        if user and hasattr(user, 'profile') and user.profile:
            user_profile = {
                "user_id": str(user.id),
                "experience_level": user.profile.experience_level.value if user.profile.experience_level else "beginner",
                "known_languages": user.profile.known_languages or [],
                "hardware_tier": user.profile.hardware_tier.value if user.profile.hardware_tier else "medium",
                "goals": user.profile.goals or [],
            }

        # Query RAG service
        result = await rag_service.query(
            query=request.query,
            selected_text=request.selected_text,
            chapter_filter=request.chapter_id,
            user_profile=user_profile,
        )

        # Format citations
        citations = [
            Citation(
                id=c["id"],
                source=c["source"],
                chapter=c["chapter"],
                score=c["score"],
            )
            for c in result.get("citations", [])
        ]

        return ChatResponse(
            answer=result["answer"],
            citations=citations,
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}",
        )


@router.get("/health")
async def chat_health():
    """Health check for chat service."""
    return {
        "status": "healthy",
        "service": "chat",
        "agent": "BookAssistant",
        "framework": "OpenAI Agents SDK",
        "features": ["persistent_chat", "rag", "personalization"]
    }
