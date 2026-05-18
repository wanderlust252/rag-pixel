import json
from pathlib import Path
from uuid import uuid4

from app.config import Settings
from app.game.schemas import (
    Bookshelf,
    CharacterSprite,
    GameCharacter,
    GameInteractionResponse,
    GameSession,
    GameSessionCreateRequest,
    GameWorldResponse,
    LibraryPortal,
    Position,
    SpriteAnimation,
)
from app.rag.index import RagIndexService
from app.rag.metadata import detail_from_metadata, summary_from_metadata
from app.rag.schemas import DocumentDetail, DocumentSummary


class GameService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def list_characters(self) -> list[GameCharacter]:
        return _CHARACTERS

    def get_character(self, character_id: str) -> GameCharacter | None:
        for character in _CHARACTERS:
            if character.character_id == character_id:
                return character
        return None

    def get_world(self) -> GameWorldResponse:
        documents = self._load_document_summaries()
        portal_groups = _group_documents_by_flow(documents)

        portals: list[LibraryPortal] = []
        shelves: list[Bookshelf] = []
        for portal_index, (flow_id, flow_documents) in enumerate(portal_groups.items()):
            portal_position = Position(x=120 + portal_index * 220, y=96)
            portals.append(
                LibraryPortal(
                    portal_id=flow_id,
                    label=_label_for_flow(flow_id),
                    business_flow=flow_id,
                    position=portal_position,
                    document_count=len(flow_documents),
                )
            )

            for shelf_index, document in enumerate(flow_documents):
                row = shelf_index // 3
                column = shelf_index % 3
                shelves.append(
                    Bookshelf(
                        shelf_id=document.shelf_id or document.doc_id,
                        label=document.title,
                        doc_id=document.doc_id,
                        doc_type=document.doc_type,
                        portal_id=flow_id,
                        position=Position(
                            x=80 + portal_index * 220 + column * 56,
                            y=230 + row * 74,
                        ),
                        document=document,
                    )
                )

        return GameWorldResponse(
            width=max(960, 220 * max(len(portals), 1) + 160),
            height=640,
            tile_size=32,
            spawn=Position(x=96, y=520),
            portals=portals,
            shelves=shelves,
        )

    def get_document(self, doc_id: str) -> DocumentDetail | None:
        document = RagIndexService(self.settings).get_document(doc_id)
        if document is not None:
            return document

        for metadata in self._load_document_metadata():
            if metadata.get("doc_id") == doc_id:
                return detail_from_metadata(metadata)
        return None

    def interact(
        self,
        session: GameSession,
        target_type: str,
        target_id: str,
        question: str | None = None,
    ) -> GameInteractionResponse | None:
        world = self.get_world()
        if target_type == "portal":
            for portal in world.portals:
                if portal.portal_id == target_id:
                    related_documents = [
                        shelf.document for shelf in world.shelves if shelf.portal_id == portal.portal_id
                    ]
                    return GameInteractionResponse(
                        interaction_id=str(uuid4()),
                        target_type="portal",
                        title=portal.label,
                        message=(
                            f"{session.display_name} opened {portal.label}. "
                            f"{portal.document_count} business file(s) are available."
                        ),
                        related_documents=related_documents,
                    )
            return None

        if target_type == "bookshelf":
            for shelf in world.shelves:
                if shelf.shelf_id == target_id:
                    document = self.get_document(shelf.doc_id)
                    if document is None:
                        return None
                    prompt = question or f"Open {document.title}"
                    return GameInteractionResponse(
                        interaction_id=str(uuid4()),
                        target_type="bookshelf",
                        title=document.title,
                        message=f"{session.display_name} interacted with shelf: {prompt}",
                        document=document,
                    )
        return None

    def _load_document_summaries(self) -> list[DocumentSummary]:
        indexed = RagIndexService(self.settings).list_documents()
        if indexed:
            return indexed
        return [summary_from_metadata(metadata) for metadata in self._load_document_metadata()]

    def _load_document_metadata(self) -> list[dict[str, object]]:
        metadata_items: list[dict[str, object]] = []
        for metadata_path in sorted(self.settings.documents_dir.glob("*.metadata.json")):
            source_path = _source_path_for_metadata(metadata_path)
            raw = json.loads(metadata_path.read_text(encoding="utf-8"))
            raw["source_path"] = str(source_path)
            metadata_items.append(raw)
        return metadata_items


