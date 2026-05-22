import io
import json
import sys
from types import ModuleType, SimpleNamespace

from fastapi.testclient import TestClient
from docx import Document

import app.main as main
from app.config import Settings


AUTH_API_KEY = "test-write-key"
AUTH_HEADERS = {"Authorization": f"Bearer {AUTH_API_KEY}"}


def test_upload_document_endpoint_requires_api_key(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
    )

    try:
        client = TestClient(main.app)
        missing_response = client.post(
            "/documents/upload",
            data={
                "doc_id": "NO-AUTH",
                "doc_type": "srs",
                "title": "No Auth",
                "reindex": "false",
            },
            files={"file": ("no-auth.txt", b"content", "text/plain")},
        )
        wrong_response = client.post(
            "/documents/upload",
            headers={"Authorization": "Bearer wrong-key"},
            data={
                "doc_id": "WRONG-AUTH",
                "doc_type": "srs",
                "title": "Wrong Auth",
                "reindex": "false",
            },
            files={"file": ("wrong-auth.txt", b"content", "text/plain")},
        )
    finally:
        main.settings = original_settings

    assert missing_response.status_code == 401
    assert wrong_response.status_code == 403


def test_upload_document_endpoint_writes_document_and_metadata(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
    )

    try:
        client = TestClient(main.app)
        response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data={
                "doc_id": "SRS-METFONE-SALARY-20260515",
                "doc_type": "srs",
                "title": "SRS Luong khoan Metfone",
                "tenant_id": "metfone-cambodia",
                "market": "cambodia",
                "country": "KH",
                "domain": "logistics",
                "module": "payroll",
                "business_flow": "salary_calculation",
                "room_id": "cambodia_market",
                "shelf_id": "metfone_salary_srs",
                "source_type": "docx",
                "reindex": "false",
            },
            files={
                "file": (
                    "original filename.docx",
                    _docx_bytes(["Luong khoan Metfone", "Su kien tinh luong giao nhan hang"]),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )
    finally:
        main.settings = original_settings

    assert response.status_code == 200
    body = response.json()
    assert body["document"]["doc_id"] == "SRS-METFONE-SALARY-20260515"
    assert body["index_persisted"] is False
    assert body["ingested_documents"] is None
    assert body["document"]["conversion_status"] == "success"
    assert body["document"]["canonical_format"] == "md"
    assert body["document"]["tenant_id"] == "metfone-cambodia"
    assert body["document"]["market"] == "cambodia"
    assert body["document"]["country"] == "KH"
    assert body["document"]["domain"] == "logistics"
    assert body["document"]["module"] == "payroll"

    raw_path = tmp_path / "documents" / "srs-metfone-salary-20260515.docx"
    canonical_path = tmp_path / "documents" / "srs-metfone-salary-20260515.md"
    metadata_path = tmp_path / "documents" / "srs-metfone-salary-20260515.metadata.json"
    assert raw_path.exists()
    assert canonical_path.read_text(encoding="utf-8").startswith("# SRS Luong khoan Metfone")

    sidecar = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert sidecar["doc_id"] == "SRS-METFONE-SALARY-20260515"
    assert sidecar["tenant_id"] == "metfone-cambodia"
    assert sidecar["market"] == "cambodia"
    assert sidecar["country"] == "KH"
    assert sidecar["domain"] == "logistics"
    assert sidecar["module"] == "payroll"
    assert sidecar["source_type"] == "docx"
    assert sidecar["source_format"] == "docx"
    assert sidecar["canonical_format"] == "md"
    assert sidecar["conversion_status"] == "success"
    assert sidecar["raw_path"] == str(raw_path)
    assert sidecar["converted_path"] == str(canonical_path)


def test_upload_document_endpoint_rejects_duplicate_doc_id(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
    )

    try:
        client = TestClient(main.app)
        data = {
            "doc_id": "DUPLICATE",
            "doc_type": "srs",
            "title": "Duplicate",
            "reindex": "false",
        }
        first_response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data=data,
            files={"file": ("duplicate.txt", b"first", "text/plain")},
        )
        second_response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data=data,
            files={"file": ("duplicate.txt", b"second", "text/plain")},
        )
    finally:
        main.settings = original_settings

    assert first_response.status_code == 200
    assert second_response.status_code == 409


