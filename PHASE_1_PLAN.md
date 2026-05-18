# Phase 1 Plan: Logistics RAG Backend With LlamaIndex

## Decision

Use LlamaIndex as a Python dependency, not as a forked codebase.

This project owns the logistics-specific layer:

- Document ingestion rules
- Logistics metadata schema
- Query API
- Source/citation response format
- UI-ready data block mapping for the future pixel library interface

LlamaIndex provides the RAG engine:

- Document loading
- Chunking
- Embedding
- Indexing
- Retrieval
- Query orchestration

## Phase 1 Goal

Build a Python backend that can:

1. Ingest sample logistics documents.
2. Attach normalized logistics metadata to each document/chunk.
3. Build and persist a LlamaIndex-powered RAG index.
4. Answer questions with source references.
5. Return response data that can later be rendered by a 2D pixel game UI.

The game UI is not part of phase 1.

The intended UI model is a character walking through a library:

- Each room represents a business flow.
- Each bookshelf represents a source document.
- Opening a bookshelf shows both a chat interface scoped to that document or room and a readable file view.

## Non-Goals

- Do not fork or modify LlamaIndex source.
- Do not build the pixel game UI yet.
- Do not add authentication or multi-tenant logic.
- Do not introduce Dify, RAGFlow, or another RAG platform.
- Do not over-engineer deployment infrastructure.
- Do not optimize for production scale before the data model and RAG behavior are validated.
- Do not build a structured knowledge catalog, knowledge graph, or extracted entity/event store in phase 1.

## Proposed Stack

- Language: Python
- API framework: FastAPI
- RAG framework: LlamaIndex
- Validation: Pydantic
- Local dev server: Uvicorn
- Initial vector/index storage: local persisted LlamaIndex storage
- Optional next vector store: Chroma
- Initial sample data format: Markdown, TXT, CSV
- Later document support: PDF, DOCX, XLSX

## Proposed Directory Structure

```text
rag-pixels/
  backend/
    app/
      main.py
      config.py
      rag/
        __init__.py
        ingest.py
        index.py
        query.py
        metadata.py
        schemas.py
      storage/
        documents/
        index/
      tests/
        test_ingest.py
        test_query.py
    pyproject.toml
    .env.example
  PHASE_1_PLAN.md
```

## Core Concepts

### 1. Logistics Document

A document is a real business artifact such as:

- Bill of lading
- Shipment manifest
- Warehouse inventory report
- Tracking event log
- Carrier contract
- Customer SLA document
- Customs document
- Incident/delay report

Each document should have metadata. This metadata is more important than deep knowledge extraction at this stage because it becomes the bridge between RAG retrieval, document browsing, and game objects later.

Example:

```json
{
  "doc_id": "BL-2026-0001",
  "doc_type": "bill_of_lading",
  "business_flow": "shipment_ops",
  "room_id": "shipment_room",
  "shelf_id": "BL-2026-0001",
  "shipment_id": "SHP-001",
  "customer": "ACME",
  "carrier": "Maersk",
  "warehouse": "WH-HCM-01",
  "route": "HCM -> Singapore",
  "date": "2026-05-18",
  "source_type": "markdown",
  "source_path": "storage/documents/bill_of_lading_sample.md"
}
```

Phase 1 organizes source documents, not extracted facts. The source files remain the system of record. The backend keeps enough metadata to browse, filter, retrieve, cite, and open the original file.

### 2. UI-Ready Data Block

Phase 1 does not render game objects, but the backend response should already expose enough structure for the future UI.

Example:

```json
{
  "block_id": "BL-2026-0001",
  "block_type": "bookshelf",
  "label": "Bill of Lading",
  "category": "shipment_room",
  "metadata": {
    "business_flow": "shipment_ops",
    "room_id": "shipment_room",
    "shelf_id": "BL-2026-0001",
    "shipment_id": "SHP-001",
    "customer": "ACME",
    "carrier": "Maersk"
  }
}
```

