from functools import lru_cache
from pathlib import Path


class VectorStoreError(Exception):
    """Raised when the local Chroma knowledge base cannot be used."""


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHROMA_PATH = PROJECT_ROOT / "data" / "chroma"
COLLECTION_NAME = "career_knowledge"


@lru_cache(maxsize=1)
def get_collection():
    try:
        import chromadb

        client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        return client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    except Exception as error:
        raise VectorStoreError("The local career knowledge base is unavailable.") from error


def knowledge_base_ready() -> bool:
    try:
        return get_collection().count() > 0
    except VectorStoreError:
        return False