def test_upload_document_endpoint_stops_on_conversion_error(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
    )

    try:
        client = TestClient(main.app)
        response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data={
                "doc_id": "BROKEN-JSON",
                "doc_type": "srs",
                "title": "Broken Json",
                "reindex": "false",
            },
            files={
                "file": (
                    "broken.json",
                    b"\xff\xfe\x00",
                    "application/json",
                )
            },
        )
    finally:
        main.settings = original_settings

    assert response.status_code == 400
    metadata_path = tmp_path / "documents" / "broken-json.metadata.json"
    sidecar = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert sidecar["conversion_status"] == "failed"
    assert sidecar["conversion_error"]
    assert not (tmp_path / "documents" / "broken-json.md").exists()


def test_upload_pdf_document_endpoint_writes_markdown_canonical(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
    )

    try:
        client = TestClient(main.app)
        response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data={
                "doc_id": "PDF-HISTORY",
                "doc_type": "history_textbook",
                "title": "PDF History",
                "source_type": "pdf",
                "reindex": "false",
            },
            files={
                "file": (
                    "history.pdf",
                    _pdf_bytes("Party history source"),
                    "application/pdf",
                )
            },
        )
    finally:
        main.settings = original_settings

    assert response.status_code == 200
    body = response.json()
    assert body["document"]["source_format"] == "pdf"
    assert body["document"]["canonical_format"] == "md"
    assert body["document"]["conversion_method"] == "markitdown_v1"

    canonical_path = tmp_path / "documents" / "pdf-history.md"
    assert canonical_path.exists()
    assert "PDF History" in canonical_path.read_text(encoding="utf-8")


def test_upload_document_uses_llamaparse_when_configured(tmp_path, monkeypatch) -> None:
    _install_fake_llama_cloud(
        monkeypatch,
        parse_result=SimpleNamespace(
            markdown=SimpleNamespace(
                pages=[
                    SimpleNamespace(markdown="Parsed page one"),
                    SimpleNamespace(markdown="Parsed page two"),
                ]
            )
        ),
    )
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
        rag_parse_provider="llamaparse_fallback",
        llama_cloud_api_key="test-llama-key",
    )

    try:
        client = TestClient(main.app)
        response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data={
                "doc_id": "LLAMAPARSE-SUCCESS",
                "doc_type": "srs",
                "title": "LlamaParse Success",
                "reindex": "false",
            },
            files={"file": ("source.txt", b"original local text", "text/plain")},
        )
    finally:
        main.settings = original_settings

    assert response.status_code == 200
    body = response.json()
    assert body["document"]["conversion_method"] == "llamaparse_cost_effective"

    canonical_path = tmp_path / "documents" / "llamaparse-success.md"
    assert canonical_path.read_text(encoding="utf-8") == (
        "# LlamaParse Success\n\nParsed page one\n\n---\n\nParsed page two"
    )


def test_upload_document_falls_back_to_markitdown_when_llamaparse_fails(
    tmp_path,
    monkeypatch,
) -> None:
    _install_fake_llama_cloud(monkeypatch, parse_error=RuntimeError("quota exhausted"))
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
        rag_parse_provider="llamaparse_fallback",
        llama_cloud_api_key="test-llama-key",
    )

    try:
        client = TestClient(main.app)
        response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data={
                "doc_id": "LLAMAPARSE-FALLBACK",
                "doc_type": "srs",
                "title": "LlamaParse Fallback",
                "reindex": "false",
            },
            files={"file": ("source.txt", b"fallback local text", "text/plain")},
        )
    finally:
        main.settings = original_settings

    assert response.status_code == 200
    body = response.json()
    assert (
        body["document"]["conversion_method"]
        == "llamaparse_cost_effective_fallback_markitdown_v1"
    )
    canonical_path = tmp_path / "documents" / "llamaparse-fallback.md"
    assert "fallback local text" in canonical_path.read_text(encoding="utf-8")


