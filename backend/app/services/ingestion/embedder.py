from langchain_huggingface import HuggingFaceEndpointEmbeddings
from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


def get_embedder() -> HuggingFaceEndpointEmbeddings:
    return HuggingFaceEndpointEmbeddings(
        model=settings.embedding_model,
        huggingfacehub_api_token=settings.hf_api_key,
    )


def get_embeddings(texts: list[str]) -> list[list[float]]:
    embedder = get_embedder()
    embeddings = embedder.embed_documents(texts)
    logger.info(f"Generated {len(embeddings)} embeddings | model: {settings.embedding_model}")
    return embeddings