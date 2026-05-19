# RAG Pixels MCP

Public MCP adapter for the private RAG Pixels backend.

This package exposes MCP tools and forwards requests to the backend HTTP API. It
does not contain backend business logic, RAG indexing code, documents, vector
stores, prompts, or private credentials.

## Local Setup

Keep the backend running first:

```bash
cd ../backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Then run MCP in another terminal:

```bash
cd mcp
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
export RAG_PIXELS_API_BASE_URL=http://127.0.0.1:8000
rag-pixels-mcp
```

`RAG_PIXELS_API_KEY` is optional. Leave it unset for local development or a
simple internal demo. If the backend later requires auth, set it and the MCP
adapter will send it as a bearer token:

```bash
export RAG_PIXELS_API_KEY=your_backend_token
```

## Tools

- `health_check`: check backend availability.
- `list_documents`: list indexed documents.
- `get_document`: read one document metadata record by `doc_id`.
- `rag_retrieve`: retrieve relevant context and sources for the calling agent
  to write the final answer. This is the recommended tool for MCP clients.
- `rag_query`: ask a question with optional metadata filters and let the
  backend LLM write an answer. Keep this for legacy/backend-owned chat flows.
- `upload_document`: upload a local file through the backend REST API.
- `clear_documents`: clear source documents, metadata, and index; requires
  `confirm=true`.

`rag_retrieve` does not require the backend to configure an answering LLM such
as OpenCode Go. It only needs the configured embedding provider and an existing
index. Use `rag_query` only when you explicitly want the backend, not the agent,
to produce the final natural-language answer.

## Publishing

This directory is designed to be moved into its own public repository. Keep only
the MCP adapter here. The private backend should remain behind the HTTP API.