def test_upload_document_fails_when_llamaparse_and_markitdown_fail(
    tmp_path,
    monkeypatch,
) -> None:
    _install_fake_llama_cloud(monkeypatch, parse_error=RuntimeError("quota exhausted"))
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
        rag_parse_provider="llamaparse_fallback",
        llama_cloud_api_key="test-llama-key",
    )

    try:
        client = TestClient(main.app)
        response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data={
                "doc_id": "LLAMAPARSE-BOTH-FAIL",
                "doc_type": "srs",
                "title": "LlamaParse Both Fail",
                "reindex": "false",
            },
            files={"file": ("broken.json", b"\xff\xfe\x00", "application/json")},
        )
    finally:
        main.settings = original_settings

    assert response.status_code == 400
    metadata_path = tmp_path / "documents" / "llamaparse-both-fail.metadata.json"
    sidecar = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert sidecar["conversion_status"] == "failed"
    assert (
        sidecar["conversion_method"]
        == "llamaparse_cost_effective_fallback_markitdown_v1"
    )
    assert not (tmp_path / "documents" / "llamaparse-both-fail.md").exists()


def test_fast_llamaparse_tier_requests_text_expansion_only(tmp_path, monkeypatch) -> None:
    _install_fake_llama_cloud(
        monkeypatch,
        expected_tier="fast",
        expected_expand=["text"],
        parse_result=SimpleNamespace(
            text=SimpleNamespace(
                pages=[
                    SimpleNamespace(text="Fast page one"),
                    SimpleNamespace(text="Fast page two"),
                ]
            )
        ),
    )
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
        rag_parse_provider="llamaparse_fallback",
        llama_cloud_api_key="test-llama-key",
        llamaparse_tier="fast",
    )

    try:
        client = TestClient(main.app)
        response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data={
                "doc_id": "LLAMAPARSE-FAST",
                "doc_type": "srs",
                "title": "LlamaParse Fast",
                "reindex": "false",
            },
            files={"file": ("source.txt", b"original local text", "text/plain")},
        )
    finally:
        main.settings = original_settings

    assert response.status_code == 200
    body = response.json()
    assert body["document"]["conversion_method"] == "llamaparse_fast"
    canonical_path = tmp_path / "documents" / "llamaparse-fast.md"
    assert canonical_path.read_text(encoding="utf-8") == (
        "# LlamaParse Fast\n\nFast page one\n\n---\n\nFast page two"
    )


