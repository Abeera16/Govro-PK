from unittest.mock import MagicMock, patch

from langchain_core.documents import Document


with patch("app.rag.vector_store.get_embedding_function") as mock_get_embedding_function:
    mock_get_embedding_function.return_value = MagicMock()
    from app.rag import vector_store


def test_similarity_search_returns_langchain_documents_and_scores():
    mock_client = MagicMock()
    mock_client.get_collections.return_value = {"collections": []}
    mock_client.search.return_value = [
        MagicMock(id="1", score=0.92, payload={"text": "alpha", "title": "Doc 1", "source_url": "https://example.com", "category": "health"}),
        MagicMock(id="2", score=0.81, payload={"text": "beta", "title": "Doc 2", "source_url": "https://example.org", "category": "education"}),
    ]

    with patch.object(vector_store, "get_qdrant_client", return_value=mock_client):
        with patch.object(vector_store, "get_embedding_function", return_value=MagicMock(embed_query=lambda text: [0.1, 0.2, 0.3])):
            results = vector_store.similarity_search("test query", k=2, category="health")

    assert len(results) == 2
    assert all(isinstance(item[0], Document) for item in results)
    assert all(isinstance(item[1], float) for item in results)
    assert results[0][0].metadata["category"] == "health"
