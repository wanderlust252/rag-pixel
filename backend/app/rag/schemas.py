from typing import Any

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class DocumentMetadata(BaseModel):
    doc_id: str
    doc_type: str
    title: str
    business_flow: str | None = None
    room_id: str | None = None
    shelf_id: str | None = None
    shipment_id: str | None = None
    customer: str | None = None
    carrier: str | None = None
    warehouse: str | None = None
    route: str | None = None
    date: str | None = None
    source_type: str | None = None
    source_path: str


class DocumentSummary(BaseModel):
    doc_id: str
    doc_type: str
    title: str
    business_flow: str | None = None
    room_id: str | None = None
    shelf_id: str | None = None
    shipment_id: str | None = None
    customer: str | None = None
    carrier: str | None = None
    warehouse: str | None = None
    route: str | None = None


class DocumentDetail(DocumentMetadata):
    pass


class DocumentListResponse(BaseModel):
    documents: list[DocumentSummary]


class IngestResponse(BaseModel):
    ingested_documents: int
    index_persisted: bool


class ClearDocumentsResponse(BaseModel):
    documents_removed: int
    metadata_removed: int
    index_cleared: bool


class ClearIndexResponse(BaseModel):
    index_cleared: bool


class QueryFilters(BaseModel):
    doc_id: str | None = None
    doc_type: str | list[str] | None = None
    business_flow: str | None = None
    room_id: str | None = None
    shipment_id: str | None = None
    customer: str | None = None
    carrier: str | None = None
    warehouse: str | None = None
    route: str | None = None


class QueryRequest(BaseModel):
    question: str = Field(min_length=1)
    filters: QueryFilters | None = None


class SourceReference(BaseModel):
    doc_id: str
    doc_type: str
    title: str | None = None
    snippet: str
    score: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class UiDataBlock(BaseModel):
    block_id: str
    block_type: str = "bookshelf"
    label: str
    category: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceReference]
    ui_blocks: list[UiDataBlock]
