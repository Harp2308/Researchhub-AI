from qdrant_client import QdrantClient
from langchain_core.documents import Document
from app.config.settings import get_settings
from app.utils.logger import get_logger
from app.services.ingestion.embedder import get_embeddings

logger = get_logger(__name__)
settings = get_settings()


def retrieve(query: str, client: QdrantClient) -> list[Document]:
    query_vector = get_embeddings([query])[0]

    results = client.query_points(
        collection_name=settings.collection_name,
        query=query_vector,
        limit=settings.top_k,
        with_payload=True,
    ).points

    docs = []
    for r in results:
        docs.append(Document(
            page_content=r.payload.get("content", ""),
            metadata={
                **r.payload.get("metadata", {}),
                "score": r.score,
            }
        ))

    logger.info(f"Retrieved {len(docs)} chunks | query: {query[:50]}")
    return docs