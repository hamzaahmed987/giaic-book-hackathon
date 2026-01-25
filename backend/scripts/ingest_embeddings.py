#!/usr/bin/env python3
"""
Embedding Ingestion Script

This script processes book content and stores embeddings in Qdrant
for RAG-based retrieval.

Usage:
    python scripts/ingest_embeddings.py --docs-path ../frontend/docs
"""

import asyncio
import argparse
import re
from pathlib import Path
from typing import List, Dict, Any
import uuid

from openai import AsyncOpenAI
from qdrant_client import AsyncQdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

# Configuration
OPENAI_API_KEY = ""  # Set via environment or .env
QDRANT_URL = "http://localhost:6333"
QDRANT_API_KEY = ""
COLLECTION_NAME = "book_content"
EMBEDDING_MODEL = "text-embedding-3-small"
CHUNK_SIZE = 500  # tokens approximately
CHUNK_OVERLAP = 50


class EmbeddingIngester:
    """Processes and ingests book content into vector database."""

    def __init__(
        self,
        openai_api_key: str,
        qdrant_url: str,
        qdrant_api_key: str = None,
    ):
        self.openai = AsyncOpenAI(api_key=openai_api_key)
        self.qdrant = AsyncQdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key if qdrant_api_key else None,
        )
        self.collection_name = COLLECTION_NAME

    async def ensure_collection(self):
        """Ensure the Qdrant collection exists."""
        collections = await self.qdrant.get_collections()
        exists = any(
            c.name == self.collection_name for c in collections.collections
        )

        if not exists:
            print(f"Creating collection: {self.collection_name}")
            await self.qdrant.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=1536,  # text-embedding-3-small dimension
                    distance=Distance.COSINE,
                ),
            )
        else:
            print(f"Collection {self.collection_name} already exists")

    async def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text."""
        response = await self.openai.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
        )
        return response.data[0].embedding

    def parse_mdx(self, content: str) -> Dict[str, Any]:
        """Parse MDX file content and extract metadata."""
        metadata = {}

        # Extract frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"\'')

        # Remove frontmatter from content
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)

        # Remove import statements
        content = re.sub(r'^import.*$', '', content, flags=re.MULTILINE)

        return {
            "metadata": metadata,
            "content": content.strip(),
        }

    def chunk_content(self, content: str, chapter_id: str, source: str) -> List[Dict[str, Any]]:
        """
        Chunk content into smaller pieces for embedding.

        Strategy:
        1. Split by headers first
        2. If section is too long, split by paragraphs
        3. Keep code blocks intact when possible
        """
        chunks = []

        # Split by level 2 headers
        sections = re.split(r'\n## ', content)

        for i, section in enumerate(sections):
            if i > 0:  # Add back the ## that was removed
                section = '## ' + section

            # Extract section title
            title_match = re.match(r'^##? (.+)', section)
            section_title = title_match.group(1) if title_match else "Introduction"

            # If section is short enough, keep as one chunk
            if len(section.split()) < CHUNK_SIZE:
                chunks.append({
                    "text": section.strip(),
                    "metadata": {
                        "chapter_id": chapter_id,
                        "section": section_title,
                        "source": source,
                        "chunk_index": len(chunks),
                    }
                })
            else:
                # Split by paragraphs
                paragraphs = section.split('\n\n')
                current_chunk = []
                current_size = 0

                for para in paragraphs:
                    para_size = len(para.split())

                    # Check if adding this paragraph exceeds limit
                    if current_size + para_size > CHUNK_SIZE and current_chunk:
                        chunks.append({
                            "text": '\n\n'.join(current_chunk).strip(),
                            "metadata": {
                                "chapter_id": chapter_id,
                                "section": section_title,
                                "source": source,
                                "chunk_index": len(chunks),
                            }
                        })
                        # Start new chunk with overlap
                        current_chunk = current_chunk[-1:] if current_chunk else []
                        current_size = len(current_chunk[0].split()) if current_chunk else 0

                    current_chunk.append(para)
                    current_size += para_size

                # Don't forget the last chunk
                if current_chunk:
                    chunks.append({
                        "text": '\n\n'.join(current_chunk).strip(),
                        "metadata": {
                            "chapter_id": chapter_id,
                            "section": section_title,
                            "source": source,
                            "chunk_index": len(chunks),
                        }
                    })

        return chunks

    async def ingest_file(self, file_path: Path):
        """Process and ingest a single MDX file."""
        print(f"Processing: {file_path}")

        content = file_path.read_text(encoding='utf-8')
        parsed = self.parse_mdx(content)

        # Determine chapter ID from path
        chapter_match = re.search(r'chapter-(\d+)', str(file_path))
        chapter_id = f"chapter-{chapter_match.group(1)}" if chapter_match else "intro"

        # Generate source name
        source = f"{chapter_id}/{file_path.stem}"

        # Chunk the content
        chunks = self.chunk_content(
            parsed["content"],
            chapter_id,
            source,
        )

        print(f"  Created {len(chunks)} chunks")

        # Generate embeddings and store
        points = []
        for chunk in chunks:
            embedding = await self.get_embedding(chunk["text"])
            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload={
                        "text": chunk["text"],
                        **chunk["metadata"],
                    }
                )
            )

        # Batch upsert
        if points:
            await self.qdrant.upsert(
                collection_name=self.collection_name,
                points=points,
            )
            print(f"  Stored {len(points)} embeddings")

    async def ingest_directory(self, docs_path: Path):
        """Process all MDX files in a directory."""
        print(f"Ingesting from: {docs_path}")

        # Find all MDX files
        mdx_files = list(docs_path.rglob("*.mdx"))
        print(f"Found {len(mdx_files)} MDX files")

        for file_path in mdx_files:
            await self.ingest_file(file_path)

        print("Ingestion complete!")


async def main():
    parser = argparse.ArgumentParser(description="Ingest book content into Qdrant")
    parser.add_argument(
        "--docs-path",
        type=str,
        default="../frontend/docs",
        help="Path to docs directory",
    )
    parser.add_argument(
        "--openai-key",
        type=str,
        default=None,
        help="OpenAI API key",
    )
    parser.add_argument(
        "--qdrant-url",
        type=str,
        default="http://localhost:6333",
        help="Qdrant URL",
    )

    args = parser.parse_args()

    # Get API key from args or environment
    import os
    openai_key = args.openai_key or os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("Error: OPENAI_API_KEY not provided")
        return

    qdrant_key = os.getenv("QDRANT_API_KEY")

    ingester = EmbeddingIngester(
        openai_api_key=openai_key,
        qdrant_url=args.qdrant_url,
        qdrant_api_key=qdrant_key,
    )

    await ingester.ensure_collection()
    await ingester.ingest_directory(Path(args.docs_path))


if __name__ == "__main__":
    asyncio.run(main())
