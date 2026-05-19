from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

from rag_pixels_mcp.client import request_json, upload_file


mcp = FastMCP("rag-pixels")


def _clean_filters(filters: dict[str, str | None]) -> dict[str, str] | None:
    cleaned = {key: value for key, value in filters.items() if value}
    return cleaned or None


@mcp.tool()
async def health_check() -> dict[str, Any]:
    """Check whether the RAG Pixels backend is reachable."""
    return await request_json("GET", "/health", timeout=10.0)


@mcp.tool()
async def list_documents() -> dict[str, Any]:
    """List documents currently available in the RAG Pixels backend."""
    return await request_json("GET", "/documents")


@mcp.tool()
async def get_document(doc_id: str) -> dict[str, Any]:
    """Get metadata for one document by business document id."""
    return await request_json("GET", f"/documents/{doc_id}")


@mcp.tool()
async def rag_query(
    question: str,
    doc_id: str | None = None,
    room_id: str | None = None,
    business_flow: str | None = None,
    shipment_id: str | None = None,
    customer: str | None = None,
    carrier: str | None = None,
    warehouse: str | None = None,
    route: str | None = None,
    date: str | None = None,
) -> dict[str, Any]:
    """Ask the backend LLM for an answer. Prefer rag_retrieve for agent answers."""
    filters = _clean_filters(
        {
            "doc_id": doc_id,
            "room_id": room_id,
            "business_flow": business_flow,
            "shipment_id": shipment_id,
            "customer": customer,
            "carrier": carrier,
            "warehouse": warehouse,
            "route": route,
            "date": date,
        }
    )
    return await request_json(
        "POST",
        "/rag/query",
        json_body={"question": question, "filters": filters},
    )


@mcp.tool()
async def rag_retrieve(
    query: str,
    doc_id: str | None = None,
    room_id: str | None = None,
    business_flow: str | None = None,
    shipment_id: str | None = None,
    customer: str | None = None,
    carrier: str | None = None,
    warehouse: str | None = None,
    route: str | None = None,
    date: str | None = None,
) -> dict[str, Any]:
    """Retrieve relevant backend RAG context for an agent to answer with."""
    filters = _clean_filters(
        {
            "doc_id": doc_id,
            "room_id": room_id,
            "business_flow": business_flow,
            "shipment_id": shipment_id,
            "customer": customer,
            "carrier": carrier,
            "warehouse": warehouse,
            "route": route,
            "date": date,
        }
    )
    return await request_json(
        "POST",
        "/rag/retrieve",
        json_body={"question": query, "filters": filters},
    )


@mcp.tool()
async def upload_document(
    file_path: str,
    doc_id: str,
    doc_type: str,
    title: str,
    business_flow: str | None = None,
    room_id: str | None = None,
    shelf_id: str | None = None,
    shipment_id: str | None = None,
    customer: str | None = None,
    carrier: str | None = None,
    warehouse: str | None = None,
    route: str | None = None,
    date: str | None = None,
    source_type: str | None = None,
    overwrite: bool = False,
    reindex: bool = True,
) -> dict[str, Any]:
    """Upload a local source document into the backend and optionally rebuild the RAG index."""
    path = Path(file_path).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"Document file does not exist: {path}")

    form_data = {
        "doc_id": doc_id,
        "doc_type": doc_type,
        "title": title,
        "overwrite": str(overwrite).lower(),
        "reindex": str(reindex).lower(),
    }
    optional = {
        "business_flow": business_flow,
        "room_id": room_id,
        "shelf_id": shelf_id,
        "shipment_id": shipment_id,
        "customer": customer,
        "carrier": carrier,
        "warehouse": warehouse,
        "route": route,
        "date": date,
        "source_type": source_type,
    }
    form_data.update({key: value for key, value in optional.items() if value})

    return await upload_file(path, form_data=form_data)


@mcp.tool()
async def clear_documents(confirm: bool = False) -> dict[str, Any]:
    """Clear all uploaded documents, metadata sidecars, and the persisted RAG index."""
    if not confirm:
        raise ValueError("Set confirm=true to clear all backend documents and index data.")
    return await request_json("DELETE", "/documents")


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
