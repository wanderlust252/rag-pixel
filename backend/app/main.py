from fastapi import FastAPI, HTTPException

from app.config import get_settings
from app.rag.index import RagIndexService
from app.rag.ingest import RagIngestService
from app.rag.query import RagQueryService
from app.rag.schemas import (
    DocumentDetail,
    DocumentListResponse,
    HealthResponse,
    IngestResponse,
    QueryRequest,
    QueryResponse,
)

settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/documents/ingest", response_model=IngestResponse)
def ingest_documents() -> IngestResponse:
    documents = RagIngestService(settings).load_documents()
    RagIndexService(settings).build_and_persist(documents)
    return IngestResponse(ingested_documents=len(documents), index_persisted=True)


@app.get("/documents", response_model=DocumentListResponse)
def list_documents() -> DocumentListResponse:
    documents = RagIndexService(settings).list_documents()
    return DocumentListResponse(documents=documents)


@app.get("/documents/{doc_id}", response_model=DocumentDetail)
def get_document(doc_id: str) -> DocumentDetail:
    document = RagIndexService(settings).get_document(doc_id)
    if document is None:
        raise HTTPException(status_code=404, detail=f"Document {doc_id} was not found")
    return document


@app.post("/rag/query", response_model=QueryResponse)
def query_rag(request: QueryRequest) -> QueryResponse:
    return RagQueryService(settings).query(request)
