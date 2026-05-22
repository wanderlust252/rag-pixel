from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

from app.config import Settings
from markitdown import MarkItDown


@dataclass(frozen=True)
class ConversionResult:
    markdown: str
    method: str


class MarkdownConversionService:
    markitdown_method = "markitdown_v1"

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

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings
        self._markitdown = MarkItDown(enable_plugins=False)

    @property
    def conversion_method(self) -> str:
        if self._should_try_llamaparse():
            return f"llamaparse_{self.settings.llamaparse_tier}_fallback_{self.markitdown_method}"
        return self.markitdown_method

    def convert(self, *, filename: str, content: bytes, title: str | None = None) -> ConversionResult:
        suffix = Path(filename).suffix.lower()
        if suffix not in self.supported_suffixes:
            raise ValueError(f"Unsupported document type {suffix or '(none)'}")

        tried_llamaparse = False
        if self._should_try_llamaparse():
            try:
                tried_llamaparse = True
                return self._convert_with_llamaparse(
                    filename=filename,
                    content=content,
                    title=title,
                )
            except Exception as e:
                import traceback
                print(f"LlamaParse conversion failed for {filename}: {e}")
                traceback.print_exc()

        if suffix == ".md":
            return ConversionResult(
                markdown=self._decode_text(content),
                method=self.conversion_method if tried_llamaparse else self.markitdown_method,
            )

        return ConversionResult(
            markdown=self._convert_with_markitdown(filename=filename, content=content, title=title),
            method=self.conversion_method if tried_llamaparse else self.markitdown_method,
        )

    def _convert_with_markitdown(
        self,
        *,
        filename: str,
        content: bytes,
        title: str | None = None,
    ) -> str:
        suffix = Path(filename).suffix.lower()

        with TemporaryDirectory() as tmp_dir:
            source_path = Path(tmp_dir) / f"source{suffix}"
            source_path.write_bytes(content)
            try:
                result = self._markitdown.convert_local(str(source_path))
            except Exception as exc:
                raise ValueError(str(exc)) from exc

        return self._with_title(result.text_content, title=title)

    def _convert_with_llamaparse(
        self,
        *,
        filename: str,
        content: bytes,
        title: str | None = None,
    ) -> ConversionResult:
        assert self.settings is not None
        method = f"llamaparse_{self.settings.llamaparse_tier}"

        from llama_cloud import LlamaCloud

        suffix = Path(filename).suffix.lower()
        with TemporaryDirectory() as tmp_dir:
            source_path = Path(tmp_dir) / f"source{suffix}"
            source_path.write_bytes(content)
            client = LlamaCloud(
                api_key=self.settings.llama_cloud_api_key,
                timeout=self.settings.llamaparse_timeout_seconds,
            )
            file = client.files.create(file=str(source_path), purpose="parse")
            result = client.parsing.parse(
                file_id=file.id,
                tier=self.settings.llamaparse_tier,
                version=self.settings.llamaparse_version,
                expand=self._llamaparse_expansions(),
                timeout=self.settings.llamaparse_timeout_seconds,
            )
        markdown = self._extract_llamaparse_markdown(result)

        markdown = self._with_title(markdown, title=title)
        return ConversionResult(markdown=markdown, method=method)

    def _extract_llamaparse_markdown(self, result: object) -> str:
        markdown_result = getattr(result, "markdown", None)
        if markdown_result is None:
            text = self._extract_llamaparse_text(result)
            if text:
                return text
            raise ValueError("LlamaParse returned no markdown")

        direct_markdown = getattr(markdown_result, "markdown", None)
        if isinstance(direct_markdown, str) and direct_markdown.strip():
            return direct_markdown

        pages = getattr(markdown_result, "pages", None)
        if pages:
            page_markdown = [
                getattr(page, "markdown", "")
                for page in pages
                if isinstance(getattr(page, "markdown", ""), str)
                and getattr(page, "markdown", "").strip()
            ]
            if page_markdown:
                return "\n\n---\n\n".join(page_markdown)

        if isinstance(markdown_result, str) and markdown_result.strip():
            return markdown_result

        raise ValueError("LlamaParse returned empty markdown")

    def _extract_llamaparse_text(self, result: object) -> str | None:
        text_result = getattr(result, "text", None)
        if isinstance(text_result, str) and text_result.strip():
            return text_result

        pages = getattr(text_result, "pages", None)
        if pages:
            page_text = [
                getattr(page, "text", "")
                for page in pages
                if isinstance(getattr(page, "text", ""), str)
                and getattr(page, "text", "").strip()
            ]
            if page_text:
                return "\n\n---\n\n".join(page_text)

        text_full = getattr(result, "text_full", None)
        if isinstance(text_full, str) and text_full.strip():
            return text_full

        return None

    def _should_try_llamaparse(self) -> bool:
        if self.settings is None:
            return False
        return (
            self.settings.rag_parse_provider == "llamaparse_fallback"
            and bool(self.settings.llama_cloud_api_key)
        )

    def _llamaparse_expansions(self) -> list[str]:
        assert self.settings is not None
        if self.settings.llamaparse_tier == "fast":
            return ["text"]
        return ["markdown", "text"]

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
