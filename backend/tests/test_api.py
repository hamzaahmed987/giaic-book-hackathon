from app.main import app
from fastapi.testclient import TestClient

# Create test client
client = TestClient(app)

print("Testing API endpoints...")

# Test the root endpoint
try:
    response = client.get('/')
    print('Root endpoint test:')
    print(f'  Status: {response.status_code}')
    print(f'  Response: {response.json()}')
except Exception as e:
    print(f'Root endpoint error: {e}')

# Test the health endpoint  
try:
    response = client.get('/health')
    print('\nHealth endpoint test:')
    print(f'  Status: {response.status_code}')
    print(f'  Response: {response.json()}')
except Exception as e:
    print(f'Health endpoint error: {e}')

# Test the chat health endpoint
try:
    response = client.get('/api/chat/health')
    print('\nChat health endpoint test:')
    print(f'  Status: {response.status_code}')
    if response.status_code == 200:
        print(f'  Response: {response.json()}')
    else:
        print(f'  Error: {response.text}')
except Exception as e:
    print(f'Chat health endpoint error: {e}')

print("\nAPI tests completed.")