from typing import Literal

from pydantic import BaseModel, Field

from app.rag.schemas import DocumentDetail, DocumentSummary


class Position(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)


class LibraryPortal(BaseModel):
    portal_id: str
    label: str
    business_flow: str
    position: Position
    document_count: int


class Bookshelf(BaseModel):
    shelf_id: str
    label: str
    doc_id: str
    doc_type: str
    portal_id: str
    position: Position
    document: DocumentSummary


class GameWorldResponse(BaseModel):
    world_id: str = "business_library"
    name: str = "Business Library"
    width: int
    height: int
    tile_size: int
    spawn: Position
    portals: list[LibraryPortal]
    shelves: list[Bookshelf]


class GameInteractionRequest(BaseModel):
    target_type: Literal["portal", "bookshelf"]
    target_id: str
    question: str | None = Field(default=None, min_length=1, max_length=500)


class GameInteractionResponse(BaseModel):
    interaction_id: str
    target_type: Literal["portal", "bookshelf"]
    title: str
    message: str
    document: DocumentDetail | None = None
    related_documents: list[DocumentSummary] = Field(default_factory=list)
