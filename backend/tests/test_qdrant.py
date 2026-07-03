from app.database.qdrant_db_client import get_qdrant_client, get_or_create_collection, get_db
from app.config.settings import get_settings

settings = get_settings()


def test_qdrant_connection():
    client = get_qdrant_client()
    result = client.get_collections()
    assert result is not None
    print("Qdrant cloud connection successful")


def test_collection_creation():
    client = get_qdrant_client()
    get_or_create_collection(client)

    collections = client.get_collections().collections
    names = [c.name for c in collections]

    assert settings.collection_name in names
    print(f"Collection '{settings.collection_name}' verified")


def test_get_db():
    client = get_db()
    assert client is not None
    print("get_db() working correctly")
    
    
# if __name__ == "__main__":
#     test_qdrant_connection()
#     test_collection_creation()
#     test_get_db()