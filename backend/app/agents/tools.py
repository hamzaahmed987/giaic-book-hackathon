"""
Function tools for the Book Assistant Agent with enhanced context management.
"""
import asyncio
from typing import Optional, List, Dict, Any
from agents import function_tool

import cohere

from app.core.config import settings


# Initialize Cohere client for embeddings
cohere_client = cohere.Client(api_key=settings.COHERE_API_KEY)


def get_embedding(text: str) -> List[float]:
    """Get embedding for text using Cohere."""
    response = cohere_client.embed(
        texts=[text],
        model=settings.COHERE_EMBEDDING_MODEL,
        input_type="search_query",
    )
    return response.embeddings[0]


@function_tool
def search_book(query: str, chapter_filter: Optional[str] = None, context_window: int = 5) -> str:
    """
    Search the book content using semantic search with enhanced context management.

    Args:
        query: The search query to find relevant content in the book
        chapter_filter: Optional chapter ID to limit search (e.g., "chapter-1")
        context_window: Number of results to return (default 5)

    Returns:
        Relevant excerpts from the book with source information and context
    """
    from qdrant_client import QdrantClient
    from qdrant_client.models import Filter, FieldCondition, MatchValue

    # Initialize Qdrant client
    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )

    # Get query embedding
    query_embedding = get_embedding(query)

    # Build filter if chapter specified
    search_filter = None
    if chapter_filter:
        search_filter = Filter(
            must=[
                FieldCondition(
                    key="chapter_id",
                    match=MatchValue(value=chapter_filter)
                )
            ]
        )

    # Search Qdrant
    results = client.search(
        collection_name=settings.QDRANT_COLLECTION,
        query_vector=query_embedding,
        limit=context_window,
        query_filter=search_filter,
    )

    if not results:
        return "No relevant content found in the book for this query."

    # Format results with enhanced context
    formatted_results = []
    for i, result in enumerate(results, 1):
        payload = result.payload or {}
        text = payload.get("text", "")
        chapter = payload.get("chapter_id", "unknown")
        source = payload.get("source", "Book Content")
        score = result.score
        page_number = payload.get("page_number", "N/A")

        # Enhanced context with page numbers and more metadata
        formatted_result = (
            f"[{i}] (Chapter: {chapter}, Page: {page_number}, Relevance: {score:.2f})\n"
            f"{text[:500]}..." if len(text) > 500 else f"[{i}] (Chapter: {chapter}, Page: {page_number}, Relevance: {score:.2f})\n{text}"
        )
        formatted_results.append(formatted_result)

    return "\n\n---\n\n".join(formatted_results)


