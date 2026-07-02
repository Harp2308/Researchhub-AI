from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, TextLoader
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
        loader = PyPDFLoader(str(path))
    elif path.suffix in {".txt", ".md"}:
        loader = TextLoader(str(path), encoding="utf-8")

    docs = loader.load()

    for doc in docs:
        doc.metadata["filename"] = path.name
        doc.metadata["source_type"] = path.suffix.replace(".", "")

    logger.info(f"Loaded {len(docs)} document(s) from {path.name}")
    return docs