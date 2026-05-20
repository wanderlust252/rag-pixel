# Domain Profiles

Domain Profiles keep RAG tuning outside backend service logic. A profile is a
versioned YAML file that describes the retrieval defaults, embedding defaults,
metadata priorities, glossary, and lexical rerank behavior for one document
domain or enterprise.

A profile is not a hardcoded knowledge base. It should not invent business
rules. It captures configuration derived from representative documents,
metadata, real questions, glossary terms, and ranking preferences supplied by
the business team.

## Select A Profile

Profiles live in `app/rag/profiles` by default. Select the active profile with:

```env
RAG_DOMAIN_PROFILE=logistics
```

The backend loads one active profile per process. If the selected profile file
does not exist, the loader falls back to `default.yaml`. If a profile file exists
but has an invalid shape, startup/query paths fail fast so the configuration can
be fixed.

Use `RAG_PROFILES_DIR=/path/to/profiles` to point the backend at another profile
directory for enterprise deployments.

## Create A New Profile

Start by copying `app/rag/profiles/default.yaml`:

```bash
cp app/rag/profiles/default.yaml app/rag/profiles/acme-logistics.yaml
```

Then change:

- `id` and `display_name`;
- `embedding` defaults if this domain needs a different local/API embedding
  setup;
- `retrieval.similarity_top_k` and `retrieval.candidate_top_k`;
- `retrieval.rerank` weights only after testing representative questions;
- `metadata.primary_ids` for exact IDs that users mention in questions;
- `metadata.recommended_filters` for fields that should be collected and passed
  as filters;
- `glossary` for domain synonyms, abbreviations, and mixed Vietnamese/English
  terms;
- `stopwords` for normalized words that should not affect lexical reranking.

Keep the profile small at first. Add tuning only when a real query or evaluation
case proves the need.

## Business Inputs Needed

To build a useful enterprise/domain profile, collect:

- representative documents, ideally 20-100 files across common doc types;
- metadata fields for each document, such as `doc_type`, IDs, status, owner,
  version, effective date, customer, or department;
- real user questions with expected source documents or expected answer phrases;
- glossary terms, abbreviations, and internal names;
- ranking preferences, such as whether approved/latest documents should beat
  drafts or whether SOPs should beat emails for process questions.

## Rebuild The Index

Rebuild the index after changing embedding-related settings:

- `embedding.provider`;
- `embedding.huggingface_model`;
- `embedding.use_e5_instructions`.

Run:

```bash
curl -X POST http://127.0.0.1:8000/documents/ingest
```

Retrieval-only settings such as top-k, glossary, stopwords, and rerank weights
can be changed without rebuilding the persisted vector index, though the backend
process must reload the profile.

## Logistics Example

Use the built-in logistics profile:

```env
RAG_DOMAIN_PROFILE=logistics
```

The logistics profile uses shipment-oriented IDs and filters:

```yaml
metadata:
  primary_ids:
    - shipment_id
    - doc_id
  recommended_filters:
    - doc_type
    - shipment_id
    - customer
    - carrier
    - warehouse
    - route
```

It also includes mixed Vietnamese/English glossary terms, for example:

```yaml
glossary:
  "vận đơn":
    - bill of lading
    - B/L
    - BL
```

This helps queries written as "vận đơn", "B/L", or "bill of lading" retrieve the
same family of documents without hardcoding logistics rules into Python code.
