import json
from pathlib import Path
from typing import Any

from app.rag.schemas import DocumentDetail, DocumentMetadata, DocumentSummary, UiDataBlock


REGISTRY_FILENAME = "documents_registry.json"


def load_sidecar_metadata(document_path: Path) -> DocumentMetadata:
    metadata_path = document_path.with_suffix(".metadata.json")
    if not metadata_path.exists():
        raise FileNotFoundError(f"Missing metadata sidecar: {metadata_path}")

    raw = json.loads(metadata_path.read_text(encoding="utf-8"))
    raw["source_path"] = str(document_path)
    return DocumentMetadata.model_validate(raw)


def metadata_to_llama(metadata: DocumentMetadata) -> dict[str, Any]:
    return metadata.model_dump(exclude_none=True)


def summary_from_metadata(metadata: dict[str, Any]) -> DocumentSummary:
    return DocumentSummary(
        doc_id=metadata["doc_id"],
        doc_type=metadata["doc_type"],
        title=metadata.get("title", metadata["doc_id"]),
        business_flow=metadata.get("business_flow"),
        room_id=metadata.get("room_id"),
        shelf_id=metadata.get("shelf_id"),
        shipment_id=metadata.get("shipment_id"),
        customer=metadata.get("customer"),
        carrier=metadata.get("carrier"),
        warehouse=metadata.get("warehouse"),
        route=metadata.get("route"),
    )


def detail_from_metadata(metadata: dict[str, Any]) -> DocumentDetail:
    return DocumentDetail.model_validate(metadata)


def ui_block_from_metadata(metadata: dict[str, Any]) -> UiDataBlock:
    doc_type = metadata.get("doc_type", "document")
    category = _category_for_doc_type(doc_type)
    return UiDataBlock(
        block_id=metadata.get("shelf_id") or metadata.get("doc_id", "unknown"),
        block_type="bookshelf",
        label=metadata.get("title") or metadata.get("doc_id", "Document"),
        category=metadata.get("room_id") or metadata.get("business_flow") or category,
        metadata={
            key: value
            for key, value in metadata.items()
            if key
            in {
                "doc_id",
                "doc_type",
                "business_flow",
                "room_id",
                "shelf_id",
                "shipment_id",
                "customer",
                "carrier",
                "warehouse",
                "route",
                "date",
                "source_type",
            }
        },
    )


def _category_for_doc_type(doc_type: str) -> str:
    if doc_type in {"bill_of_lading", "shipment_manifest", "customs_document"}:
        return "shipment_docs"
    if doc_type in {"tracking_event", "incident_report"}:
        return "shipment_exceptions"
    if doc_type in {"warehouse_inventory"}:
        return "warehouse_ops"
    if doc_type in {"customer_sla", "carrier_contract"}:
        return "contracts"
    return "documents"
