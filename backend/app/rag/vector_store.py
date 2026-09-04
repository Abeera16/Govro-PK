from __future__ import annotations

from functools import lru_cache
from typing import Any

from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
from qdrant_client.http.models import Distance, PointStruct, VectorParams

from app.core.config import settings
from app.core.logging_config import logger
from app.rag.embeddings import get_embedding_function


@lru_cache
def get_qdrant_client() -> QdrantClient:
    client = QdrantClient(url=settings.qdrant_url, api_key=settings.qdrant_api_key, timeout=30)
    collection_name = settings.qdrant_collection
    existing = client.get_collections().collections
    existing_names = {collection.name for collection in existing}

    if collection_name not in existing_names:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
        logger.info(f"Created Qdrant collection '{collection_name}'")
    else:
        logger.info(f"Connected to Qdrant collection '{collection_name}'")

    return client


@lru_cache
def get_vector_store() -> Any:
    client = get_qdrant_client()
    return {"client": client, "collection": settings.qdrant_collection}


def upsert_chunks(texts: list[str], metadatas: list[dict], ids: list[str]) -> None:
    if not texts:
        return

    embedding_fn = get_embedding_function()
    vectors = embedding_fn.embed_documents(texts)
    client = get_qdrant_client()
    points = [
        PointStruct(
            id=ids[idx],
            vector=vectors[idx],
            payload={**metadatas[idx], "text": texts[idx]},
        )
        for idx in range(len(texts))
    ]
    client.upsert(collection_name=settings.qdrant_collection, points=points)


def delete_by_source(source_url: str) -> None:
    client = get_qdrant_client()
    client.delete(
        collection_name=settings.qdrant_collection,
        points_selector=rest.Filter(
            must=[rest.FieldCondition(key="source_url", match=rest.MatchValue(value=source_url))]
        ),
    )


def similarity_search(query: str, k: int = 5, category: str | None = None) -> list[tuple[Document, float]]:
    embedding_fn = get_embedding_function()
    vector = embedding_fn.embed_query(query)
    client = get_qdrant_client()

    query_filter = None
    if category:
        query_filter = rest.Filter(
            must=[rest.FieldCondition(key="category", match=rest.MatchValue(value=category))]
        )

    response = client.query_points(
        collection_name=settings.qdrant_collection,
        query=vector,
        limit=k,
        query_filter=query_filter,
        with_payload=True,
    )
    results = response.points

    docs: list[tuple[Document, float]] = []
    for item in results:
        payload = item.payload or {}
        metadata = {
            "title": payload.get("title", "Government Source"),
            "source_url": payload.get("source_url", ""),
            "category": payload.get("category", "general"),
            "chunk_index": payload.get("chunk_index"),
        }
        doc = Document(page_content=payload.get("text", ""), metadata=metadata)
        docs.append((doc, float(item.score)))
    return docs
