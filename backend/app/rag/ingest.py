import json
import re
from datetime import UTC, datetime
from pathlib import Path

from app.config import Settings
from app.rag.convert import MarkdownConversionService
from app.rag.metadata import load_sidecar_metadata, metadata_to_llama
from app.rag.schemas import DocumentDetail, DocumentMetadata


class RagIngestService:
    supported_suffixes = MarkdownConversionService.supported_suffixes
    canonical_suffix = ".md"

    def __init__(self, settings: Settings):
        self.settings = settings
        self.converter = MarkdownConversionService(settings)

    def load_documents(self):
        from llama_index.core import Document

        document_dir = self.settings.documents_dir
        if not document_dir.exists():
            raise FileNotFoundError(f"Document directory does not exist: {document_dir}")

        documents = []
        for metadata_path in sorted(document_dir.glob("*.metadata.json")):
            path = self._ensure_canonical_document(metadata_path)
            if path is None:
                continue

            metadata = load_sidecar_metadata(path)
            text = self._read_document_text(path)
            documents.append(
                Document(
                    doc_id=metadata.doc_id,
                    text=text,
                    metadata=metadata_to_llama(metadata),
                    excluded_llm_metadata_keys=["source_path"],
                    excluded_embed_metadata_keys=["source_path"],
                )
            )

        if not documents:
            raise ValueError(f"No supported documents found in {document_dir}")

        return documents

    def clear_source_documents(self) -> tuple[int, int]:
        document_dir = self.settings.documents_dir
        if not document_dir.exists():
            return 0, 0

        documents_removed = 0
        metadata_removed = 0
        handled_paths: set[Path] = set()

        for metadata_path in sorted(document_dir.glob("*.metadata.json")):
            stem = metadata_path.name.removesuffix(".metadata.json")
            removed_any = False
            for path in sorted(document_dir.glob(f"{stem}.*")):
                if not path.is_file() or path == metadata_path:
                    continue
                if path.suffix.lower() in self.supported_suffixes:
                    path.unlink()
                    handled_paths.add(path)
                    removed_any = True

            metadata_path.unlink()
            handled_paths.add(metadata_path)
            metadata_removed += 1
            if removed_any:
                documents_removed += 1

        for path in document_dir.iterdir():
            if not path.is_file() or path in handled_paths:
                continue
            if path.name.endswith(".metadata.json"):
                path.unlink()
                metadata_removed += 1
            elif path.suffix.lower() in self.supported_suffixes:
                path.unlink()
                documents_removed += 1

        return documents_removed, metadata_removed

    def save_uploaded_document(
        self,
        *,
        filename: str,
        content: bytes,
        metadata: dict,
        overwrite: bool = False,
    ) -> DocumentDetail:
        suffix = Path(filename).suffix.lower()
        if suffix not in self.supported_suffixes:
            supported = ", ".join(sorted(self.supported_suffixes))
            raise ValueError(f"Unsupported document type {suffix}. Supported suffixes: {supported}")
        if not content:
            raise ValueError("Uploaded document is empty")

        metadata_model = DocumentMetadata.model_validate(
            {**metadata, "source_path": "__pending__"}
        )
        stem = self._safe_document_stem(metadata_model.doc_id)
        raw_path = self.settings.documents_dir / f"{stem}{suffix}"
        canonical_path = self.settings.documents_dir / f"{stem}{self.canonical_suffix}"
        metadata_path = self.settings.documents_dir / f"{stem}.metadata.json"

        existing_paths = self._existing_document_paths(stem)
        if not overwrite and existing_paths:
            raise FileExistsError(f"Document already exists for doc_id: {metadata_model.doc_id}")

        self.settings.documents_dir.mkdir(parents=True, exist_ok=True)
        if overwrite:
            self._remove_existing_document_paths(stem, keep_paths={metadata_path})

        raw_path.write_bytes(content)

        sidecar = metadata_model.model_dump(exclude_none=True, exclude={"source_path"})
        sidecar.update(
            {
                "source_type": sidecar.get("source_type") or suffix.lstrip("."),
                "source_format": suffix.lstrip("."),
                "canonical_format": "md",
                "raw_path": str(raw_path),
                "converted_path": str(canonical_path),
                "conversion_status": "pending",
                "conversion_error": None,
                "conversion_method": self.converter.conversion_method,
                "updated_at": self._utc_now(),
            }
        )
        self._write_sidecar(metadata_path, sidecar)

        try:
            conversion = self.converter.convert(
                filename=filename,
                content=content,
                title=metadata_model.title,
            )
        except ValueError as exc:
            sidecar["conversion_status"] = "failed"
            sidecar["conversion_error"] = str(exc)
            sidecar["updated_at"] = self._utc_now()
            self._write_sidecar(metadata_path, sidecar)
            raise

        canonical_path.write_text(conversion.markdown, encoding="utf-8")
        sidecar["conversion_status"] = "success"
        sidecar["conversion_error"] = None
        sidecar["conversion_method"] = conversion.method
        sidecar["updated_at"] = self._utc_now()
        self._write_sidecar(metadata_path, sidecar)

        return DocumentDetail.model_validate(load_sidecar_metadata(canonical_path).model_dump())

    def _read_document_text(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")

    def _safe_document_stem(self, doc_id: str) -> str:
        stem = re.sub(r"[^A-Za-z0-9_.-]+", "_", doc_id).strip("._-")
        if not stem:
            raise ValueError("doc_id must contain at least one filename-safe character")
        return stem.lower()

    def _ensure_canonical_document(self, metadata_path: Path) -> Path | None:
        stem = metadata_path.name.removesuffix(".metadata.json")
        canonical_path = metadata_path.with_name(f"{stem}{self.canonical_suffix}")
        if canonical_path.exists():
            return canonical_path

        raw_path = self._resolve_raw_document_path(metadata_path, stem)
        if raw_path is None:
            return None

        metadata = load_sidecar_metadata(raw_path)
        conversion = self.converter.convert(
            filename=raw_path.name,
            content=raw_path.read_bytes(),
            title=metadata.title,
        )
        canonical_path.write_text(conversion.markdown, encoding="utf-8")

        sidecar = metadata.model_dump(exclude_none=True, exclude={"source_path"})
        sidecar.update(
            {
                "source_format": raw_path.suffix.lstrip("."),
                "canonical_format": "md",
                "raw_path": sidecar.get("raw_path") or str(raw_path),
                "converted_path": str(canonical_path),
                "conversion_status": "success",
                "conversion_error": None,
                "conversion_method": conversion.method,
                "updated_at": self._utc_now(),
            }
        )
        self._write_sidecar(metadata_path, sidecar)
        return canonical_path

    def _resolve_raw_document_path(self, metadata_path: Path, stem: str) -> Path | None:
        raw = json.loads(metadata_path.read_text(encoding="utf-8"))
        raw_path = raw.get("raw_path")
        if raw_path:
            path = Path(raw_path)
            if path.exists():
                return path

        for path in sorted(metadata_path.parent.glob(f"{stem}.*")):
            if path.name.endswith(".metadata.json") or path.suffix.lower() == self.canonical_suffix:
                continue
            if path.suffix.lower() in self.supported_suffixes:
                return path
        return None

    def _existing_document_paths(self, stem: str) -> list[Path]:
        return [
            path
            for path in self.settings.documents_dir.glob(f"{stem}.*")
            if path.is_file()
        ]

    def _remove_existing_document_paths(self, stem: str, *, keep_paths: set[Path]) -> None:
        for path in self._existing_document_paths(stem):
            if path in keep_paths:
                continue
            path.unlink()

    def _write_sidecar(self, metadata_path: Path, sidecar: dict) -> None:
        metadata_path.write_text(
            json.dumps(sidecar, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def _utc_now(self) -> str:
        return datetime.now(UTC).isoformat()
