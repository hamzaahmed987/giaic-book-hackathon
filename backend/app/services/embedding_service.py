"""
Embedding service using Cohere.
"""
from typing import List

import cohere

from app.core.config import settings


class EmbeddingService:
    """Service for generating embeddings using Cohere."""

    def __init__(self):
        self.client = cohere.Client(api_key=settings.COHERE_API_KEY)
        self.model = settings.COHERE_EMBEDDING_MODEL

    async def get_embedding(self, text: str) -> List[float]:
        """Get embedding for a single text."""
        response = self.client.embed(
            texts=[text],
            model=self.model,
            input_type="search_query",  # Use "search_query" for queries, "search_document" for docs
        )
        return response.embeddings[0]

    async def get_embeddings(self, texts: List[str], input_type: str = "search_document") -> List[List[float]]:
        """
        Get embeddings for multiple texts.

        Args:
            texts: List of texts to embed
            input_type: "search_query" for queries, "search_document" for documents
        """
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type=input_type,
        )
        return response.embeddings


# Global instance
embedding_service = EmbeddingService()
