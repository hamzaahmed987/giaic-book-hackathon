"""
RAG (Retrieval-Augmented Generation) service.
"""
from typing import Optional, Dict, Any, List

from openai import AsyncOpenAI

from app.core.config import settings
from app.services.embedding_service import embedding_service
from app.infrastructure.vector_store import vector_store


class RAGService:
    """RAG service for question answering."""

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

    async def query(
        self,
        query: str,
        selected_text: Optional[str] = None,
        chapter_filter: Optional[str] = None,
        user_profile: Optional[Dict[str, Any]] = None,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Process a RAG query.

        Args:
            query: The user's question
            selected_text: Optional text selected by the user for context
            chapter_filter: Optional chapter to filter results
            user_profile: Optional user profile for personalization
            top_k: Number of documents to retrieve

        Returns:
            Dict with answer and citations
        """
        # Build the query with selected text context
        full_query = query
        if selected_text:
            full_query = f"Regarding this text: '{selected_text[:500]}'\n\nQuestion: {query}"

        # Get query embedding
        query_embedding = await embedding_service.get_embedding(full_query)

        # Search vector store
        results = await vector_store.search(
            query_vector=query_embedding,
            limit=top_k,
            filter_chapter=chapter_filter,
        )

        # Build context from retrieved documents
        context_parts = []
        citations = []
        for i, result in enumerate(results):
            payload = result.get("payload", {})
            text = payload.get("text", "")
            chapter = payload.get("chapter_id", "unknown")
            source = payload.get("source", "Book Content")

            context_parts.append(f"[{i + 1}] {text}")
            citations.append({
                "id": i + 1,
                "source": source,
                "chapter": chapter,
                "score": result.get("score", 0),
            })

        context = "\n\n".join(context_parts)

        # Build system prompt
        system_prompt = self._build_system_prompt(context, user_profile)

        # Generate response
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=0.7,
            max_tokens=1000,
        )

        answer = response.choices[0].message.content

        return {
            "answer": answer,
            "citations": citations,
        }

    def _build_system_prompt(
        self,
        context: str,
        user_profile: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build the system prompt for the LLM."""
        base_prompt = f"""You are a helpful AI assistant for an educational book about AI development.

Answer questions based on the following context from the book. If the answer isn't in the context, say "I don't have information about that in the book."

When citing information, reference the source numbers in brackets like [1], [2], etc.

Context:
{context}
"""

        # Add personalization if user profile exists
        if user_profile:
            level = user_profile.get("experience_level", "beginner")
            languages = user_profile.get("known_languages", [])

            personalization = f"""

Adjust your explanation for a {level} learner."""

            if languages:
                personalization += f" They are familiar with: {', '.join(languages)}."

            base_prompt += personalization

        return base_prompt


# Global instance
rag_service = RAGService()
