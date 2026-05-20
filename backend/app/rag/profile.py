from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator

from app.config import Settings


DEFAULT_PROFILE_ID = "default"


class EmbeddingProfile(BaseModel):
    provider: str = "mock"
    huggingface_model: str | None = None
    use_e5_instructions: bool = False


class RerankProfile(BaseModel):
    lexical_enabled: bool = True
    token_overlap_weight: float = Field(default=0.003, ge=0)
    phrase_hit_weight: float = Field(default=0.02, ge=0)
    numeric_token_weight: float = Field(default=0.01, ge=0)
    max_phrase_size: int = Field(default=8, ge=3)
    min_phrase_size: int = Field(default=3, ge=1)


class RetrievalProfile(BaseModel):
    similarity_top_k: int = Field(default=20, ge=1, le=80)
    candidate_top_k: int = Field(default=60, ge=1, le=200)
    rerank: RerankProfile = Field(default_factory=RerankProfile)

    @field_validator("candidate_top_k")
    @classmethod
    def candidate_must_cover_final_top_k(cls, value: int, info):
        similarity_top_k = info.data.get("similarity_top_k")
        if similarity_top_k is not None and value < similarity_top_k:
            raise ValueError("candidate_top_k must be greater than or equal to similarity_top_k")
        return value


class MetadataProfile(BaseModel):
    primary_ids: list[str] = Field(default_factory=list)
    recommended_filters: list[str] = Field(default_factory=list)


class DomainProfile(BaseModel):
    id: str
    display_name: str
    embedding: EmbeddingProfile = Field(default_factory=EmbeddingProfile)
    retrieval: RetrievalProfile = Field(default_factory=RetrievalProfile)
    metadata: MetadataProfile = Field(default_factory=MetadataProfile)
    glossary: dict[str, list[str]] = Field(default_factory=dict)
    stopwords: list[str] = Field(default_factory=list)


class DomainProfileService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def load(self) -> DomainProfile:
        return load_domain_profile(
            profile_id=self.settings.rag_domain_profile,
            profiles_dir=self.settings.rag_profiles_dir,
        )


@lru_cache
def load_domain_profile(
    *,
    profile_id: str,
    profiles_dir: Path | None = None,
) -> DomainProfile:
    base_dir = profiles_dir or Path(__file__).with_name("profiles")
    profile_path = base_dir / f"{profile_id}.yaml"
    if not profile_path.exists() and profile_id != DEFAULT_PROFILE_ID:
        profile_path = base_dir / f"{DEFAULT_PROFILE_ID}.yaml"

    if not profile_path.exists():
        raise FileNotFoundError(f"Domain profile was not found: {profile_path}")

    raw = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Domain profile must be a YAML object: {profile_path}")

    try:
        return DomainProfile.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"Invalid domain profile {profile_path}: {exc}") from exc


def expand_query_with_glossary(query: str, glossary: dict[str, list[str]]) -> str:
    expansions: list[str] = []
    query_lower = query.lower()
    for term, synonyms in glossary.items():
        if term.lower() in query_lower:
            expansions.extend(synonyms)
            continue
        if any(synonym.lower() in query_lower for synonym in synonyms):
            expansions.append(term)

    if not expansions:
        return query
    return f"{query} {' '.join(expansions)}"
