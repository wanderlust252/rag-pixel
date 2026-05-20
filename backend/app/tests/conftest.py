import pytest


@pytest.fixture(autouse=True)
def default_to_local_parser(monkeypatch) -> None:
    monkeypatch.setenv("RAG_PARSE_PROVIDER", "markitdown")
    monkeypatch.setenv("LLAMA_CLOUD_API_KEY", "")