@function_tool
def get_chapter_content(chapter_id: str, include_context: bool = True) -> str:
    """
    Get the full content of a specific chapter with enhanced context management.

    Args:
        chapter_id: The chapter identifier (e.g., "chapter-1", "chapter-2")
        include_context: Whether to include additional context like learning objectives

    Returns:
        The chapter content or an error message if not found
    """
    import os

    # Map chapter_id to file path
    docs_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
        "..", "frontend", "docs", chapter_id
    )

    overview_path = os.path.join(docs_path, "overview.mdx")

    if os.path.exists(overview_path):
        with open(overview_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Enhanced context with chapter summary
        chapter_info = {
            "chapter-1": {"title": "AI Foundations", "objectives": ["Understand AI history", "Learn types of AI", "Grasp ML basics"]},
            "chapter-2": {"title": "LLM Fundamentals", "objectives": ["Understand transformers", "Learn tokenization", "Explore APIs"]},
            "chapter-3": {"title": "Prompt Engineering", "objectives": ["Master CRAFT framework", "Learn few-shot prompting", "Understand chain-of-thought"]},
            "chapter-4": {"title": "RAG Systems", "objectives": ["Learn embeddings", "Understand vector databases", "Explore retrieval methods"]},
            "chapter-5": {"title": "AI Agents", "objectives": ["Learn function calling", "Understand agent loops", "Explore orchestration"]},
            "chapter-6": {"title": "Building AI Apps", "objectives": ["Full-stack development", "Deployment strategies", "Production considerations"]}
        }

        chapter_details = chapter_info.get(chapter_id, {"title": chapter_id, "objectives": []})

        if include_context:
            context_section = f"Learning Objectives for {chapter_details['title']}:\n"
            for obj in chapter_details['objectives']:
                context_section += f"- {obj}\n"
            context_section += "\n"

            return f"{context_section}Chapter Overview for {chapter_id} ({chapter_details['title']}):\n\n{content[:2000]}..."
        else:
            return f"Chapter Overview for {chapter_id} ({chapter_details['title']}):\n\n{content[:2000]}..."

    return f"Chapter {chapter_id} not found. Available chapters: chapter-1 through chapter-6."


@function_tool
def list_chapters() -> str:
    """
    List all available chapters in the book with enhanced context.

    Returns:
        A formatted list of all book chapters with their topics and learning objectives
    """
    chapters = [
        {
            "id": "chapter-1",
            "title": "AI Foundations",
            "desc": "Core concepts, history, and types of AI",
            "key_topics": ["AI History", "Types of AI", "Machine Learning Basics"]
        },
        {
            "id": "chapter-2",
            "title": "LLM Fundamentals",
            "desc": "Understanding Large Language Models",
            "key_topics": ["Transformers", "Tokenization", "APIs"]
        },
        {
            "id": "chapter-3",
            "title": "Prompt Engineering",
            "desc": "Crafting effective AI prompts",
            "key_topics": ["CRAFT Framework", "Few-Shot Learning", "Chain-of-Thought"]
        },
        {
            "id": "chapter-4",
            "title": "RAG Systems",
            "desc": "Retrieval-Augmented Generation",
            "key_topics": ["Embeddings", "Vector Databases", "Retrieval Methods"]
        },
        {
            "id": "chapter-5",
            "title": "AI Agents",
            "desc": "Building autonomous AI systems",
            "key_topics": ["Function Calling", "Agent Loops", "Orchestration"]
        },
        {
            "id": "chapter-6",
            "title": "Building AI Apps",
            "desc": "Full-stack AI development",
            "key_topics": ["Frontend Integration", "Backend Services", "Deployment"]
        },
    ]

    result = "Available Book Chapters:\n\n"
    for ch in chapters:
        result += f"- **{ch['id']}**: {ch['title']}\n"
        result += f"  {ch['desc']}\n"
        result += f"  Key Topics: {', '.join(ch['key_topics'])}\n\n"

    return result


@function_tool
def explain_concept(concept: str, experience_level: str = "beginner", include_examples: bool = True) -> str:
    """
    Get a detailed explanation of a concept adapted to the user's level with examples.

    Args:
        concept: The AI/ML concept to explain
        experience_level: User's level - "beginner", "intermediate", or "advanced"
        include_examples: Whether to include practical examples

    Returns:
        An explanation tailored to the user's experience level with examples
    """
    # First search for the concept
    search_results = search_book.func(query=concept)

    level_context = {
        "beginner": {
            "instructions": "Explain in simple terms with analogies. Avoid jargon.",
            "depth": "surface level with intuitive understanding",
            "examples": "simple, everyday analogies"
        },
        "intermediate": {
            "instructions": "Balance theory and practice. Include some technical details.",
            "depth": "moderate depth with practical applications",
            "examples": "technical examples with some complexity"
        },
        "advanced": {
            "instructions": "Focus on nuances, edge cases, and advanced patterns.",
            "depth": "deep dive with implementation details",
            "examples": "complex, production-level examples"
        }
    }

    context_info = level_context.get(experience_level, level_context["beginner"])

    # Enhanced explanation with examples based on level
    explanation = f"Explanation for '{concept}' at {experience_level} level:\n\n"
    explanation += f"Guidelines: {context_info['instructions']}\n"
    explanation += f"Depth: {context_info['depth']}\n"

    if include_examples:
        explanation += f"Example Type: {context_info['examples']}\n\n"

    explanation += f"Relevant book content:\n{search_results}"

    return explanation


@function_tool
def get_learning_path(topic: str, experience_level: str = "beginner") -> str:
    """
    Generate a personalized learning path for a specific topic based on experience level.

    Args:
        topic: The topic to create a learning path for
        experience_level: User's level - "beginner", "intermediate", or "advanced"

    Returns:
        A structured learning path with recommended chapters and sequence
    """
    # Search for relevant content first
    search_results = search_book.func(query=topic)

    # Define learning paths based on experience level
    learning_paths = {
        "beginner": [
            "Start with Chapter 1: AI Foundations to understand basic concepts",
            "Move to Chapter 2: LLM Fundamentals to grasp how language models work",
            "Continue with Chapter 3: Prompt Engineering for practical skills",
            "Then Chapter 4: RAG Systems for advanced techniques",
            "Followed by Chapter 5: AI Agents for building intelligent systems",
            "Finish with Chapter 6: Building AI Apps for full implementation"
        ],
        "intermediate": [
            "Begin with Chapter 2: LLM Fundamentals to solidify understanding",
            "Proceed to Chapter 3: Prompt Engineering for advanced techniques",
            "Study Chapter 4: RAG Systems for practical implementations",
            "Explore Chapter 5: AI Agents for building complex systems",
            "Complete with Chapter 6: Building AI Apps for deployment"
        ],
        "advanced": [
            "Focus on Chapter 4: RAG Systems for cutting-edge techniques",
            "Deep-dive into Chapter 5: AI Agents for advanced architectures",
            "Master Chapter 6: Building AI Apps for production systems",
            "Review other chapters for foundational reinforcement as needed"
        ]
    }

    path = learning_paths.get(experience_level, learning_paths["beginner"])

    result = f"Personalized Learning Path for '{topic}' at {experience_level} level:\n\n"
    for i, step in enumerate(path, 1):
        result += f"{i}. {step}\n"

    result += f"\nRelevant content found:\n{search_results}"

    return result
