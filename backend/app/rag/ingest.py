from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from app.config import Settings
from app.rag.metadata import load_sidecar_metadata, metadata_to_llama


class RagIngestService:
    supported_suffixes = {".md", ".txt", ".csv", ".docx"}

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
            text = self._read_document_text(path)
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

    def clear_source_documents(self) -> tuple[int, int]:
        document_dir = self.settings.documents_dir
        if not document_dir.exists():
            return 0, 0

        documents_removed = 0
        metadata_removed = 0
        for path in document_dir.iterdir():
            if not path.is_file():
                continue
            if path.name.endswith(".metadata.json"):
                path.unlink()
                metadata_removed += 1
            elif path.suffix.lower() in self.supported_suffixes:
                path.unlink()
                documents_removed += 1

        return documents_removed, metadata_removed

    def _read_document_text(self, path: Path) -> str:
        if path.suffix.lower() == ".docx":
            return self._read_docx_text(path)
        return path.read_text(encoding="utf-8")

    def _read_docx_text(self, path: Path) -> str:
        try:
            with ZipFile(path) as docx:
                document_xml = docx.read("word/document.xml")
        except (BadZipFile, KeyError) as exc:
            raise ValueError(f"Unsupported or invalid DOCX file: {path}") from exc

        root = ElementTree.fromstring(document_xml)
        namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paragraphs = []
        for paragraph in root.findall(".//w:p", namespace):
            text_parts = [
                node.text
                for node in paragraph.findall(".//w:t", namespace)
                if node.text is not None
            ]
            if text_parts:
                paragraphs.append("".join(text_parts))

        return "\n".join(paragraphs)
