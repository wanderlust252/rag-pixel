from app.config import Settings
from app.rag.query import RagQueryService
from app.rag.schemas import QueryRequest


def test_retrieve_uses_retriever_without_llm(monkeypatch) -> None:
    load_calls = []

    class FakeRagIndexService:
        def __init__(self, settings):
            self.settings = settings

        def load(self, *, include_llm: bool = True):
            load_calls.append(include_llm)
            return FakeIndex()

    class FakeIndex:
        def as_retriever(self, *, similarity_top_k, filters):
            assert similarity_top_k == 60
            assert filters is None
            return FakeRetriever()

    class FakeRetriever:
        def retrieve(self, query):
            assert query == "Where is SHP-001?"
            return [FakeSourceNode()]

    class FakeSourceNode:
        score = 0.91
        node = None

        def __init__(self):
            self.node = FakeNode()

    class FakeNode:
        metadata = {
            "doc_id": "INC-2026-0001",
            "doc_type": "incident_report",
            "title": "Incident Report INC-2026-0001",
        }

        def get_content(self, metadata_mode):
            assert metadata_mode == "none"
            return "Shipment SHP-001 is delayed by weather."

    monkeypatch.setattr("app.rag.query.RagIndexService", FakeRagIndexService)

    response = RagQueryService(Settings()).retrieve(
        QueryRequest(question="Where is SHP-001?")
    )

    assert load_calls == [False]
    assert response.query == "Where is SHP-001?"
    assert response.matches[0].doc_id == "INC-2026-0001"
    assert response.matches[0].snippet == "Shipment SHP-001 is delayed by weather."
    assert response.ui_blocks[0].block_id == "INC-2026-0001"


def test_retrieve_uses_profile_candidate_top_k(tmp_path, monkeypatch) -> None:
    profile_dir = tmp_path / "profiles"
    profile_dir.mkdir()
    (profile_dir / "default.yaml").write_text(
        """
id: default
display_name: Default
embedding:
  provider: mock
retrieval:
  similarity_top_k: 1
  candidate_top_k: 7
  rerank:
    lexical_enabled: false
metadata: {}
glossary: {}
stopwords: []
""".strip(),
        encoding="utf-8",
    )
    seen_top_k = []

    class FakeRagIndexService:
        def __init__(self, settings):
            self.settings = settings

        def load(self, *, include_llm: bool = True):
            return FakeIndex()

    class FakeIndex:
        def as_retriever(self, *, similarity_top_k, filters):
            seen_top_k.append(similarity_top_k)
            return FakeRetriever()

    class FakeRetriever:
        def retrieve(self, query):
            return [
                _FakeSourceNode(0.9, "first"),
                _FakeSourceNode(0.8, "second"),
            ]

    monkeypatch.setattr("app.rag.query.RagIndexService", FakeRagIndexService)

    response = RagQueryService(
        Settings(
            documents_dir=tmp_path / "documents",
            index_dir=tmp_path / "index",
            rag_profiles_dir=profile_dir,
        )
    ).retrieve(QueryRequest(question="anything"))

    assert seen_top_k == [7]
    assert len(response.matches) == 1


def test_retrieve_reranks_specific_date_and_conference_context() -> None:
    service = RagQueryService(Settings())
    query = "Tại Hội nghị Trung ương 6, khóa X (8-2007), Quan điểm chỉ đạo của Trung ương là gì?"
    nodes = [
        _FakeSourceNode(
            0.90,
            "Quan điểm chỉ đạo của Trung ương là: Thanh niên là rường cột của nước nhà.",
        ),
        _FakeSourceNode(
            0.84,
            "Hội nghị Trung ương 6, khóa X (8-2007) đã ban hành Nghị quyết. "
            "Quan điểm chỉ đạo của Trung ương: Kiên định quan điểm giai cấp công nhân.",
        ),
    ]

    reranked = service._rerank_nodes(query, nodes)

    assert "Kiên định quan điểm giai cấp công nhân" in reranked[0].node.get_content("none")


def test_rerank_has_no_hardcoded_august_2007_boost() -> None:
    service = RagQueryService(Settings())
    query_tokens = service._tokens("alpha beta")
    query_phrases = service._phrases(query_tokens)

    without_date = service._lexical_score("alpha beta", query_tokens, query_phrases)
    with_date = service._lexical_score("alpha beta 8 2007", query_tokens, query_phrases)

    assert with_date == without_date


class _FakeSourceNode:
    def __init__(self, score, text):
        self.score = score
        self.node = _FakeNode(text)


class _FakeNode:
    metadata = {}

    def __init__(self, text):
        self.text = text

    def get_content(self, metadata_mode):
        return self.text
