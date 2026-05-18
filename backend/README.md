# RAG Pixels Backend

Python backend for phase 1: logistics RAG logic powered by LlamaIndex.

Phase 1 treats source files as the system of record. The backend organizes them as a document catalog for the future pixel-library UI: business rooms, bookshelves, scoped chat, readable source files, and citations. It does not extract a separate knowledge graph or structured event/entity catalog yet.

## Local Setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
```

Default `.env.example` uses mock LLM and mock embeddings so the service can be smoke-tested without a paid API key.

For real answers, configure an LLM + embeddings provider.

OpenAI (LLM + embeddings):

```env
RAG_LLM_PROVIDER=openai
RAG_EMBEDDING_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4.1-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

Anthropic (LLM) + OpenAI (embeddings):

```env
RAG_LLM_PROVIDER=anthropic
RAG_EMBEDDING_PROVIDER=openai
ANTHROPIC_API_KEY=your_key
ANTHROPIC_MODEL=claude-3-5-sonnet-latest
OPENAI_API_KEY=your_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
```

## Run

```bash
uvicorn app.main:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

## Basic Flow

```bash
curl http://127.0.0.1:8000/health

curl -X POST http://127.0.0.1:8000/documents/ingest

curl -X POST http://127.0.0.1:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Why is shipment SHP-001 delayed?","filters":{"shipment_id":"SHP-001"}}'
```

For a bookshelf-level chat, filter by `doc_id`. For a room-level chat, filter by `room_id` or `business_flow`.

## Document Metadata

Each source file should have a matching `*.metadata.json` sidecar file. Recommended UI fields:

```json
{
  "doc_id": "BL-2026-0001",
  "doc_type": "bill_of_lading",
  "title": "Bill of Lading BL-2026-0001",
  "business_flow": "shipment_ops",
  "room_id": "shipment_room",
  "shelf_id": "BL-2026-0001",
  "source_type": "markdown"
}
```

## Notes

- Keep this backend in the same repository as the future UI for now.
- Add the future UI under `frontend/` and treat this repo as a monorepo.
- Split into separate repositories only when deployment, ownership, or release cycles become independent.
