"""
Embedding provider factory.

Defaults to FastEmbed — a free, local, no-API-key embedding library built on
ONNX Runtime (not PyTorch). This keeps the backend image small and the build
fast/reliable even on slow connections, since it avoids the large torch
download entirely. Set EMBEDDING_PROVIDER=openai in .env to use OpenAI
embeddings instead (requires OPENAI_API_KEY and billing).
"""
from functools import lru_cache
from typing import List

from app.core.config import settings
from app.core.logging_config import logger


class FastEmbedLangChainWrapper:
    """Thin adapter exposing the LangChain Embeddings interface (embed_documents/
    embed_query) around fastembed's TextEmbedding, so it drops into
    langchain_chroma.Chroma exactly like any other LangChain embeddings object."""

    def __init__(self, model_name: str):
        from fastembed import TextEmbedding

        logger.info(f"Loading local FastEmbed model '{model_name}' (first run downloads it)...")
        self._model = TextEmbedding(model_name=model_name)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [vec.tolist() for vec in self._model.embed(texts)]

    def embed_query(self, text: str) -> List[float]:
        return list(next(self._model.embed([text])).tolist())


@lru_cache
def get_embedding_function():
    provider = settings.embedding_provider.lower().strip()

    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        if not settings.openai_api_key:
            logger.warning("OPENAI_API_KEY not set — OpenAI embeddings will fail until configured.")
        return OpenAIEmbeddings(
            model=settings.openai_embedding_model,
            api_key=settings.openai_api_key,
        )

    # default: local, free, no API key, no torch required
    return FastEmbedLangChainWrapper(model_name=settings.local_embedding_model)