The future pixel UI can map these blocks to:

- Room, based on `business_flow` or `room_id`
- Bookshelf, based on `shelf_id` or `doc_id`
- Bookshelf label, based on `title`
- Chat scope, based on `doc_id`, `room_id`, or other metadata filters
- File reader, based on `source_path` and `source_type`

### 3. Structured Knowledge Records

Phase 1 intentionally does not extract separate structured knowledge records such as shipment timelines, SLA obligations, contract clauses, or incident entities.

Those records can be added later if the product needs views that are not document-centered, such as shipment timelines, exception dashboards, SLA breach lists, or contract obligation trackers. Until then, the document catalog plus RAG citations are sufficient for the library UI.

## API Design

### GET /health

Checks whether the backend is running.

Response:

```json
{
  "status": "ok"
}
```

### POST /documents/ingest

Ingests documents from the configured sample document directory.

Initial phase can keep this simple and ingest all files under `backend/app/storage/documents`.

Response:

```json
{
  "ingested_documents": 6,
  "index_persisted": true
}
```

### GET /documents

Lists known documents and their metadata.

Response:

```json
{
  "documents": [
    {
      "doc_id": "BL-2026-0001",
      "doc_type": "bill_of_lading",
      "business_flow": "shipment_ops",
      "room_id": "shipment_room",
      "shelf_id": "BL-2026-0001",
      "shipment_id": "SHP-001",
      "title": "Bill of Lading"
    }
  ]
}
```

### GET /documents/{doc_id}

Returns a single document metadata record.

Response:

```json
{
  "doc_id": "BL-2026-0001",
  "doc_type": "bill_of_lading",
  "business_flow": "shipment_ops",
  "room_id": "shipment_room",
  "shelf_id": "BL-2026-0001",
  "shipment_id": "SHP-001",
  "customer": "ACME",
  "carrier": "Maersk",
  "route": "HCM -> Singapore",
  "source_type": "markdown",
  "source_path": "storage/documents/bill_of_lading_sample.md"
}
```

### POST /rag/query

Asks a question against the RAG index.

Request:

```json
{
  "question": "Why is shipment SHP-001 delayed?",
  "filters": {
    "shipment_id": "SHP-001",
    "doc_type": ["tracking_event", "incident_report"]
  }
}
```

Response:

```json
{
  "answer": "Shipment SHP-001 is delayed because the container was held at the port for customs inspection.",
  "sources": [
    {
      "doc_id": "INC-2026-0001",
      "doc_type": "incident_report",
      "snippet": "Container ABC was held at Singapore port for customs inspection...",
      "score": 0.84
    }
  ],
  "ui_blocks": [
    {
      "block_id": "INC-2026-0001",
      "block_type": "bookshelf",
      "label": "Incident Report",
      "category": "incident_room"
    }
  ]
}
```

## Implementation Checklist

### Step 1: Backend Skeleton

- Create `backend/`.
- Add FastAPI app entrypoint.
- Add config module.
- Add `.env.example`.
- Add `/health`.
- Add local run command with Uvicorn.

Expected result:

```text
GET /health -> {"status":"ok"}
```

### Step 2: Python Dependencies

Add initial dependencies:

- `fastapi`
- `uvicorn`
- `pydantic`
- `pydantic-settings`
- `llama-index`
- `python-dotenv`

Optional after first POC:

- `llama-index-vector-stores-chroma`
- `chromadb`
- `pypdf`
- `python-docx`
- `pandas`

### Step 3: Sample Logistics Dataset

Create sample files under:

```text
backend/app/storage/documents/
```

Minimum sample documents:

- `shipment_manifest.md`
- `bill_of_lading_sample.md`
- `warehouse_inventory.csv`
- `tracking_events.csv`
- `customer_sla.md`
- `carrier_contract.md`
- `incident_report.md`

The sample dataset should support questions like:

