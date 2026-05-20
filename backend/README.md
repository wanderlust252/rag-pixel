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

Domain profile:

```env
RAG_DOMAIN_PROFILE=logistics
```

Domain profiles keep retrieval tuning, glossary terms, and metadata priorities
outside service logic. See [`docs/domain-profiles.md`](docs/domain-profiles.md)
for the profile format and customization workflow.

Hugging Face local embeddings:

```env
RAG_EMBEDDING_PROVIDER=huggingface
HUGGINGFACE_EMBEDDING_MODEL=intfloat/multilingual-e5-small
```

`intfloat/multilingual-e5-small` is the recommended local default for mixed
Vietnamese/English documents. The backend automatically applies E5's
`query:`/`passage:` instructions when this model family is selected. Rebuild the
index after changing embedding models. Top-k and rerank behavior now come from
the active domain profile.

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

curl -X POST http://127.0.0.1:8000/documents/upload \
  -F "file=@/path/to/document.pdf" \
  -F "doc_id=SRS-METFONE-SALARY-20260515" \
  -F "doc_type=srs" \
  -F "title=SRS Luong khoan Metfone 20260515" \
  -F "business_flow=salary_calculation" \
  -F "room_id=cambodia_market" \
  -F "shelf_id=metfone_salary_srs" \
  -F "source_type=pdf" \
  -F "reindex=true"

curl -X POST http://127.0.0.1:8000/documents/ingest

curl -X DELETE http://127.0.0.1:8000/documents/index

curl -X DELETE http://127.0.0.1:8000/documents

curl -X POST http://127.0.0.1:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Why is shipment SHP-001 delayed?","filters":{"shipment_id":"SHP-001"}}'

curl -X POST http://127.0.0.1:8000/rag/retrieve \
  -H "Content-Type: application/json" \
  -d '{"question":"Why is shipment SHP-001 delayed?","filters":{"shipment_id":"SHP-001"}}'
```

For a bookshelf-level chat, filter by `doc_id`. For a room-level chat, filter by `room_id` or `business_flow`.

Use `/rag/retrieve` for agent/MCP flows. It returns source snippets and UI
blocks only, so the calling agent can write the final answer. Use `/rag/query`
when the backend should call its configured LLM and return an `answer` itself.

`POST /documents/upload` accepts multipart form data. It writes the uploaded file
and metadata sidecar into the document store. By default `reindex=true`, so the
document is queryable immediately after upload. Use `overwrite=true` to replace
an existing document with the same `doc_id`.

`DELETE /documents/index` removes only the persisted vector index. `DELETE /documents`
removes supported source documents, their `*.metadata.json` sidecars, and the persisted
index so the backend can start with a clean document store.

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

Document conversion uses Microsoft MarkItDown and writes a canonical `.md` file
for indexing. Supported upload suffixes include PDF, Word, PowerPoint, Excel,
HTML, text-based formats, images, audio metadata/transcription formats, ZIP, and
EPub files supported by MarkItDown.

## MCP Server

The MCP adapter has been split out of the backend source and now lives under
`../mcp`. Keep the backend running, then start MCP from that package:

```bash
cd ../mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
export RAG_PIXELS_API_BASE_URL=http://127.0.0.1:8000
rag-pixels-mcp
```

`RAG_PIXELS_API_KEY` is optional. For local development, leave it unset. If the
backend later enables auth, set it in the MCP process and it will be sent as a
bearer token.

Available MCP tools:

- `health_check`: check backend availability.
- `list_documents`: list indexed documents.
- `get_document`: read one document metadata record by `doc_id`.
- `rag_retrieve`: retrieve relevant context for the calling agent to answer with.
- `rag_query`: ask a question and let the backend LLM write an answer.
- `upload_document`: upload a local file through the REST upload API.
- `clear_documents`: clear source documents, metadata, and index; requires `confirm=true`.

## Notes

- Keep backend business logic private if the MCP adapter is published separately.
- Publish only `../mcp` if you want agents to integrate through MCP without exposing backend source.
- Prefer `rag_retrieve` for external agents. It avoids coupling the backend to
  OpenCode Go for answer generation; the agent becomes responsible for the final
  response.
