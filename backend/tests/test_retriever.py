from app.services.retrieval.retriever import retrieve
from app.database.qdrant_db_client import get_db


def test_retrieve_returns_documents():
    client = get_db()
    docs = retrieve("what is langgraph", client)
    assert isinstance(docs, list)
    print(f"Retrieved {len(docs)} docs")
    for doc in docs:
        print(f"Score: {doc.metadata['score']:.4f} | Content: {doc.page_content[:100]}")


if __name__ == "__main__":
    client = get_db()
    docs = retrieve("what is langgraph", client)
    print(f"Total retrieved: {len(docs)}")
    for doc in docs:
        print(f"\nScore: {doc.metadata['score']:.4f}")
        print(f"Content: {doc.page_content[:200]}")
        print(f"Metadata: {doc.metadata}")