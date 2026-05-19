import io
import json

from fastapi.testclient import TestClient
from docx import Document

import app.main as main
from app.config import Settings


def test_upload_document_endpoint_writes_document_and_metadata(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(documents_dir=tmp_path / "documents", index_dir=tmp_path / "index")

    try:
        client = TestClient(main.app)
        response = client.post(
            "/documents/upload",
            data={
                "doc_id": "SRS-METFONE-SALARY-20260515",
                "doc_type": "srs",
                "title": "SRS Luong khoan Metfone",
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

    raw_path = tmp_path / "documents" / "srs-metfone-salary-20260515.docx"
    canonical_path = tmp_path / "documents" / "srs-metfone-salary-20260515.md"
    metadata_path = tmp_path / "documents" / "srs-metfone-salary-20260515.metadata.json"
    assert raw_path.exists()
    assert canonical_path.read_text(encoding="utf-8").startswith("# SRS Luong khoan Metfone")

    sidecar = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert sidecar["doc_id"] == "SRS-METFONE-SALARY-20260515"
    assert sidecar["source_type"] == "docx"
    assert sidecar["source_format"] == "docx"
    assert sidecar["canonical_format"] == "md"
    assert sidecar["conversion_status"] == "success"
    assert sidecar["raw_path"] == str(raw_path)
    assert sidecar["converted_path"] == str(canonical_path)


def test_upload_document_endpoint_rejects_duplicate_doc_id(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(documents_dir=tmp_path / "documents", index_dir=tmp_path / "index")

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
            data=data,
            files={"file": ("duplicate.txt", b"first", "text/plain")},
        )
        second_response = client.post(
            "/documents/upload",
            data=data,
            files={"file": ("duplicate.txt", b"second", "text/plain")},
        )
    finally:
        main.settings = original_settings

    assert first_response.status_code == 200
    assert second_response.status_code == 409


def test_upload_document_endpoint_stops_on_conversion_error(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(documents_dir=tmp_path / "documents", index_dir=tmp_path / "index")

    try:
        client = TestClient(main.app)
        response = client.post(
            "/documents/upload",
            data={
                "doc_id": "BROKEN-DOCX",
                "doc_type": "srs",
                "title": "Broken Docx",
                "reindex": "false",
            },
            files={
                "file": (
                    "broken.docx",
                    b"not a real docx",
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            },
        )
    finally:
        main.settings = original_settings

    assert response.status_code == 400
    metadata_path = tmp_path / "documents" / "broken-docx.metadata.json"
    sidecar = json.loads(metadata_path.read_text(encoding="utf-8"))
    assert sidecar["conversion_status"] == "failed"
    assert "zip file" in sidecar["conversion_error"]
    assert not (tmp_path / "documents" / "broken-docx.md").exists()


def test_document_endpoints_read_uploaded_metadata_without_reindex(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(documents_dir=tmp_path / "documents", index_dir=tmp_path / "index")

    try:
        client = TestClient(main.app)
        upload_response = client.post(
            "/documents/upload",
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
    main.settings = Settings(documents_dir=tmp_path / "documents", index_dir=tmp_path / "index")

    try:
        client = TestClient(main.app)
        upload_response = client.post(
            "/documents/upload",
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
        clear_response = client.delete("/documents")
    finally:
        main.settings = original_settings

    assert upload_response.status_code == 200
    assert clear_response.status_code == 200
    assert clear_response.json() == {
        "documents_removed": 1,
        "metadata_removed": 1,
        "index_cleared": False,
    }


def _docx_bytes(paragraphs: list[str]) -> bytes:
    document = Document()
    for paragraph in paragraphs:
        document.add_paragraph(paragraph)

    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()