- Which shipments are delayed?
- Why is shipment SHP-001 delayed?
- What is the SLA for customer ACME?
- Which carrier handles the HCM to Singapore route?
- Which warehouse currently stores shipment SHP-001?

### Step 4: Metadata Schema

Create Pydantic schemas for:

- `DocumentMetadata`
- `DocumentSummary`
- `QueryRequest`
- `QueryFilters`
- `SourceReference`
- `UiDataBlock`
- `QueryResponse`

Recommended metadata fields:

- `doc_id`
- `doc_type`
- `title`
- `business_flow`
- `room_id`
- `shelf_id`
- `shipment_id`
- `customer`
- `carrier`
- `warehouse`
- `route`
- `date`
- `source_type`
- `source_path`

### Step 5: Ingestion Service

Create `RagIngestService`.

Responsibilities:

- Read supported files from the sample document directory.
- Convert files into LlamaIndex documents.
- Attach normalized metadata.
- Validate metadata shape.
- Pass documents to the index service.

First version can use a simple sidecar metadata convention, such as:

```text
bill_of_lading_sample.md
bill_of_lading_sample.metadata.json
```

This avoids guessing business metadata from text.

### Step 6: Index Service

Create `RagIndexService`.

Responsibilities:

- Build an index from ingested documents.
- Persist the index to local storage.
- Load an existing index from disk.
- Rebuild the index when requested.

Initial storage:

```text
backend/app/storage/index/
```

### Step 7: Query Service

Create `RagQueryService`.

Responsibilities:

- Load the persisted index.
- Apply metadata filters where supported.
- Query LlamaIndex.
- Extract answer text.
- Extract source nodes.
- Convert source metadata into `SourceReference`.
- Convert source metadata into `UiDataBlock`.

The query service is the most important integration point for the future game UI.

### Step 8: API Integration

Wire services into FastAPI endpoints:

- `GET /health`
- `POST /documents/ingest`
- `GET /documents`
- `GET /documents/{doc_id}`
- `POST /rag/query`

Keep API responses stable and explicit. The future UI should not depend on raw LlamaIndex internals.

### Step 9: Basic Tests

Add tests for:

- Metadata validation
- Ingesting sample documents
- Persisting/loading index
- Query response shape
- Source references exist for known questions

Do not attempt full answer-quality evaluation yet.

### Step 10: Manual Acceptance Test

Run the backend locally and test:

```text
GET /health
POST /documents/ingest
POST /rag/query
```

Acceptance questions:

- Why is shipment SHP-001 delayed?
- What is the SLA for customer ACME?
- Which warehouse stores shipment SHP-001?
- Which carrier handles the HCM to Singapore route?

Acceptance criteria:

- The API returns an answer.
- The API returns at least one source for each answer.
- Source metadata includes `doc_id` and `doc_type`.
- Response includes `ui_blocks`.
- No game UI is required yet.

## Phase 1 Completion Criteria

Phase 1 is complete when:

- A Python FastAPI backend exists.
- LlamaIndex is integrated as a dependency.
- Sample logistics documents can be ingested.
- The index can be persisted and reloaded.
- Query API returns answer, sources, and UI-ready blocks.
- Basic tests pass.
- The backend can be called independently from any future frontend.

## Risks And Notes

### Metadata Quality

RAG quality for logistics will depend heavily on metadata quality. The first implementation should not try to infer everything automatically. Prefer explicit `.metadata.json` files for sample data.

### Document Parsing

If real project data includes scanned PDFs, tables, invoices, or complex spreadsheets, phase 2 may need better parsing tools. Phase 1 should validate the RAG flow with clean Markdown/CSV first.

### LLM And Embedding Cost

The backend should isolate model configuration in `config.py` so it can switch between paid APIs and local models later.

### UI Coupling

The backend should expose `ui_blocks`, but it should not know about sprite sheets, character movement, tile maps, or game engine state. Those belong to a later UI phase.

## Recommended Next Step

Implement the backend skeleton and sample dataset first, then wire in LlamaIndex ingestion and query services.
