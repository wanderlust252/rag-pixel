import logging
import re
from time import perf_counter
from typing import Any
from unicodedata import category, normalize

from app.config import Settings
from app.rag.index import RagIndexService
from app.rag.metadata import ui_block_from_metadata
from app.rag.profile import DomainProfileService, expand_query_with_glossary
from app.rag.schemas import (
    QueryRequest,
    QueryResponse,
    RetrieveResponse,
    SourceReference,
)

logger = logging.getLogger(__name__)


class RagQueryService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.profile = DomainProfileService(settings).load()

    def query(self, request: QueryRequest) -> QueryResponse:
        total_started_at = perf_counter()
        index = RagIndexService(self.settings).load()
        load_elapsed = perf_counter() - total_started_at

        engine_started_at = perf_counter()
        question = expand_query_with_glossary(request.question, self.profile.glossary)
        query_engine = index.as_query_engine(
            similarity_top_k=self.profile.retrieval.similarity_top_k,
            filters=self._build_filters(request),
        )
        engine_elapsed = perf_counter() - engine_started_at

        llm_started_at = perf_counter()
        response = query_engine.query(question)
        llm_elapsed = perf_counter() - llm_started_at

        sources = [self._source_from_node(node) for node in response.source_nodes]
        ui_blocks = self._ui_blocks_from_sources(sources)

        logger.info(
            "RAG query timing load=%.3fs engine=%.3fs answer=%.3fs total=%.3fs question=%r sources=%d",
            load_elapsed,
            engine_elapsed,
            llm_elapsed,
            perf_counter() - total_started_at,
            request.question,
            len(sources),
        )

        return QueryResponse(answer=str(response), sources=sources, ui_blocks=ui_blocks)

    def retrieve(self, request: QueryRequest) -> RetrieveResponse:
        total_started_at = perf_counter()
        index = RagIndexService(self.settings).load(include_llm=False)
        load_elapsed = perf_counter() - total_started_at

        retriever_started_at = perf_counter()
        question = expand_query_with_glossary(request.question, self.profile.glossary)
        retriever = index.as_retriever(
            similarity_top_k=self.profile.retrieval.candidate_top_k,
            filters=self._build_filters(request),
        )
        nodes = self._rerank_nodes(question, retriever.retrieve(question))
        nodes = nodes[: self.profile.retrieval.similarity_top_k]
        retrieve_elapsed = perf_counter() - retriever_started_at

        matches = [self._source_from_node(node) for node in nodes]
        ui_blocks = self._ui_blocks_from_sources(matches)

        logger.info(
            "RAG retrieve timing load=%.3fs retrieve=%.3fs total=%.3fs query=%r matches=%d",
            load_elapsed,
            retrieve_elapsed,
            perf_counter() - total_started_at,
            request.question,
            len(matches),
        )

        return RetrieveResponse(query=request.question, matches=matches, ui_blocks=ui_blocks)

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

    def _rerank_nodes(self, query: str, nodes: list[Any]) -> list[Any]:
        if not self.profile.retrieval.rerank.lexical_enabled:
            return nodes

        query_tokens = self._tokens(query)
        query_phrases = self._phrases(query_tokens)
        if not query_tokens:
            return nodes

        def rank_key(source_node: Any) -> float:
            text = source_node.node.get_content(metadata_mode="none")
            lexical_score = self._lexical_score(text, query_tokens, query_phrases)
            return (source_node.score or 0.0) + lexical_score

        return sorted(nodes, key=rank_key, reverse=True)

    def _lexical_score(
        self,
        text: str,
        query_tokens: list[str],
        query_phrases: list[str],
    ) -> float:
        text_normalized = self._normalize_for_search(text)
        text_tokens = set(text_normalized.split())
        token_overlap = sum(1 for token in set(query_tokens) if token in text_tokens)
        phrase_hits = sum(1 for phrase in query_phrases if phrase in text_normalized)
        numeric_overlap = sum(
            1
            for token in set(query_tokens)
            if token.isdigit() and token in text_tokens
        )
        rerank = self.profile.retrieval.rerank
        return (
            token_overlap * rerank.token_overlap_weight
            + phrase_hits * rerank.phrase_hit_weight
            + numeric_overlap * rerank.numeric_token_weight
        )

    def _phrases(self, tokens: list[str]) -> list[str]:
        phrases = []
        rerank = self.profile.retrieval.rerank
        max_size = min(rerank.max_phrase_size, len(tokens))
        for size in range(max_size, rerank.min_phrase_size - 1, -1):
            for start in range(0, len(tokens) - size + 1):
                phrase = " ".join(tokens[start : start + size])
                if any(char.isdigit() for char in phrase) or size >= 5:
                    phrases.append(phrase)
        return phrases

    def _tokens(self, text: str) -> list[str]:
        stopwords = set(self.profile.stopwords)
        return [
            token
            for token in self._normalize_for_search(text).split()
            if token not in stopwords
        ]

    def _normalize_for_search(self, text: str) -> str:
        text = "".join(
            char
            for char in normalize("NFD", text.lower().replace("đ", "d"))
            if category(char) != "Mn"
        )
        return re.sub(r"[^a-z0-9]+", " ", text).strip()

    def _ui_blocks_from_sources(self, sources: list[SourceReference]):
        ui_blocks = []
        seen_blocks = set()
        for source in sources:
            block = ui_block_from_metadata(source.metadata)
            if block.block_id in seen_blocks:
                continue
            seen_blocks.add(block.block_id)
            ui_blocks.append(block)
        return ui_blocks

    def _source_from_node(self, source_node: Any) -> SourceReference:
        node = source_node.node
        metadata = dict(node.metadata)
        snippet = node.get_content(metadata_mode="none").strip()
        if len(snippet) > 1500:
            snippet = f"{snippet[:1497]}..."

        return SourceReference(
            doc_id=metadata.get("doc_id", "unknown"),
            doc_type=metadata.get("doc_type", "document"),
            title=metadata.get("title"),
            snippet=snippet,
            score=source_node.score,
            metadata=metadata,
        )
