from functools import lru_cache
import json
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    log_level: str = "INFO"

    # CORS — JSON or comma-separated list of allowed frontend origins
    cors_origins: Annotated[list[str], NoDecode] = [
        "http://localhost:5173",
        "https://govro-pk-4ipj-git-main-abeera-amir-s-projects.vercel.app",
    ]

    # Postgres
    database_url: str = "postgresql+asyncpg://govropk:govropk_pass@localhost:5432/govropk"

    # Qdrant Cloud
    qdrant_url: str = ""
    qdrant_api_key: str = ""
    qdrant_collection: str = "govropk_gov_docs"

    # LLM provider selection: "groq" (default) or "openai"
    llm_provider: str = "groq"

    # Groq
    # openai/gpt-oss-120b is a model served by Groq, not the OpenAI API.
    groq_api_key: str = ""
    groq_chat_model: str = "openai/gpt-oss-120b"

    # OpenAI (optional — only used if llm_provider="openai")
    openai_api_key: str = ""
    openai_chat_model: str = "gpt-4o-mini"

    # Embeddings: local, no API key required (used for RAG regardless of llm_provider)
    embedding_provider: str = "local"
    local_embedding_model: str = "BAAI/bge-small-en-v1.5"
    openai_embedding_model: str = "text-embedding-3-small"

    # Tavily
    tavily_api_key: str = ""

    # LangSmith
    langchain_tracing_v2: bool = False
    langchain_api_key: str = ""
    langchain_project: str = "govropk"
    langchain_endpoint: str = "https://api.smith.langchain.com"

    # JWT
    jwt_secret_key: str = "insecure-dev-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    refresh_token_expire_days: int = 7

    # MCP
    mcp_server_host: str = "0.0.0.0"
    mcp_server_port: int = 8765
    mcp_server_url: str = "http://localhost:8765"

    @field_validator("cors_origins", mode="before")
    @classmethod
    def split_cors_origins(cls, v):
        if isinstance(v, str):
            value = v.strip()
            if not value:
                return []
            try:
                decoded = json.loads(value)
            except json.JSONDecodeError:
                decoded = value.split(",")
            if isinstance(decoded, list):
                return [origin.strip() for origin in decoded if origin.strip()]
            return [str(decoded).strip()]
        return v


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()