def test_document_endpoints_read_uploaded_metadata_without_reindex(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
    )

    try:
        client = TestClient(main.app)
        upload_response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data={
                "doc_id": "SRS-METFONE-SALARY-20260515",
                "doc_type": "srs",
                "title": "SRS Luong khoan Metfone",
                "reindex": "false",
            },
            files={
                "file": (
                    "original filename.docx",
                    _docx_bytes(["Luong khoan Metfone", "Su kien tinh luong giao nhan hang"]),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )
        list_response = client.get("/documents")
        detail_response = client.get("/documents/SRS-METFONE-SALARY-20260515")
    finally:
        main.settings = original_settings

    assert upload_response.status_code == 200
    assert list_response.status_code == 200
    assert detail_response.status_code == 200
    assert list_response.json()["documents"][0]["doc_id"] == "SRS-METFONE-SALARY-20260515"
    assert detail_response.json()["converted_path"].endswith("srs-metfone-salary-20260515.md")


def test_clear_documents_endpoint_counts_logical_documents(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
    )

    try:
        client = TestClient(main.app)
        upload_response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data={
                "doc_id": "SRS-METFONE-SALARY-20260515",
                "doc_type": "srs",
                "title": "SRS Luong khoan Metfone",
                "reindex": "false",
            },
            files={
                "file": (
                    "original filename.docx",
                    _docx_bytes(["Luong khoan Metfone", "Su kien tinh luong giao nhan hang"]),
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )
        clear_response = client.delete("/documents", headers=AUTH_HEADERS)
    finally:
        main.settings = original_settings

    assert upload_response.status_code == 200
    assert clear_response.status_code == 200
    assert clear_response.json() == {
        "documents_removed": 1,
        "metadata_removed": 1,
        "index_cleared": False,
    }


def test_clear_documents_endpoint_requires_api_key(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=AUTH_API_KEY,
    )

    try:
        client = TestClient(main.app)
        missing_response = client.delete("/documents")
        wrong_response = client.delete(
            "/documents",
            headers={"Authorization": "Bearer wrong-key"},
        )
    finally:
        main.settings = original_settings

    assert missing_response.status_code == 401
    assert wrong_response.status_code == 403


def test_protected_document_endpoints_fail_when_backend_api_key_is_not_configured(
    tmp_path,
) -> None:
    original_settings = main.settings
    main.settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_pixels_api_key=None,
    )

    try:
        client = TestClient(main.app)
        upload_response = client.post(
            "/documents/upload",
            headers=AUTH_HEADERS,
            data={
                "doc_id": "NO-BACKEND-KEY",
                "doc_type": "srs",
                "title": "No Backend Key",
                "reindex": "false",
            },
            files={"file": ("no-backend-key.txt", b"content", "text/plain")},
        )
        clear_response = client.delete("/documents", headers=AUTH_HEADERS)
    finally:
        main.settings = original_settings

    assert upload_response.status_code == 503
    assert clear_response.status_code == 503


def _docx_bytes(paragraphs: list[str]) -> bytes:
    document = Document()
    for paragraph in paragraphs:
        document.add_paragraph(paragraph)

    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def _pdf_bytes(text: str) -> bytes:
    stream = f"BT /F1 24 Tf 72 720 Td ({text}) Tj ET".encode("latin-1")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    chunks = [b"%PDF-1.4\n"]
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(sum(len(chunk) for chunk in chunks))
        chunks.append(f"{index} 0 obj\n".encode("ascii") + obj + b"\nendobj\n")
    xref_offset = sum(len(chunk) for chunk in chunks)
    chunks.append(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    chunks.append(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        chunks.append(f"{offset:010d} 00000 n \n".encode("ascii"))
    chunks.append(
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return b"".join(chunks)


def _install_fake_llama_cloud(
    monkeypatch,
    *,
    parse_result: object | None = None,
    parse_error: Exception | None = None,
    expected_tier: str = "cost_effective",
    expected_expand: list[str] | None = None,
) -> None:
    module = ModuleType("llama_cloud")

    class FakeFiles:
        def create(self, *, file: str, purpose: str):
            assert file
            assert purpose == "parse"
            return SimpleNamespace(id="fake-file-id")

    class FakeParsing:
        def parse(self, *, file_id: str, tier: str, version: str, expand: list[str], timeout: int):
            assert file_id == "fake-file-id"
            assert tier == expected_tier
            assert version == "latest"
            assert expand == (expected_expand or ["markdown", "text"])
            assert timeout == 120
            if parse_error is not None:
                raise parse_error
            return parse_result

    class FakeLlamaCloud:
        def __init__(self, *, api_key: str | None = None, timeout: int):
            assert api_key == "test-llama-key"
            assert timeout == 120
            self.files = FakeFiles()
            self.parsing = FakeParsing()

    module.LlamaCloud = FakeLlamaCloud
    monkeypatch.setitem(sys.modules, "llama_cloud", module)
