"""Repeatable command for building the local career knowledge collection."""

import hashlib
import re
from pathlib import Path

from app.services.embeddings import embed_texts
from app.services.vector_store import get_collection

KNOWLEDGE_PATH = Path(__file__).resolve().parents[2] / "data" / "knowledge"
CHUNK_SIZE = 700
CHUNK_OVERLAP = 120


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Split text on word boundaries with a small overlap for retrieval context."""
    words = text.split()
    if not words:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(words):
        chunk = " ".join(words[start : start + chunk_size])
        chunks.append(chunk)
        if start + chunk_size >= len(words):
            break
        start += chunk_size - overlap
    return chunks


def document_metadata(path: Path, text: str) -> dict[str, str]:
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    skill = match.group(1).strip() if match else path.stem.replace("-", " ").title()
    return {"skill": skill, "topic": "career-development", "document_name": path.name}


def ingest_knowledge_base() -> int:
    documents = sorted(KNOWLEDGE_PATH.glob("*.md"))
    if not documents:
        raise RuntimeError("No career knowledge documents were found.")

    ids: list[str] = []
    chunks: list[str] = []
    metadatas: list[dict[str, str]] = []
    for path in documents:
        text = path.read_text(encoding="utf-8").strip()
        metadata = document_metadata(path, text)
        for index, chunk in enumerate(chunk_text(text)):
            digest = hashlib.sha256(f"{path.name}:{index}:{chunk}".encode()).hexdigest()
            ids.append(digest)
            chunks.append(chunk)
            metadatas.append({**metadata, "chunk_index": str(index)})

    collection = get_collection()
    collection.upsert(ids=ids, documents=chunks, metadatas=metadatas, embeddings=embed_texts(chunks))
    return len(chunks)


if __name__ == "__main__":
    count = ingest_knowledge_base()
    print(f"Ingested {count} career knowledge chunks.")
