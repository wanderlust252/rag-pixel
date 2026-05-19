from pathlib import Path
from tempfile import TemporaryDirectory

from markitdown import MarkItDown


class MarkdownConversionService:
    conversion_method = "markitdown_v1"

    supported_suffixes = {
        ".bmp",
        ".csv",
        ".doc",
        ".docx",
        ".epub",
        ".gif",
        ".htm",
        ".html",
        ".jpeg",
        ".jpg",
        ".json",
        ".md",
        ".mp3",
        ".msg",
        ".pdf",
        ".png",
        ".ppt",
        ".pptx",
        ".tif",
        ".tiff",
        ".txt",
        ".wav",
        ".xls",
        ".xlsx",
        ".xml",
        ".zip",
    }

    def __init__(self) -> None:
        self._markitdown = MarkItDown(enable_plugins=False)

    def convert(self, *, filename: str, content: bytes, title: str | None = None) -> str:
        suffix = Path(filename).suffix.lower()
        if suffix == ".md":
            return self._decode_text(content)
        if suffix not in self.supported_suffixes:
            raise ValueError(f"Unsupported document type {suffix or '(none)'}")

        with TemporaryDirectory() as tmp_dir:
            source_path = Path(tmp_dir) / f"source{suffix}"
            source_path.write_bytes(content)
            try:
                result = self._markitdown.convert_local(str(source_path))
            except Exception as exc:
                raise ValueError(str(exc)) from exc

        return self._with_title(result.text_content, title=title)

    def _decode_text(self, content: bytes) -> str:
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Uploaded Markdown document must be valid UTF-8 text") from exc

        if not text.strip():
            raise ValueError("Uploaded document is empty")
        return text

    def _with_title(self, markdown: str, *, title: str | None = None) -> str:
        body = markdown.strip()
        if not body:
            raise ValueError("Uploaded document is empty")
        if not title:
            return body
        heading = f"# {title}"
        if body.startswith(heading):
            return body
        return f"{heading}\n\n{body}"
