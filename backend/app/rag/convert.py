import csv
import io
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from tempfile import TemporaryDirectory

from docx2md import do_convert

class MarkdownConversionService:
    conversion_method = "docx2md_v1"

    def convert(self, *, filename: str, content: bytes, title: str | None = None) -> str:
        suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if suffix == "md":
            return self._decode_text(content)
        if suffix == "txt":
            return self._as_markdown_body(self._decode_text(content), title=title)
        if suffix == "csv":
            return self._csv_to_markdown(content, title=title)
        if suffix == "docx":
            return self._as_markdown_body(self._read_docx_text(content), title=title)

        raise ValueError(f"Unsupported document type .{suffix}")

    def _decode_text(self, content: bytes) -> str:
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("Uploaded document must be valid UTF-8 text") from exc

    def _csv_to_markdown(self, content: bytes, *, title: str | None = None) -> str:
        decoded = self._decode_text(content)
        rows = list(csv.reader(io.StringIO(decoded)))
        if not rows:
            raise ValueError("Uploaded CSV document is empty")

        width = max(len(row) for row in rows)
        normalized_rows = [row + [""] * (width - len(row)) for row in rows]
        header = normalized_rows[0]
        separator = ["---"] * width
        table_rows = [header, separator, *normalized_rows[1:]]
        table = "\n".join(f"| {' | '.join(row)} |" for row in table_rows)
        return self._as_markdown_body(table, title=title)

    def _read_docx_text(self, content: bytes) -> str:
        with TemporaryDirectory() as tmp_dir:
            docx_path = Path(tmp_dir) / "source.docx"
            docx_path.write_bytes(content)
            with io.StringIO() as captured_stdout, io.StringIO() as captured_stderr:
                with redirect_stdout(captured_stdout), redirect_stderr(captured_stderr):
                    markdown = do_convert(str(docx_path), use_md_table=True)

        if markdown.startswith("Exception:"):
            raise ValueError(markdown.removeprefix("Exception:").strip())

        if not markdown.strip():
            raise ValueError("Uploaded DOCX document is empty")

        return markdown

    def _as_markdown_body(self, text: str, *, title: str | None = None) -> str:
        body = text.strip()
        if not body:
            raise ValueError("Uploaded document is empty")
        if not title:
            return body
        return f"# {title}\n\n{body}"