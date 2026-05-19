from typing import Literal

from pydantic import BaseModel, Field

from app.rag.schemas import DocumentDetail, DocumentSummary


class Position(BaseModel):
    x: int = Field(ge=0)
    y: int = Field(ge=0)


class SpriteAnimation(BaseModel):
    name: str
    row: int = Field(ge=0)
    frames: int = Field(ge=1)
    frame_duration_ms: int = Field(default=120, ge=16)


class CharacterSprite(BaseModel):
    image_url: str
    frame_width: int = Field(gt=0)
    frame_height: int = Field(gt=0)
    columns: int = Field(gt=0)
    rows: int = Field(gt=0)
    animations: list[SpriteAnimation]


class GameCharacter(BaseModel):
    character_id: str
    display_name: str
    description: str
    sprite: CharacterSprite


class GameCharacterListResponse(BaseModel):
    characters: list[GameCharacter]


class GameSessionCreateRequest(BaseModel):
    user_name: str = Field(min_length=3, max_length=32, pattern=r"^[a-zA-Z0-9_-]+$")
    display_name: str = Field(min_length=1, max_length=48)
    character_id: str


class GameCharacterChangeRequest(BaseModel):
    character_id: str


class GamePositionUpdateRequest(BaseModel):
    position: Position


class GameSession(BaseModel):
    session_id: str
    user_name: str
    display_name: str
    character: GameCharacter
    position: Position


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
    session_id: str
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