class GameSessionStore:
    def __init__(self) -> None:
        self._sessions: dict[str, GameSession] = {}

    def create(self, request: GameSessionCreateRequest, character: GameCharacter) -> GameSession:
        session = GameSession(
            session_id=str(uuid4()),
            user_name=request.user_name,
            display_name=request.display_name,
            character=character,
            position=Position(x=96, y=520),
        )
        self._sessions[session.session_id] = session
        return session

    def get(self, session_id: str) -> GameSession | None:
        return self._sessions.get(session_id)

    def change_character(self, session_id: str, character: GameCharacter) -> GameSession | None:
        session = self._sessions.get(session_id)
        if session is None:
            return None
        updated = session.model_copy(update={"character": character})
        self._sessions[session_id] = updated
        return updated

    def update_position(self, session_id: str, position: Position) -> GameSession | None:
        session = self._sessions.get(session_id)
        if session is None:
            return None
        updated = session.model_copy(update={"position": position})
        self._sessions[session_id] = updated
        return updated


def _source_path_for_metadata(metadata_path: Path) -> Path:
    stem = metadata_path.name.removesuffix(".metadata.json")
    for suffix in (".md", ".csv", ".txt", ".json"):
        candidate = metadata_path.with_name(f"{stem}{suffix}")
        if candidate.exists():
            return candidate
    return metadata_path


def _group_documents_by_flow(documents: list[DocumentSummary]) -> dict[str, list[DocumentSummary]]:
    grouped: dict[str, list[DocumentSummary]] = {}
    for document in documents:
        flow_id = document.room_id or document.business_flow or _flow_for_doc_type(document.doc_type)
        grouped.setdefault(flow_id, []).append(document)
    return grouped


def _flow_for_doc_type(doc_type: str) -> str:
    if doc_type in {"bill_of_lading", "shipment_manifest", "customs_document"}:
        return "shipment_docs"
    if doc_type in {"tracking_event", "incident_report"}:
        return "shipment_exceptions"
    if doc_type == "warehouse_inventory":
        return "warehouse_ops"
    if doc_type in {"customer_sla", "carrier_contract"}:
        return "contracts"
    return "documents"


def _label_for_flow(flow_id: str) -> str:
    labels = {
        "shipment_docs": "Shipment Records",
        "shipment_exceptions": "Exception Desk",
        "warehouse_ops": "Warehouse Room",
        "contracts": "Contract Archive",
        "documents": "Document Vault",
    }
    return labels.get(flow_id, flow_id.replace("_", " ").title())


_CHARACTERS = [
    GameCharacter(
        character_id="mage",
        display_name="Mage Archivist",
        description="Balanced library explorer with walk, spell, and fallback sheets.",
        sprite=CharacterSprite(
            image_url="/assets/sprites/mage-walk.png",
            frame_width=64,
            frame_height=64,
            columns=9,
            rows=4,
            animations=[
                SpriteAnimation(name="down", row=0, frames=9),
                SpriteAnimation(name="left", row=1, frames=9),
                SpriteAnimation(name="right", row=2, frames=9),
                SpriteAnimation(name="up", row=3, frames=9),
            ],
        ),
    ),
    GameCharacter(
        character_id="baldric",
        display_name="Baldric Runner",
        description="Alternative character for testing character switching.",
        sprite=CharacterSprite(
            image_url="/assets/sprites/baldric-walk.png",
            frame_width=64,
            frame_height=64,
            columns=9,
            rows=4,
            animations=[
                SpriteAnimation(name="down", row=0, frames=9),
                SpriteAnimation(name="left", row=1, frames=9),
                SpriteAnimation(name="right", row=2, frames=9),
                SpriteAnimation(name="up", row=3, frames=9),
            ],
        ),
    ),
]
