from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "RAG Pixels Backend"
    app_env: str = "local"

    documents_dir: Path = Path("app/storage/documents")
    index_dir: Path = Path("app/storage/index")

    rag_llm_provider: str = Field(default="mock")
    rag_embedding_provider: str = Field(default="mock")
    rag_domain_profile: str = Field(default="default")
    rag_profiles_dir: Path | None = None
    similarity_top_k: int = Field(default=20, ge=1, le=20)

    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    huggingface_embedding_model: str = "intfloat/multilingual-e5-small"

    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-3-5-sonnet-latest"

    opencode_api_key: str | None = None
    opencode_base_url: str = "https://opencode.ai/zen/go/v1"
    opencode_model: str = "deepseek-v4-flash"

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
