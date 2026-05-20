import json

from fastapi.testclient import TestClient

import app.main as main
from app.config import Settings


client = TestClient(main.app)


def test_game_world_builds_from_document_metadata(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(documents_dir=tmp_path / "documents", index_dir=tmp_path / "index")
    _write_document_fixture(main.settings.documents_dir)

    try:
        response = client.get("/game/world")
    finally:
        main.settings = original_settings

    assert response.status_code == 200
    payload = response.json()
    assert payload["world_id"] == "business_library"
    assert len(payload["portals"]) == 2
    assert len(payload["shelves"]) == 2
    assert {shelf["doc_id"] for shelf in payload["shelves"]} >= {
        "BL-2026-0001",
        "INC-2026-0001",
    }


def test_game_session_routes_are_client_owned() -> None:
    assert client.get("/game/characters").status_code == 404
    assert client.post("/game/sessions", json={}).status_code == 404


def test_bookshelf_interaction_returns_document_detail(tmp_path) -> None:
    original_settings = main.settings
    main.settings = Settings(documents_dir=tmp_path / "documents", index_dir=tmp_path / "index")
    _write_document_fixture(main.settings.documents_dir)

    try:
        interaction_response = client.post(
            "/game/interactions",
            json={
                "target_type": "bookshelf",
                "target_id": "BL-2026-0001",
                "question": "Open this file",
            },
        )
    finally:
        main.settings = original_settings

    assert interaction_response.status_code == 200
    payload = interaction_response.json()
    assert payload["target_type"] == "bookshelf"
    assert payload["document"]["doc_id"] == "BL-2026-0001"


def _write_document_fixture(document_dir) -> None:
    document_dir.mkdir(parents=True, exist_ok=True)
    fixtures = [
        (
            "bill_of_lading_sample",
            "Bill of lading",
            {
                "doc_id": "BL-2026-0001",
                "doc_type": "bill_of_lading",
                "title": "Bill of Lading BL-2026-0001",
            },
        ),
        (
            "incident_report",
            "Incident report",
            {
                "doc_id": "INC-2026-0001",
                "doc_type": "incident_report",
                "title": "Incident Report INC-2026-0001",
            },
        ),
    ]

    for stem, content, metadata in fixtures:
        (document_dir / f"{stem}.md").write_text(content, encoding="utf-8")
        (document_dir / f"{stem}.metadata.json").write_text(
            json.dumps(metadata),
            encoding="utf-8",
        )
