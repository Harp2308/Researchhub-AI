from app.services.ingestion.loader import load_document
from app.services.ingestion.chunker import chunk_documents


def test_chunking_txt(tmp_path):
    sample = tmp_path / "test.txt"
    sample.write_text("This is sentence one.\n\n" * 50)

    docs = load_document(str(sample))
    chunks = chunk_documents(docs)

    assert len(chunks) > 1
    assert chunks[0].metadata["chunk_index"] == 0
    assert chunks[0].metadata["chunk_total"] == len(chunks)
    print(f"Total chunks: {len(chunks)}")


def test_chunk_metadata_preserved(tmp_path):
    sample = tmp_path / "test.txt"
    sample.write_text("Content " * 200)
    
    docs = load_document(str(sample))
    
    print("==="*50,f"\n {docs}\n\n")
    
    chunks = chunk_documents(docs)

    for chunk in chunks:
        assert "filename" in chunk.metadata
        assert "source_type" in chunk.metadata
        assert "chunk_index" in chunk.metadata
    print("Metadata preserved across all chunks")


if __name__ == "__main__":
    pdf_path = r"E:\.harp_26\pocs\researchhub-ai\researchhub-ai\backend\research_papers\Ian Goodfellow, Yoshua Bengio, Aaron Courville - Deep Learning (2017, MIT).pdf"
    
    from app.services.ingestion.loader import load_document
    docs = load_document(pdf_path)
    chunks = chunk_documents(docs)
    print(f"Total chunks: {len(chunks)}")
    for i, chunk in enumerate(chunks[:3]):
        print(f"\nChunk {i}:")
        print(f"Content: {chunk.page_content[:200]}")
        print(f"Metadata: {chunk.metadata}")