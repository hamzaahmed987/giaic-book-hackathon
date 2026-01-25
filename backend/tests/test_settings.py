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