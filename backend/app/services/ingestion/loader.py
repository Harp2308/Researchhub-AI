from pathlib import Path
from pypdf import PdfReader
from langchain_core.documents import Document
from app.utils.logger import get_logger

logger = get_logger(__name__)

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def load_document(file_path: str) -> list[Document]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {path.suffix}. Supported: {SUPPORTED_EXTENSIONS}")

    logger.info(f"Loading file: {path.name} | type: {path.suffix}")

    if path.suffix == ".pdf":
        docs = _load_pdf(path)
    else:
        docs = _load_text(path)

    logger.info(f"Loaded {len(docs)} document(s) from {path.name}")
    return docs


def _load_pdf(path: Path) -> list[Document]:
    reader = PdfReader(str(path))
    docs = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        docs.append(Document(
            page_content=text,
            metadata={
                "filename": path.name,
                "source_type": "pdf",
                "page_number": i + 1,
            }
        ))
    return docs


def _load_text(path: Path) -> list[Document]:
    text = path.read_text(encoding="utf-8")
    return [Document(
        page_content=text,
        metadata={
            "filename": path.name,
            "source_type": path.suffix.replace(".", ""),
            "page_number": 1,
        }
    )]