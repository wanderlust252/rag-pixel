import json

from fastapi.testclient import TestClient

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
                    b"docx bytes",
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

    document_path = tmp_path / "documents" / "srs-metfone-salary-20260515.docx"
    metadata_path = tmp_path / "documents" / "srs-metfone-salary-20260515.metadata.json"
    assert document_path.read_bytes() == b"docx bytes"
    assert json.loads(metadata_path.read_text(encoding="utf-8")) == {
        "doc_id": "SRS-METFONE-SALARY-20260515",
        "doc_type": "srs",
        "title": "SRS Luong khoan Metfone",
        "business_flow": "salary_calculation",
        "room_id": "cambodia_market",
        "shelf_id": "metfone_salary_srs",
        "source_type": "docx",
    }


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
