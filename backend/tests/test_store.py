from app.database.qdrant_db_client import get_db, store_documents
from app.services.ingestion.loader import load_document
from app.services.ingestion.chunker import chunk_documents
from app.services.ingestion.embedder import get_embeddings


def test_store_documents(tmp_path):
    sample = tmp_path / "test.txt"
    sample.write_text("LangGraph is a graph-based orchestration framework." * 10)

    docs = load_document(str(sample))
    chunks = chunk_documents(docs)
    embeddings = get_embeddings([c.page_content for c in chunks])
    client = get_db()

    count = store_documents(chunks, embeddings, client)
    assert count == len(chunks)
    print(f"Stored {count} chunks")


if __name__ == "__main__":
    pdf_path = r"Researchhub-AI\backend\research_papers\Ian Goodfellow, Yoshua Bengio, Aaron Courville - Deep Learning (2017, MIT).pdf"
    docs = load_document(pdf_path)
    chunks = chunk_documents(docs)
    embeddings = get_embeddings([c.page_content for c in chunks])
    client = get_db()
    count = store_documents(chunks, embeddings, client)
    print(f"Stored {count} chunks in Qdrant")