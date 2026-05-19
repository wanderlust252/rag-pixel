import logging
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.game.schemas import (
    GameCharacterChangeRequest,
    GameCharacterListResponse,
    GameInteractionRequest,
    GameInteractionResponse,
    GamePositionUpdateRequest,
    GameSession,
    GameSessionCreateRequest,
    GameWorldResponse,
)
from app.game.service import GameService, GameSessionStore
from app.rag.index import RagIndexService
from app.rag.ingest import RagIngestService
from app.rag.query import RagQueryService
from app.rag.schemas import (
    ClearDocumentsResponse,
    ClearIndexResponse,
    DocumentDetail,
    DocumentListResponse,
    DocumentUploadResponse,
    HealthResponse,
    IngestResponse,
    QueryRequest,
    QueryResponse,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

settings = get_settings()
app = FastAPI(title=settings.app_name)
game_sessions = GameSessionStore()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/documents/ingest", response_model=IngestResponse)
def ingest_documents() -> IngestResponse:
    documents = RagIngestService(settings).load_documents()
    RagIndexService(settings).build_and_persist(documents)
    return IngestResponse(ingested_documents=len(documents), index_persisted=True)


@app.post("/documents/upload", response_model=DocumentUploadResponse)
async def upload_document(
    file: Annotated[UploadFile, File()],
    doc_id: Annotated[str, Form()],
    doc_type: Annotated[str, Form()],
    title: Annotated[str, Form()],
    business_flow: Annotated[str | None, Form()] = None,
    room_id: Annotated[str | None, Form()] = None,
    shelf_id: Annotated[str | None, Form()] = None,
    shipment_id: Annotated[str | None, Form()] = None,
    customer: Annotated[str | None, Form()] = None,
    carrier: Annotated[str | None, Form()] = None,
    warehouse: Annotated[str | None, Form()] = None,
    route: Annotated[str | None, Form()] = None,
    date: Annotated[str | None, Form()] = None,
    source_type: Annotated[str | None, Form()] = None,
    overwrite: Annotated[bool, Form()] = False,
    reindex: Annotated[bool, Form()] = True,
) -> DocumentUploadResponse:
    metadata = {
        "doc_id": doc_id,
        "doc_type": doc_type,
        "title": title,
        "business_flow": business_flow,
        "room_id": room_id,
        "shelf_id": shelf_id,
        "shipment_id": shipment_id,
        "customer": customer,
        "carrier": carrier,
        "warehouse": warehouse,
        "route": route,
        "date": date,
        "source_type": source_type,
    }

    ingest_service = RagIngestService(settings)
    try:
        document = ingest_service.save_uploaded_document(
            filename=file.filename or "",
            content=await file.read(),
            metadata=metadata,
            overwrite=overwrite,
        )
    except FileExistsError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    ingested_documents = None
    if reindex:
        documents = ingest_service.load_documents()
        RagIndexService(settings).build_and_persist(documents)
        ingested_documents = len(documents)

    return DocumentUploadResponse(
        document=document,
        index_persisted=reindex,
        ingested_documents=ingested_documents,
    )


@app.delete("/documents/index", response_model=ClearIndexResponse)
def clear_document_index() -> ClearIndexResponse:
    index_cleared = RagIndexService(settings).clear()
    return ClearIndexResponse(index_cleared=index_cleared)


@app.delete("/documents", response_model=ClearDocumentsResponse)
def clear_documents() -> ClearDocumentsResponse:
    documents_removed, metadata_removed = RagIngestService(settings).clear_source_documents()
    index_cleared = RagIndexService(settings).clear()
    return ClearDocumentsResponse(
        documents_removed=documents_removed,
        metadata_removed=metadata_removed,
        index_cleared=index_cleared,
    )


@app.get("/documents", response_model=DocumentListResponse)
def list_documents() -> DocumentListResponse:
    documents = RagIndexService(settings).list_documents()
    return DocumentListResponse(documents=documents)


@app.get("/documents/{doc_id}", response_model=DocumentDetail)
def get_document(doc_id: str) -> DocumentDetail:
    document = RagIndexService(settings).get_document(doc_id)
    if document is None:
        raise HTTPException(status_code=404, detail=f"Document {doc_id} was not found")
    return document


@app.post("/rag/query", response_model=QueryResponse)
def query_rag(request: QueryRequest) -> QueryResponse:
    return RagQueryService(settings).query(request)


@app.get("/game/characters", response_model=GameCharacterListResponse)
def list_game_characters() -> GameCharacterListResponse:
    return GameCharacterListResponse(characters=GameService(settings).list_characters())


@app.get("/game/world", response_model=GameWorldResponse)
def get_game_world() -> GameWorldResponse:
    return GameService(settings).get_world()


@app.post("/game/sessions", response_model=GameSession)
def create_game_session(request: GameSessionCreateRequest) -> GameSession:
    game_service = GameService(settings)
    character = game_service.get_character(request.character_id)
    if character is None:
        raise HTTPException(status_code=404, detail=f"Character {request.character_id} was not found")
    return game_sessions.create(request, character)


@app.get("/game/sessions/{session_id}", response_model=GameSession)
def get_game_session(session_id: str) -> GameSession:
    session = game_sessions.get(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session {session_id} was not found")
    return session


@app.patch("/game/sessions/{session_id}/character", response_model=GameSession)
def change_game_character(
    session_id: str,
    request: GameCharacterChangeRequest,
) -> GameSession:
    game_service = GameService(settings)
    character = game_service.get_character(request.character_id)
    if character is None:
        raise HTTPException(status_code=404, detail=f"Character {request.character_id} was not found")

    session = game_sessions.change_character(session_id, character)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session {session_id} was not found")
    return session


@app.patch("/game/sessions/{session_id}/position", response_model=GameSession)
def update_game_position(
    session_id: str,
    request: GamePositionUpdateRequest,
) -> GameSession:
    session = game_sessions.update_position(session_id, request.position)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session {session_id} was not found")
    return session


@app.post("/game/interactions", response_model=GameInteractionResponse)
def interact_with_game_target(request: GameInteractionRequest) -> GameInteractionResponse:
    session = game_sessions.get(request.session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session {request.session_id} was not found")

    interaction = GameService(settings).interact(
        session=session,
        target_type=request.target_type,
        target_id=request.target_id,
        question=request.question,
    )
    if interaction is None:
        raise HTTPException(status_code=404, detail=f"Target {request.target_id} was not found")
    return interaction
