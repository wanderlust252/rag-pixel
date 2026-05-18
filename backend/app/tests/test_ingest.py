from app.config import Settings
from app.rag.ingest import RagIngestService


def test_load_sample_documents() -> None:
    settings = Settings()
    documents = RagIngestService(settings).load_documents()

    assert len(documents) >= 6
    doc_ids = {document.metadata["doc_id"] for document in documents}
    assert "BL-2026-0001" in doc_ids
    assert "INC-2026-0001" in doc_ids
