from qdrant_client import QdrantClient
from qdrant_client import models
from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


def get_qdrant_client() -> QdrantClient:
    client = QdrantClient(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
        timeout=30
    )
    return client


def get_or_create_collection(client: QdrantClient) -> None:
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if settings.collection_name not in names:
        client.create_collection(
            collection_name=settings.collection_name,
            vectors_config=models.VectorParams(
                size=settings.embedding_dimensions,
                distance=models.Distance.COSINE
            )
        )
        logger.info(f"Collection created: {settings.collection_name}")
    else:
        logger.info(f"Collection already exists: {settings.collection_name}")


def get_db():
    client = get_qdrant_client()
    get_or_create_collection(client)
    return client