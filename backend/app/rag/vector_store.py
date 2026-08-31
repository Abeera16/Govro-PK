from functools import lru_cache

import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma

from app.core.config import settings
from app.core.logging_config import logger
from app.rag.embeddings import get_embedding_function


@lru_cache
def get_chroma_client() -> chromadb.HttpClient:
    return chromadb.HttpClient(
        host=settings.chroma_host,
        port=settings.chroma_port,
        ssl=settings.chroma_ssl,
        settings=ChromaSettings(anonymized_telemetry=False),
    )


@lru_cache
def get_vector_store() -> Chroma:
    client = get_chroma_client()
    store = Chroma(
        client=client,
        collection_name=settings.chroma_collection,
        embedding_function=get_embedding_function(),
    )
    logger.info(f"Connected to Chroma collection '{settings.chroma_collection}'")
    return store


def upsert_chunks(texts: list[str], metadatas: list[dict], ids: list[str]) -> None:
    store = get_vector_store()
    store.add_texts(texts=texts, metadatas=metadatas, ids=ids)


def delete_by_source(source_url: str) -> None:
    client = get_chroma_client()
    collection = client.get_or_create_collection(settings.chroma_collection)
    collection.delete(where={"source_url": source_url})
