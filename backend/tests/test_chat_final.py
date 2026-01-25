from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print('Testing chat API endpoint...')

# Test the chat query endpoint
try:
    response = client.post('/api/chat/query', 
                          json={
                              "query": "What is this book about?",
                              "selected_text": None,
                              "chapter_id": None
                          })
    print('Chat query test:')
    print(f'  Status: {response.status_code}')
    if response.status_code == 200:
        print(f'  Response: {response.json()}')
    else:
        print(f'  Error: {response.text}')
except Exception as e:
    print(f'Chat query error: {e}')