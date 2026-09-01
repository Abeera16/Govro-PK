from app.core.logging_config import logger
from app.models.schemas import Citation
from app.rag.vector_store import similarity_search


async def retrieve_gov_documents(query: str, k: int = 5, category: str | None = None) -> list[dict]:
    """Retrieve top-k chunks from the Qdrant-backed RAG index with similarity scores + metadata."""
    try:
        results = similarity_search(query, k=k, category=category)
    except Exception as exc:  # noqa: BLE001
        logger.error(f"Qdrant retrieval failed: {exc}")
        return []

    docs = []
    for doc, score in results:
        docs.append(
            {
                "text": doc.page_content,
                "score": score,
                "title": doc.metadata.get("title", "Government Source"),
                "url": doc.metadata.get("source_url", ""),
                "category": doc.metadata.get("category", "general"),
            }
        )
    return docs


def docs_to_citations(docs: list[dict], source_type: str = "gov_rag") -> list[Citation]:
    citations = []
    for d in docs:
        citations.append(
            Citation(
                title=d.get("title", "Government Source"),
                url=d.get("url", ""),
                snippet=(d.get("text", "")[:220] + "...") if len(d.get("text", "")) > 220 else d.get("text", ""),
                source_type=source_type,
            )
        )
    return citations
