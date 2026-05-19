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
            assert similarity_top_k == 20
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
