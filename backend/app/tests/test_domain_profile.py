import pytest

from app.config import Settings
from app.rag.profile import DomainProfileService


def test_loads_default_profile(tmp_path) -> None:
    settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_domain_profile="default",
    )

    profile = DomainProfileService(settings).load()

    assert profile.id == "default"
    assert profile.retrieval.similarity_top_k == 20
    assert profile.retrieval.candidate_top_k == 60
    assert "doc_id" in profile.metadata.recommended_filters
    assert "doc_type" in profile.metadata.recommended_filters


def test_loads_logistics_profile(tmp_path) -> None:
    settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_domain_profile="logistics",
    )

    profile = DomainProfileService(settings).load()

    assert profile.id == "logistics"
    assert profile.embedding.provider == "huggingface"
    assert "tenant_id" in profile.metadata.primary_ids
    assert "shipment_id" in profile.metadata.primary_ids
    assert "market" in profile.metadata.recommended_filters
    assert "vận đơn" in profile.glossary


def test_unknown_profile_falls_back_to_default(tmp_path) -> None:
    settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_domain_profile="missing-enterprise",
    )

    profile = DomainProfileService(settings).load()

    assert profile.id == "default"


def test_invalid_profile_fails_fast(tmp_path) -> None:
    profile_dir = tmp_path / "profiles"
    profile_dir.mkdir()
    (profile_dir / "broken.yaml").write_text(
        """
id: broken
display_name: Broken
retrieval:
  similarity_top_k: 10
  candidate_top_k: 2
""".strip(),
        encoding="utf-8",
    )
    settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_profiles_dir=profile_dir,
        rag_domain_profile="broken",
    )

    with pytest.raises(ValueError, match="Invalid domain profile"):
        DomainProfileService(settings).load()
