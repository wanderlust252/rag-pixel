# RAG Pixels Agent Notes

## Project Context

RAG Pixels is a prototype that connects a logistics-focused RAG backend with a
2D pixel-library interface. The product metaphor is a character walking through
a library:

- Rooms map to business flows, markets, or domains.
- Bookshelves map to source documents.
- Interactions open scoped chat or source-document context.
- Source documents remain the system of record.

Phase 1 built the Python RAG backend. Phase 2 adds the pixel-library frontend
and game-facing API surface.

## Repository Layout

- `backend/`: FastAPI backend with RAG ingestion, indexing, retrieval, query,
  document upload, and game-world endpoints.
- `frontend/`: Vite + React + TypeScript pixel-library UI.
- `mcp/`: standalone MCP adapter package that forwards agent tool calls to the
  backend HTTP API.
- `PHASE_1_PLAN.md`: original backend/RAG product and architecture plan.
- `PHASE_2_ASSET_REQUIREMENTS.md`: current asset and next-model notes for the
  pixel UI.
- `Parse.md`: project notes; inspect before changing parsing/conversion work.

Generated or build output such as `backend/build/` should not be edited unless
there is a specific packaging/build task.

## Backend

Stack:

- Python 3.11+
- FastAPI
- Pydantic v2
- LlamaIndex
- MarkItDown for canonical Markdown conversion
- Optional LlamaParse fallback
- Pytest

Local setup:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Run:

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Test:

```bash
cd backend
source .venv/bin/activate
pytest
```

Important backend endpoints:

- `GET /health`
- `POST /documents/upload`
- `POST /documents/ingest`
- `GET /documents`
- `GET /documents/{doc_id}`
- `DELETE /documents/index`
- `DELETE /documents`
- `POST /rag/retrieve`
- `POST /rag/query`
- `GET /game/world`
- `POST /game/interactions`

Write operations such as document upload and full document clearing require
`Authorization: Bearer <RAG_PIXELS_API_KEY>`. If the backend has no
`RAG_PIXELS_API_KEY`, protected write operations are disabled.

Prefer `/rag/retrieve` for agent workflows because it returns source snippets,
metadata, and UI blocks while leaving final answer composition to the calling
agent. Use `/rag/query` when the backend should generate the answer itself.

## RAG And Metadata Rules

Treat source files plus `*.metadata.json` sidecars as the source of truth. Do
not introduce a knowledge graph, extracted event store, or structured fact
catalog unless the task explicitly asks for it.

Core metadata fields used across retrieval and UI mapping include:

- `doc_id`
- `doc_type`
- `title`
- `tenant_id`
- `market`
- `country`
- `domain`
- `module`
- `business_flow`
- `room_id`
- `shelf_id`
- logistics-specific fields such as `shipment_id`, `customer`, `carrier`,
  `warehouse`, `route`, and `date`

For multi-market use cases, keep customer/market separation in document
metadata and query filters such as `tenant_id`, `market`, `country`, `domain`,
and `module`. Do not fork logic per tenant unless required.

Domain profiles live under `backend/app/rag/profiles`. Select a profile with
`RAG_DOMAIN_PROFILE`, and use `backend/docs/domain-profiles.md` as the guide for
profile changes. Rebuild the index after changing embedding provider/model
settings.

The recommended local embedding default for mixed Vietnamese/English documents
is `intfloat/multilingual-e5-small`; the backend applies E5 query/passage
instructions when that model family is selected.

## Frontend

Stack:

- Vite
- React 19
- TypeScript
- Axios

Run:

```bash
cd frontend
npm install
npm run dev
```

Build:

```bash
cd frontend
npm run build
```

The frontend API base defaults to `/api`; set `VITE_API_BASE_URL` when pointing
directly at another backend origin.

The current UI is an actual game-like workspace, not a marketing landing page.
Preserve the direct playable experience: session gate, character selection,
movement, target interaction, bookshelf/portal context, and scoped RAG chat.

## MCP Adapter

The MCP adapter is intentionally separated from backend business logic. Keep
`mcp/` publishable as a standalone package that only forwards requests to a
configured RAG Pixels HTTP API.

Run locally:

```bash
cd mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
export RAG_PIXELS_API_BASE_URL=http://127.0.0.1:8000
rag-pixels-mcp
```

Read-only MCP tools do not require `RAG_PIXELS_API_KEY`. Write tools such as
`upload_document` and `clear_documents` require the same backend write key.

## Development Guidance

- Follow existing module boundaries: backend RAG logic under `backend/app/rag`,
  game-facing API logic under `backend/app/game`, frontend UI under
  `frontend/src`, and MCP forwarding logic under `mcp/src/rag_pixels_mcp`.
- Add or adjust focused tests when behavior changes, especially for ingestion,
  upload, metadata filtering, retrieval, and game interaction contracts.
- Do not edit generated `backend/build/` files for normal source changes.
- Do not commit credentials, local document stores, vector indexes, or private
  uploaded files.
- Be careful with existing uncommitted user changes. Inspect before editing the
  same file and avoid reverting unrelated work.
- Prefer small, scoped changes that keep the document-centered RAG model intact.
