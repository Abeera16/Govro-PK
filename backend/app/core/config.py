from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: str = "development"
    log_level: str = "INFO"

    # Postgres
    database_url: str = "postgresql+asyncpg://civicai:civicai_pass@localhost:5432/civicai"

    # Chroma
    chroma_host: str = "localhost"
    chroma_port: int = 8001
    chroma_collection: str = "civicai_gov_docs"

    # LLM provider selection: "groq" (default, free-tier friendly) or "openai"
    llm_provider: str = "groq"

    # Groq
    groq_api_key: str = ""
    groq_chat_model: str = "llama-3.3-70b-versatile"

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
    langchain_project: str = "civicai"
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


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
