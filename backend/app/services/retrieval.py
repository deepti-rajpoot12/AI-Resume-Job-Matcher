from dataclasses import dataclass

from app.services.embeddings import embed_texts
from app.services.vector_store import VectorStoreError, get_collection, knowledge_base_ready


@dataclass
class RetrievedKnowledge:
    text: str
    metadata: dict[str, str]
    distance: float | None


def retrieve_career_knowledge(missing_skills: list[str], limit: int = 6) -> list[RetrievedKnowledge]:
    """Retrieve only the best local guidance chunks for the identified skill gaps."""
    skills = list(dict.fromkeys(skill.strip() for skill in missing_skills if skill.strip()))[:4]
    if not skills or not knowledge_base_ready():
        return []

    try:
        queries = [f"career learning guidance for {skill}" for skill in skills]
        result = get_collection().query(
            query_embeddings=embed_texts(queries),
            n_results=2,
            include=["documents", "metadatas", "distances"],
        )
    except VectorStoreError:
        raise
    except Exception as error:
        raise VectorStoreError("Career knowledge retrieval failed.") from error

    retrieved: list[RetrievedKnowledge] = []
    seen: set[str] = set()
    for documents, metadatas, distances in zip(result["documents"], result["metadatas"], result["distances"]):
        for document, metadata, distance in zip(documents, metadatas, distances):
            if document and document not in seen:
                seen.add(document)
                retrieved.append(RetrievedKnowledge(document, metadata or {}, distance))
    return retrieved[:limit]
