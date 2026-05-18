from pathlib import Path

from app.config import Settings
from app.rag.metadata import load_sidecar_metadata, metadata_to_llama


class RagIngestService:
    supported_suffixes = {".md", ".txt", ".csv"}

    def __init__(self, settings: Settings):
        self.settings = settings

    def load_documents(self):
        from llama_index.core import Document

        document_dir = self.settings.documents_dir
        if not document_dir.exists():
            raise FileNotFoundError(f"Document directory does not exist: {document_dir}")

        documents = []
        for path in sorted(document_dir.iterdir()):
            if not self._is_supported_document(path):
                continue

            metadata = load_sidecar_metadata(path)
            text = path.read_text(encoding="utf-8")
            documents.append(
                Document(
                    text=text,
                    metadata=metadata_to_llama(metadata),
                    excluded_llm_metadata_keys=["source_path"],
                    excluded_embed_metadata_keys=["source_path"],
                )
            )

        if not documents:
            raise ValueError(f"No supported documents found in {document_dir}")

        return documents

    def _is_supported_document(self, path: Path) -> bool:
        if not path.is_file():
            return False
        if path.name.endswith(".metadata.json"):
            return False
        return path.suffix.lower() in self.supported_suffixes
