#!/usr/bin/env python3
"""
Test script for the Book Assistant Agent using OpenAI Agents SDK with OpenRouter.
"""
import asyncio
import os
from pathlib import Path

# Add the backend directory to the path so we can import modules
BACKEND_DIR = Path(__file__).parent
os.chdir(BACKEND_DIR)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

from app.agents.book_agent import run_book_agent


async def test_agent():
    """Test the book agent with sample queries."""
    print("Testing Book Assistant Agent with OpenAI Agents SDK and OpenRouter...")
    print("=" * 70)
    
    # Test queries
    test_queries = [
        {
            "query": "What are the foundations of artificial intelligence?",
            "description": "Basic AI concepts"
        },
        {
            "query": "Explain how large language models work",
            "description": "LLM fundamentals"
        },
        {
            "query": "How do I create effective prompts for AI models?",
            "description": "Prompt engineering"
        },
        {
            "query": "What is RAG and how does it work?",
            "description": "RAG systems"
        }
    ]
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        print("-" * 50)
        
        try:
            result = await run_book_agent(
                query=test_case['query'],
                user_profile={
                    "experience_level": "beginner",
                    "known_languages": ["Python"]
                }
            )
            
            print(f"Answer: {result['answer'][:500]}...")
            print(f"Model: {result['model']}")
            print(f"Tools used: {len(result['tool_calls'])}")
            for tool_call in result['tool_calls']:
                print(f"  - {tool_call['tool']}: {tool_call['status']}")
                
        except Exception as e:
            print(f"Error in test {i}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("Agent testing completed!")


async def test_specific_features():
    """Test specific agent features."""
    print("\nTesting Specific Agent Features...")
    print("=" * 70)
    
    # Test with selected text context
    print("\n1. Testing with selected text context:")
    selected_text = "Artificial Intelligence is a branch of computer science that aims to create software or machines that exhibit human-like intelligence."
    result = await run_book_agent(
        query="Can you expand on this concept?",
        selected_text=selected_text,
        user_profile={"experience_level": "intermediate"}
    )
    print(f"Response length: {len(result['answer'])} characters")
    print(f"Tools used: {len(result['tool_calls'])}")
    
    # Test with chapter filter
    print("\n2. Testing with chapter filter:")
    result = await run_book_agent(
        query="What are the key concepts about neural networks?",
        chapter_filter="chapter-1",
        user_profile={"experience_level": "beginner"}
    )
    print(f"Response length: {len(result['answer'])} characters")
    print(f"Tools used: {len(result['tool_calls'])}")
    
    print("\nSpecific feature tests completed!")


if __name__ == "__main__":
    # Run the tests
    asyncio.run(test_agent())
    asyncio.run(test_specific_features())