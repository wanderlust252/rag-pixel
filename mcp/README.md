# RAG Pixels MCP

MCP server for connecting AI agents to a RAG Pixels backend.

RAG Pixels MCP exposes document and retrieval tools through the Model Context
Protocol, then forwards those requests to a configured RAG Pixels HTTP API. The
backend can run on the same machine during development or be hosted on an
internal/public server in production.

This npm package contains only the MCP adapter. It does not include backend
business logic, RAG indexing code, source documents, vector stores, prompts, or
private credentials.

## Quick Start

Point the MCP server at your backend URL, then run it with `npx`:

```bash
export RAG_PIXELS_API_BASE_URL=https://your-rag-pixels-backend.example.com
npx rag-pixels-mcp
```

For a local backend, use your local API address instead:

```bash
export RAG_PIXELS_API_BASE_URL=http://127.0.0.1:8000
npx rag-pixels-mcp
```

If `RAG_PIXELS_API_BASE_URL` is not set, the adapter defaults to
`http://127.0.0.1:8000` for local development.

## Configuration

| Environment variable | Required | Description |
| --- | --- | --- |
| `RAG_PIXELS_API_BASE_URL` | No | Base URL of the RAG Pixels backend. Defaults to `http://127.0.0.1:8000`. |
| `RAG_PIXELS_API_KEY` | No | Bearer token for protected write tools such as `upload_document` and `clear_documents`. |
| `RAG_PIXELS_MCP_PYTHON` | No | Path to a Python 3.11+ interpreter if one is not discoverable on `PATH`. |

Example with protected write tools enabled:

```bash
export RAG_PIXELS_API_BASE_URL=https://your-rag-pixels-backend.example.com
export RAG_PIXELS_API_KEY=the_same_write_key_configured_on_the_backend
npx rag-pixels-mcp
```

Read-only tools such as `health_check`, `list_documents`, `get_document`,
`rag_retrieve`, and `rag_query` do not require `RAG_PIXELS_API_KEY`. Set the key
only when you want this MCP server to call protected backend write operations.

## Runtime Requirements

- Node.js/npm or another npm-compatible runner for `npx`.
- Python 3.11+ available on `PATH`, or configured with `RAG_PIXELS_MCP_PYTHON`.

On first run, the npm wrapper creates a Python virtual environment under
`~/.cache/rag-pixels-mcp/venv`, installs the bundled Python MCP adapter and its
dependencies, then starts the MCP server.

## Tools

- `health_check`: check backend availability.
- `list_documents`: list documents currently available through the backend.
- `get_document`: read one document metadata record by `doc_id`.
- `rag_retrieve`: retrieve relevant source context so the calling agent can
  write the final answer.
- `rag_query`: ask a question and let the backend generate the answer.
- `upload_document`: upload a local file through the backend REST API.
- `clear_documents`: clear source documents, metadata, and index data; requires
  `confirm=true`.

Prefer `rag_retrieve` for most agent workflows. It gives the agent source
snippets and metadata while keeping final response generation in the agent
client. Use `rag_query` when you explicitly want the backend to generate the
natural-language answer.

`upload_document` and `clear_documents` require the backend write API key. The
MCP server sends that key as `Authorization: Bearer <RAG_PIXELS_API_KEY>` when
the environment variable is configured.

## Local Development

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

## Publishing

This directory is designed to be publishable as a standalone npm package and to
remain cleanly separable into its own public repository. Keep only the MCP
adapter here. The private backend should remain behind the HTTP API.
