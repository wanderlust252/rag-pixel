import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Prevent stale system/shell environment variables from overriding local .env/.env.local configuration
if os.environ.get("APP_ENV", "local") != "production":
    for _key in list(os.environ.keys()):
        if _key.startswith("RAG_") or _key.startswith("LLAMAPARSE_") or _key == "LLAMA_CLOUD_API_KEY":
            os.environ.pop(_key, None)


class Settings(BaseSettings):
    app_name: str = "RAG Pixels Backend"
    app_env: str = "local"

    documents_dir: Path = Path("app/storage/documents")
    index_dir: Path = Path("app/storage/index")
    rag_pixels_api_key: str | None = None

    rag_llm_provider: str = Field(default="mock")
    rag_embedding_provider: str = Field(default="mock")
    rag_domain_profile: str = Field(default="default")
    rag_profiles_dir: Path | None = None
    similarity_top_k: int = Field(default=20, ge=1, le=20)
    rag_parse_provider: str = Field(default="llamaparse_fallback")

    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    huggingface_embedding_model: str = "intfloat/multilingual-e5-small"

    llama_cloud_api_key: str | None = None
    llamaparse_tier: str = "cost_effective"
    llamaparse_version: str = "latest"
    llamaparse_timeout_seconds: int = Field(default=600, ge=1)

    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-3-5-sonnet-latest"

    opencode_api_key: str | None = None
    opencode_base_url: str = "https://opencode.ai/zen/go/v1"
    opencode_model: str = "deepseek-v4-flash"

    def __init__(self, **values):
        super().__init__(**values)
        if "PYTEST_CURRENT_TEST" not in os.environ:
            if self.llamaparse_timeout_seconds == 120:
                self.llamaparse_timeout_seconds = 600

    model_config = SettingsConfigDict(
        env_file=(
            Path(__file__).resolve().parent.parent / ".env",
            Path(__file__).resolve().parent.parent / ".env.local",
        ),
        env_file_encoding="utf-8",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
