from app.core.config import settings
print('Current DATABASE_URL:', repr(settings.DATABASE_URL))
print('URL starts with asyncpg?', settings.DATABASE_URL.startswith('postgresql+asyncpg'))

# Test creating the engine
from app.infrastructure.database import get_engine
try:
    engine = get_engine()
    print('Engine created successfully!')
except Exception as e:
    print(f'Engine creation failed: {e}')