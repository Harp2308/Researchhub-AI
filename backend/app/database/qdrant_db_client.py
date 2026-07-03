from qdrant_client import QdrantClient
from qdrant_client import models
import uuid
from langchain_core.documents import Document
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

# def ensure_collection(client, name, dim):
#     if not client.collection_exists(name):
#         client.create_collection(
#             collection_name=name,
#             vectors_config=models.VectorParams(size=dim, distance=models.Distance.COSINE),
#         )
#         return
#     info = client.get_collection(name)
#     existing_dim = info.config.params.vectors.size
#     if existing_dim != dim:
#         raise RuntimeError(
#             f"Collection '{name}' has dim {existing_dim}, "
#             f"but current embedding model produces dim {dim}. "
#             f"Create a new collection or re-embed."
#         )

def get_db():
    client = get_qdrant_client()
    get_or_create_collection(client)
    return client



def store_documents(docs: list[Document], embeddings: list[list[float]], client: QdrantClient) -> int:
    points = [
        models.PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={
                "content": doc.page_content,
                "metadata": doc.metadata,
            }
        )
        for doc, embedding in zip(docs, embeddings)
    ]

    client.upsert(
        collection_name=settings.collection_name,
        points=points,
    )

    logger.info(f"Stored {len(points)} chunks in Qdrant")
    return len(points)