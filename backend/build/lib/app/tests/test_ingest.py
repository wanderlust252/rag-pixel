import json

from docx import Document

from app.config import Settings
from app.rag.ingest import RagIngestService


def test_load_sample_documents(tmp_path) -> None:
    (tmp_path / "bill_of_lading_sample.md").write_text("Bill of lading", encoding="utf-8")
    (tmp_path / "bill_of_lading_sample.metadata.json").write_text(
        json.dumps(
            {
                "doc_id": "BL-2026-0001",
                "doc_type": "bill_of_lading",
                "title": "Bill of Lading BL-2026-0001",
            }
        ),
        encoding="utf-8",
    )
    (tmp_path / "incident_report.md").write_text("Incident report", encoding="utf-8")
    (tmp_path / "incident_report.metadata.json").write_text(
        json.dumps(
            {
                "doc_id": "INC-2026-0001",
                "doc_type": "incident_report",
                "title": "Incident Report INC-2026-0001",
            }
        ),
        encoding="utf-8",
    )

    settings = Settings(documents_dir=tmp_path, index_dir=tmp_path / "index")
    documents = RagIngestService(settings).load_documents()

    assert len(documents) == 2
    doc_ids = {document.metadata["doc_id"] for document in documents}
    assert "BL-2026-0001" in doc_ids
    assert "INC-2026-0001" in doc_ids


def test_load_docx_document(tmp_path) -> None:
    document_path = tmp_path / "salary_srs.docx"
    metadata_path = tmp_path / "salary_srs.metadata.json"
    _write_docx(document_path, ["Luong khoan Metfone", "Su kien tinh luong giao nhan hang"])
    metadata_path.write_text(
        json.dumps(
            {
                "doc_id": "SRS-METFONE-SALARY-20260515",
                "doc_type": "srs",
                "title": "SRS Luong khoan Metfone",
                "business_flow": "salary_calculation",
                "room_id": "cambodia_market",
                "shelf_id": "metfone_salary_srs",
                "source_type": "docx",
            }
        ),
        encoding="utf-8",
    )

    settings = Settings(documents_dir=tmp_path, index_dir=tmp_path / "index")
    documents = RagIngestService(settings).load_documents()

    assert len(documents) == 1
    assert documents[0].doc_id == "SRS-METFONE-SALARY-20260515"
    assert documents[0].metadata["doc_id"] == "SRS-METFONE-SALARY-20260515"
    assert documents[0].metadata["conversion_status"] == "success"
    assert documents[0].metadata["canonical_format"] == "md"
    assert "# SRS Luong khoan Metfone" in documents[0].text


def test_clear_source_documents_removes_supported_files_and_metadata(tmp_path) -> None:
    (tmp_path / "document.md").write_text("content", encoding="utf-8")
    (tmp_path / "document.metadata.json").write_text("{}", encoding="utf-8")
    (tmp_path / "notes.pdf").write_text("keep me", encoding="utf-8")

    settings = Settings(documents_dir=tmp_path, index_dir=tmp_path / "index")
    documents_removed, metadata_removed = RagIngestService(settings).clear_source_documents()

    assert documents_removed == 1
    assert metadata_removed == 1
    assert not (tmp_path / "document.md").exists()
    assert not (tmp_path / "document.metadata.json").exists()
    assert (tmp_path / "notes.pdf").exists()


def _write_docx(path, paragraphs: list[str]) -> None:
    document = Document()
    for paragraph in paragraphs:
        document.add_paragraph(paragraph)
    document.save(path)
