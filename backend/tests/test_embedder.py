from app.services.ingestion.embedder import get_embeddings
from app.config.settings import get_settings

settings = get_settings()


def test_single_embedding():
    result = get_embeddings(["LangGraph is a graph-based orchestration framework."])
    assert len(result) == 1
    assert len(result[0]) == settings.embedding_dimensions
    print(f"Embedding dim: {len(result[0])}")


def test_batch_embeddings():
    texts = ["Document one content.", "Document two content.", "Document three."]
    result = get_embeddings(texts)
    assert len(result) == 3
    assert all(len(e) == settings.embedding_dimensions for e in result)
    print(f"Batch embeddings: {len(result)}")


if __name__ == "__main__":
    texts = ["Testing HF embedding API for ResearchHub AI."]
    result = get_embeddings(texts)
    print(f"Dims: {len(result[0])}")
    print(f"First 5 values: {result[0][:5]}")