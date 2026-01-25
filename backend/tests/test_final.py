import os
from app.core.config import settings
print('Current DATABASE_URL:', repr(settings.DATABASE_URL))
print('URL starts with asyncpg?', settings.DATABASE_URL.startswith('postgresql+asyncpg'))

# Also test importing the database module
try:
    from app.infrastructure.database import get_engine
    print("Database module imported successfully")
    
    # Try to get the engine
    engine = get_engine()
    print("Engine created successfully:", type(engine).__name__)
except Exception as e:
    print(f"Error creating engine: {e}")

# Test the chat endpoint again
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

try:
    response = client.post('/api/chat/query', 
                          json={
                              "query": "What is this book about?",
                              "selected_text": None,
                              "chapter_id": None
                          })
    print('\nChat query test:')
    print(f'  Status: {response.status_code}')
    if response.status_code == 200:
        print(f'  Response: {response.json()}')
    else:
        print(f'  Error: {response.text}')
except Exception as e:
    print(f'\nChat query error: {e}')