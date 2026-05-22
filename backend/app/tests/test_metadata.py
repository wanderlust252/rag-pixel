import json

from app.rag.metadata import load_sidecar_metadata, ui_block_from_metadata


def test_load_sidecar_metadata(tmp_path) -> None:
    document_path = tmp_path / "bill_of_lading_sample.md"
    document_path.write_text("Bill of lading", encoding="utf-8")
    document_path.with_suffix(".metadata.json").write_text(
        json.dumps(
            {
                "doc_id": "BL-2026-0001",
                "doc_type": "bill_of_lading",
                "title": "Bill of Lading BL-2026-0001",
                "tenant_id": "unitel-laos",
                "market": "laos",
                "domain": "logistics",
                "module": "shipment_ops",
                "shipment_id": "SHP-001",
            }
        ),
        encoding="utf-8",
    )

    metadata = load_sidecar_metadata(document_path)

    assert metadata.doc_id == "BL-2026-0001"
    assert metadata.doc_type == "bill_of_lading"
    assert metadata.tenant_id == "unitel-laos"
    assert metadata.market == "laos"
    assert metadata.domain == "logistics"
    assert metadata.module == "shipment_ops"
    assert metadata.shipment_id == "SHP-001"


def test_ui_block_from_metadata() -> None:
    block = ui_block_from_metadata(
        {
            "doc_id": "INC-2026-0001",
            "doc_type": "incident_report",
            "title": "Incident Report INC-2026-0001",
            "tenant_id": "unitel-laos",
            "market": "laos",
            "domain": "logistics",
            "module": "shipment_exceptions",
            "shipment_id": "SHP-001",
        }
    )

    assert block.block_id == "INC-2026-0001"
    assert block.block_type == "bookshelf"
    assert block.category == "shipment_exceptions"
    assert block.metadata["tenant_id"] == "unitel-laos"
    assert block.metadata["market"] == "laos"
    assert block.metadata["domain"] == "logistics"
    assert block.metadata["module"] == "shipment_exceptions"
