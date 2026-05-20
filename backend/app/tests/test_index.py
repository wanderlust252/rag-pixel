from app.config import Settings
from app.rag.index import RagIndexService
from app.rag.profile import DomainProfileService


def test_huggingface_e5_embeddings_use_required_instructions(tmp_path) -> None:
    settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        huggingface_embedding_model="intfloat/multilingual-e5-small",
    )

    kwargs = RagIndexService(settings)._huggingface_embedding_kwargs()

    assert kwargs == {
        "model_name": "intfloat/multilingual-e5-small",
        "query_instruction": "query: ",
        "text_instruction": "passage: ",
    }


def test_huggingface_e5_instructions_can_be_disabled_by_profile(tmp_path) -> None:
    profile_dir = tmp_path / "profiles"
    profile_dir.mkdir()
    (profile_dir / "default.yaml").write_text(
        """
id: default
display_name: Default
embedding:
  provider: huggingface
  huggingface_model: intfloat/multilingual-e5-small
  use_e5_instructions: false
retrieval:
  similarity_top_k: 4
  candidate_top_k: 8
metadata: {}
glossary: {}
stopwords: []
""".strip(),
        encoding="utf-8",
    )
    settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        rag_profiles_dir=profile_dir,
        rag_domain_profile="default",
    )

    profile = DomainProfileService(settings).load()
    kwargs = RagIndexService(settings)._huggingface_embedding_kwargs(profile)

    assert kwargs == {"model_name": "intfloat/multilingual-e5-small"}


def test_huggingface_non_e5_embeddings_do_not_get_e5_instructions(tmp_path) -> None:
    settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        huggingface_embedding_model="BAAI/bge-m3",
    )

    kwargs = RagIndexService(settings)._huggingface_embedding_kwargs()

    assert kwargs == {"model_name": "BAAI/bge-m3"}
