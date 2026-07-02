import pytest
from app.services.ingestion.loader import load_document


def test_load_txt(tmp_path):
    sample = tmp_path / "test.txt"
    sample.write_text("This is a test document for ResearchHub AI.")

    docs = load_document(str(sample))

    assert len(docs) > 0
    assert docs[0].metadata["filename"] == "test.txt"
    assert docs[0].metadata["source_type"] == "txt"
    assert "ResearchHub" in docs[0].page_content
    print("TXT loading works")


def test_load_md(tmp_path):
    sample = tmp_path / "test.md"
    sample.write_text("# Heading\nThis is markdown content.")

    docs = load_document(str(sample))

    assert len(docs) > 0
    assert docs[0].metadata["source_type"] == "md"
    print("MD loading works")


def test_unsupported_extension(tmp_path):
    sample = tmp_path / "test.csv"
    sample.write_text("col1,col2")

    with pytest.raises(ValueError):
        load_document(str(sample))
    print("Unsupported extension handled correctly")


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_document("nonexistent/path/file.txt")
    print("File not found handled correctly")


# def test_load_pdf():
#     # drop your pdf path here
#     pdf_path = "your_pdf_path_here.pdf"
#     docs = load_document(pdf_path)

#     assert len(docs) > 0
#     assert docs[0].metadata["source_type"] == "pdf"
#     print(f"PDF loaded: {len(docs)} pages")
#     for doc in docs:
#         print(f"Page {doc.metadata.get('page')}: {doc.page_content[:100]}")


if __name__ == "__main__":
    pdf_path = r"E:\.harp_26\pocs\researchhub-ai\researchhub-ai\backend\research_papers\Ian Goodfellow, Yoshua Bengio, Aaron Courville - Deep Learning (2017, MIT).pdf"
    docs = load_document(pdf_path)
    print(f"Total docs loaded: {len(docs)}")
    for doc in docs:
        print(f"\nFilename: {doc.metadata['filename']}")
        print(f"Source type: {doc.metadata['source_type']}")
        print(f"Content preview: {doc.page_content[:200]}")