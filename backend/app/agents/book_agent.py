"""
Book Assistant Agent using OpenAI Agents SDK with OpenRouter.
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, set_tracing_disabled, ModelSettings
from agents.run import RunConfig
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

# Load environment variables
BACKEND_DIR = Path(__file__).parent.parent.parent
load_dotenv(BACKEND_DIR / ".env")

# Import core components
from app.core.config import settings
from app.agents.tools import search_book, get_chapter_content, list_chapters, explain_concept


# ==================== CONFIGURATION ====================

# OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", settings.OPENROUTER_API_KEY)

# Model to use - OpenRouter supports many models
# Examples: openai/gpt-4o, anthropic/claude-3.5-sonnet, google/gemini-2.0-flash-exp, meta-llama/llama-3.1-70b-instruct
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", settings.OPENROUTER_MODEL)

# Create AsyncOpenAI client pointing to OpenRouter's API
# Reference: https://openrouter.ai/docs
external_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
    default_headers={
        "HTTP-Referer": os.getenv("OPENROUTER_REFERER", "http://localhost:3000"),
        "X-Title": os.getenv("OPENROUTER_APP_TITLE", "AI Book Assistant"),
    }
)

# Create the model using OpenAIChatCompletionsModel for compatibility
# Set max_tokens low to stay within OpenRouter free tier limits
model = OpenAIChatCompletionsModel(
    model=OPENROUTER_MODEL,
    openai_client=external_client,
)

# Disable tracing (we don't need OpenAI's tracing)
set_tracing_disabled(True)

# Run configuration
run_config = RunConfig(
    model=model,
    tracing_disabled=True
)


# System instructions for the Book Assistant
BOOK_ASSISTANT_INSTRUCTIONS = """You are an AI-powered learning assistant for an educational book about AI development.

## Your Capabilities:
1. **Search the book** - Use the search_book tool to find relevant content
2. **Get chapter content** - Use get_chapter_content to retrieve specific chapters
3. **List chapters** - Use list_chapters to show available content
4. **Explain concepts** - Use explain_concept for tailored explanations

## Guidelines:
- Always search the book first before answering questions about AI topics
- Cite your sources using [1], [2], etc. format
- If information isn't in the book, say so and provide general knowledge with a disclaimer
- Adapt your explanations based on the user's experience level if known
- Be encouraging and supportive - learning AI can be challenging!

## Topics Covered in the Book:
- Chapter 1: AI Foundations (history, types of AI, ML basics)
- Chapter 2: LLM Fundamentals (transformers, tokenization, APIs)
- Chapter 3: Prompt Engineering (CRAFT framework, few-shot, chain-of-thought)
- Chapter 4: RAG Systems (embeddings, vector databases, retrieval)
- Chapter 5: AI Agents (function calling, agent loops, orchestration)
- Chapter 6: Building AI Apps (full-stack development, deployment)

## Response Format:
- Keep responses concise but informative
- Use markdown formatting for readability
- Include code examples when relevant
- Always cite which chapter the information comes from
"""


def get_book_assistant():
    """Get the Book Assistant Agent with current configuration."""
    # Recreate the model with current settings
    from openai import AsyncOpenAI
    from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel

    openrouter_client = AsyncOpenAI(
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": os.getenv("OPENROUTER_REFERER", "http://localhost:3000"),
            "X-Title": os.getenv("OPENROUTER_APP_TITLE", "AI Book Assistant"),
        }
    )

    current_model = OpenAIChatCompletionsModel(
        model=settings.OPENROUTER_MODEL,
        openai_client=openrouter_client,
    )
    # Note: max_tokens is controlled via RunConfig

    return Agent(
        name="BookAssistant",
        instructions=BOOK_ASSISTANT_INSTRUCTIONS,
        model=current_model,
        tools=[search_book, get_chapter_content, list_chapters, explain_concept],
    )


async def run_book_agent(
    query: str,
    selected_text: Optional[str] = None,
    chapter_filter: Optional[str] = None,
    user_profile: Optional[Dict[str, Any]] = None,
    conversation_history: Optional[list] = None,
) -> Dict[str, Any]:
    """
    Run the Book Assistant Agent with a user query.

    Args:
        query: The user's question
        selected_text: Optional text selected by the user for context
        chapter_filter: Optional chapter to focus on
        user_profile: Optional user profile for personalization
        conversation_history: Optional list of previous messages for memory

    Returns:
        Dict with answer and metadata
    """
    # Get the current agent with updated configuration
    book_assistant = get_book_assistant()

    # Build conversation context from history
    context_parts = []

    if conversation_history:
        # Add previous conversation for memory (limit to last 6 messages to save tokens)
        recent_history = conversation_history[-6:]
        history_text = "\n".join([
            f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content'][:300]}"
            for msg in recent_history
        ])
        context_parts.append(f"Previous conversation:\n{history_text}")

    if selected_text:
        context_parts.append(f"The user has selected this text for context:\n\"{selected_text[:500]}\"")

    if chapter_filter:
        context_parts.append(f"Focus on: {chapter_filter}")

    if user_profile:
        level = user_profile.get("experience_level", "beginner")
        languages = user_profile.get("known_languages", [])
        context_parts.append(f"User level: {level}")
        if languages:
            context_parts.append(f"Known languages: {', '.join(languages)}")

    context_parts.append(f"Current question: {query}")

    full_input = "\n\n".join(context_parts)

    # Run the agent with token limit to stay within OpenRouter free tier
    result = await Runner.run(
        book_assistant,
        input=full_input,
        max_turns=5,  # Limit turns to save tokens
        run_config=RunConfig(
            model_settings=ModelSettings(max_tokens=600)  # Stay within free tier limits
        )
    )

    # Extract tool calls made for transparency
    tool_calls = []
    for item in result.raw_responses:
        if hasattr(item, 'output') and item.output:
            for output in item.output:
                if hasattr(output, 'type') and output.type == 'function_call':
                    tool_calls.append({
                        "tool": output.name if hasattr(output, 'name') else "unknown",
                        "status": "completed"
                    })

    return {
        "answer": result.final_output,
        "tool_calls": tool_calls,
        "model": settings.OPENROUTER_MODEL,
        "agent": "BookAssistant",
    }
