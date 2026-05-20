import json
import logging
import shutil
from pathlib import Path
from time import perf_counter
from typing import Any

from app.config import Settings
from app.rag.metadata import (
    REGISTRY_FILENAME,
    detail_from_metadata,
    load_sidecar_metadata,
    summary_from_metadata,
)
from app.rag.profile import DomainProfile, DomainProfileService
from app.rag.schemas import DocumentDetail, DocumentSummary

logger = logging.getLogger(__name__)


class RagIndexService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def build_and_persist(self, documents: list[Any]) -> None:
        started_at = perf_counter()
        self._configure_llama_index(include_llm=False)

        from llama_index.core import StorageContext, VectorStoreIndex

        self.settings.index_dir.mkdir(parents=True, exist_ok=True)
        storage_context = StorageContext.from_defaults()
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
        index.storage_context.persist(persist_dir=str(self.settings.index_dir))
        self._write_registry(documents)
        logger.info(
            "RAG build_and_persist completed in %.3fs for %d document(s)",
            perf_counter() - started_at,
            len(documents),
        )

    def load(self, *, include_llm: bool = True):
        started_at = perf_counter()
        self._configure_llama_index(include_llm=include_llm)

        from llama_index.core import StorageContext, load_index_from_storage

        if not self.settings.index_dir.exists():
            raise FileNotFoundError("RAG index does not exist. Run POST /documents/ingest first.")

        storage_context = StorageContext.from_defaults(persist_dir=str(self.settings.index_dir))
        index = load_index_from_storage(storage_context)
        logger.info("RAG index load completed in %.3fs", perf_counter() - started_at)
        return index

    def list_documents(self) -> list[DocumentSummary]:
        indexed = self._read_registry()
        if indexed:
            return [summary_from_metadata(metadata) for metadata in indexed]
        return [summary_from_metadata(metadata) for metadata in self._read_source_metadata()]

    def get_document(self, doc_id: str) -> DocumentDetail | None:
        for metadata in self._read_registry():
            if metadata.get("doc_id") == doc_id:
                return detail_from_metadata(metadata)
        for metadata in self._read_source_metadata():
            if metadata.get("doc_id") == doc_id:
                return detail_from_metadata(metadata)
        return None

    def clear(self) -> bool:
        if not self.settings.index_dir.exists():
            return False
        shutil.rmtree(self.settings.index_dir)
        return True

    def _configure_llama_index(self, *, include_llm: bool = True) -> None:
        started_at = perf_counter()
        from llama_index.core import Settings as LlamaSettings

        profile = DomainProfileService(self.settings).load()

        if not include_llm:
            from llama_index.core.llms.mock import MockLLM

            LlamaSettings.llm = MockLLM(max_tokens=256)
        elif self.settings.rag_llm_provider == "mock":
            from llama_index.core.llms.mock import MockLLM

            LlamaSettings.llm = MockLLM(max_tokens=256)
        elif self.settings.rag_llm_provider == "openai":
            if not self.settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when RAG_LLM_PROVIDER=openai")

            from llama_index.llms.openai import OpenAI

            LlamaSettings.llm = OpenAI(
                model=self.settings.openai_model,
                api_key=self.settings.openai_api_key,
            )
        elif self.settings.rag_llm_provider == "anthropic":
            if not self.settings.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY is required when RAG_LLM_PROVIDER=anthropic")

            from llama_index.llms.anthropic import Anthropic

            LlamaSettings.llm = Anthropic(
                model=self.settings.anthropic_model,
                api_key=self.settings.anthropic_api_key,
            )
        elif self.settings.rag_llm_provider == "opencode_go":
            if not self.settings.opencode_api_key:
                raise ValueError("OPENCODE_API_KEY is required when RAG_LLM_PROVIDER=opencode_go")

            from llama_index.llms.openai_like import OpenAILike

            LlamaSettings.llm = OpenAILike(
                api_base=self.settings.opencode_base_url,
                api_key=self.settings.opencode_api_key,
                model=self.settings.opencode_model,
                is_chat_model=True,
            )
        else:
            raise ValueError(f"Unsupported RAG_LLM_PROVIDER: {self.settings.rag_llm_provider}")

        embedding_provider = self._embedding_provider(profile)
        if embedding_provider == "mock":
            from llama_index.core.embeddings.mock_embed_model import MockEmbedding

            LlamaSettings.embed_model = MockEmbedding(embed_dim=1536)
        elif embedding_provider == "openai":
            if not self.settings.openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY is required when RAG_EMBEDDING_PROVIDER=openai"
                )

            from llama_index.embeddings.openai import OpenAIEmbedding

            LlamaSettings.embed_model = OpenAIEmbedding(
                model=self.settings.openai_embedding_model,
                api_key=self.settings.openai_api_key,
            )
        elif embedding_provider == "huggingface":
            from llama_index.embeddings.huggingface import HuggingFaceEmbedding

            LlamaSettings.embed_model = HuggingFaceEmbedding(
                **self._huggingface_embedding_kwargs(profile)
            )
        else:
            raise ValueError(
                f"Unsupported RAG embedding provider: {embedding_provider}"
            )

        logger.info(
            "RAG llama settings configured in %.3fs (llm=%s, embedding=%s)",
            perf_counter() - started_at,
            self.settings.rag_llm_provider if include_llm else "mock_retrieval_only",
            embedding_provider,
        )

    def _embedding_provider(self, profile: DomainProfile) -> str:
        if self.settings.rag_embedding_provider != "mock":
            return self.settings.rag_embedding_provider
        return profile.embedding.provider

    def _huggingface_embedding_kwargs(self, profile: DomainProfile | None = None) -> dict[str, Any]:
        profile = profile or DomainProfileService(self.settings).load()
        settings_default_model = Settings.model_fields["huggingface_embedding_model"].default
        model_name = (
            self.settings.huggingface_embedding_model
            if self.settings.huggingface_embedding_model != settings_default_model
            else profile.embedding.huggingface_model
        )
        if not model_name:
            raise ValueError("A Hugging Face embedding model must be configured")

        kwargs: dict[str, Any] = {"model_name": model_name}
        if profile.embedding.use_e5_instructions and "e5" in model_name.lower():
            kwargs.update(
                {
                    "query_instruction": "query: ",
                    "text_instruction": "passage: ",
                }
            )
        return kwargs

    def _registry_path(self) -> Path:
        return self.settings.index_dir / REGISTRY_FILENAME

    def _write_registry(self, documents: list[Any]) -> None:
        unique: dict[str, dict[str, Any]] = {}
        for document in documents:
            metadata = dict(document.metadata)
            unique[metadata["doc_id"]] = metadata

        self._registry_path().write_text(
            json.dumps(list(unique.values()), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _read_registry(self) -> list[dict[str, Any]]:
        registry_path = self._registry_path()
        if not registry_path.exists():
            return []
        return json.loads(registry_path.read_text(encoding="utf-8"))

    def _read_source_metadata(self) -> list[dict[str, Any]]:
        if not self.settings.documents_dir.exists():
            return []

        metadata_items: list[dict[str, Any]] = []
        for metadata_path in sorted(self.settings.documents_dir.glob("*.metadata.json")):
            stem = metadata_path.name.removesuffix(".metadata.json")
            document_path = self.settings.documents_dir / f"{stem}.md"
            if not document_path.exists():
                document_path = self._resolve_source_path(stem)
            if document_path is None:
                continue

            metadata = load_sidecar_metadata(document_path)
            metadata_items.append(metadata.model_dump(exclude_none=True))
        return metadata_items

    def _resolve_source_path(self, stem: str) -> Path | None:
        for path in sorted(self.settings.documents_dir.glob(f"{stem}.*")):
            if path.name.endswith(".metadata.json"):
                continue
            return path
        return None
