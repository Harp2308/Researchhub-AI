from pathlib import Path
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    
    model_config = ConfigDict(
        env_file=Path(__file__).parent.parent.parent.parent / ".env",
        env_file_encoding = "utf-8",
        extra = "ignore",
        case_sensitive = False
    )
    
    # LLM - Groq
    groq_api_key: str
    groq_model: str = "llama-3.1-8b-instant"

    # Embeddings - HuggingFace api
    hf_api_key: str =""
    embedding_model: str = "BAAI/bge-base-en-v1.5"
    embedding_dimensions: int = 768


    # Qdrant
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    collection_name: str = "researchhub"

    # Chunking
    chunk_size: int = 512
    chunk_overlap: int = 50

    # Retrieval
    top_k: int = 5

    # LangSmith
    langsmith_api_key: str
    langsmith_tracing_v2: bool = True
    langsmith_project: str = "researchhub-ai"

    


@lru_cache()
def get_settings() -> Settings:
    return Settings()
