import json
import shutil
from pathlib import Path
from typing import Any

from app.config import Settings
from app.rag.metadata import (
    REGISTRY_FILENAME,
    detail_from_metadata,
    load_sidecar_metadata,
    summary_from_metadata,
)
from app.rag.schemas import DocumentDetail, DocumentSummary


class RagIndexService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def build_and_persist(self, documents: list[Any]) -> None:
        self._configure_llama_index()

        from llama_index.core import StorageContext, VectorStoreIndex

        self.settings.index_dir.mkdir(parents=True, exist_ok=True)
        storage_context = StorageContext.from_defaults()
        index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
        index.storage_context.persist(persist_dir=str(self.settings.index_dir))
        self._write_registry(documents)

    def load(self):
        self._configure_llama_index()

        from llama_index.core import StorageContext, load_index_from_storage

        if not self.settings.index_dir.exists():
            raise FileNotFoundError("RAG index does not exist. Run POST /documents/ingest first.")

        storage_context = StorageContext.from_defaults(persist_dir=str(self.settings.index_dir))
        return load_index_from_storage(storage_context)

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

    def _configure_llama_index(self) -> None:
        from llama_index.core import Settings as LlamaSettings

        if self.settings.rag_llm_provider == "mock":
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

        if self.settings.rag_embedding_provider == "mock":
            from llama_index.core.embeddings.mock_embed_model import MockEmbedding

            LlamaSettings.embed_model = MockEmbedding(embed_dim=1536)
        elif self.settings.rag_embedding_provider == "openai":
            if not self.settings.openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY is required when RAG_EMBEDDING_PROVIDER=openai"
                )

            from llama_index.embeddings.openai import OpenAIEmbedding

            LlamaSettings.embed_model = OpenAIEmbedding(
                model=self.settings.openai_embedding_model,
                api_key=self.settings.openai_api_key,
            )
        elif self.settings.rag_embedding_provider == "huggingface":
            from llama_index.embeddings.huggingface import HuggingFaceEmbedding

            LlamaSettings.embed_model = HuggingFaceEmbedding(
                model_name=self.settings.huggingface_embedding_model,
            )
        else:
            raise ValueError(
                f"Unsupported RAG_EMBEDDING_PROVIDER: {self.settings.rag_embedding_provider}"
            )

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
