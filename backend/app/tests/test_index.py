from app.config import Settings
from app.rag.index import RagIndexService


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


def test_huggingface_non_e5_embeddings_do_not_get_e5_instructions(tmp_path) -> None:
    settings = Settings(
        documents_dir=tmp_path / "documents",
        index_dir=tmp_path / "index",
        huggingface_embedding_model="BAAI/bge-m3",
    )

    kwargs = RagIndexService(settings)._huggingface_embedding_kwargs()

    assert kwargs == {"model_name": "BAAI/bge-m3"}
