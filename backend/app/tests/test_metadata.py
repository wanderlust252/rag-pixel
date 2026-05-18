from pathlib import Path

from app.rag.metadata import load_sidecar_metadata, ui_block_from_metadata


def test_load_sidecar_metadata() -> None:
    metadata = load_sidecar_metadata(
        Path("app/storage/documents/bill_of_lading_sample.md")
    )

    assert metadata.doc_id == "BL-2026-0001"
    assert metadata.doc_type == "bill_of_lading"
    assert metadata.shipment_id == "SHP-001"


def test_ui_block_from_metadata() -> None:
    block = ui_block_from_metadata(
        {
            "doc_id": "INC-2026-0001",
            "doc_type": "incident_report",
            "title": "Incident Report INC-2026-0001",
            "shipment_id": "SHP-001",
        }
    )

    assert block.block_id == "INC-2026-0001"
    assert block.block_type == "bookshelf"
    assert block.category == "shipment_exceptions"
