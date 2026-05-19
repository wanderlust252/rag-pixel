from typing import Any

from app.config import Settings
from app.rag.index import RagIndexService
from app.rag.metadata import ui_block_from_metadata
from app.rag.schemas import QueryRequest, QueryResponse, SourceReference


class RagQueryService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def query(self, request: QueryRequest) -> QueryResponse:
        index = RagIndexService(self.settings).load()
        query_engine = index.as_query_engine(
            similarity_top_k=self.settings.similarity_top_k,
            filters=self._build_filters(request),
        )
        response = query_engine.query(request.question)

        sources = [self._source_from_node(node) for node in response.source_nodes]
        ui_blocks = []
        seen_blocks = set()
        for source in sources:
            block = ui_block_from_metadata(source.metadata)
            if block.block_id in seen_blocks:
                continue
            seen_blocks.add(block.block_id)
            ui_blocks.append(block)

        return QueryResponse(answer=str(response), sources=sources, ui_blocks=ui_blocks)

    def _build_filters(self, request: QueryRequest):
        if request.filters is None:
            return None

        filters = request.filters.model_dump(exclude_none=True)
        if not filters:
            return None

        from llama_index.core.vector_stores import (
            FilterOperator,
            MetadataFilter,
            MetadataFilters,
        )

        exact_filters = []
        for key, value in filters.items():
            if isinstance(value, list):
                exact_filters.append(
                    MetadataFilter(key=key, value=value, operator=FilterOperator.IN)
                )
            else:
                exact_filters.append(MetadataFilter(key=key, value=value))

        return MetadataFilters(filters=exact_filters)

    def _source_from_node(self, source_node: Any) -> SourceReference:
        node = source_node.node
        metadata = dict(node.metadata)
        snippet = node.get_content(metadata_mode="none").strip()
        if len(snippet) > 500:
            snippet = f"{snippet[:497]}..."

        return SourceReference(
            doc_id=metadata.get("doc_id", "unknown"),
            doc_type=metadata.get("doc_type", "document"),
            title=metadata.get("title"),
            snippet=snippet,
            score=source_node.score,
            metadata=metadata,
        )
