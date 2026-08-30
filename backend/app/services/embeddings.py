from functools import lru_cache


class EmbeddingServiceError(Exception):
    """Raised when the local embedding model cannot be loaded or used."""


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the local model once per backend process."""
    try:
        from sentence_transformers import SentenceTransformer

        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception as error:
        raise EmbeddingServiceError("The local embedding model is unavailable.") from error


def embed_texts(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    try:
        embeddings = get_embedding_model().encode(texts, normalize_embeddings=True)
        return embeddings.tolist()
    except EmbeddingServiceError:
        raise
    except Exception as error:
        raise EmbeddingServiceError("The local embedding model could not create embeddings.") from error
