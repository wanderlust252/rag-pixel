from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_game_world_builds_from_document_metadata() -> None:
    response = client.get("/game/world")

    assert response.status_code == 200
    payload = response.json()
    assert payload["world_id"] == "business_library"
    assert len(payload["portals"]) >= 3
    assert len(payload["shelves"]) >= 6
    assert {shelf["doc_id"] for shelf in payload["shelves"]} >= {
        "BL-2026-0001",
        "INC-2026-0001",
    }


def test_session_create_and_character_change() -> None:
    create_response = client.post(
        "/game/sessions",
        json={
            "user_name": "phase2_user",
            "display_name": "Phase 2 User",
            "character_id": "mage",
        },
    )

    assert create_response.status_code == 200
    session = create_response.json()
    assert session["character"]["character_id"] == "mage"

    change_response = client.patch(
        f"/game/sessions/{session['session_id']}/character",
        json={"character_id": "baldric"},
    )

    assert change_response.status_code == 200
    assert change_response.json()["character"]["character_id"] == "baldric"

    position_response = client.patch(
        f"/game/sessions/{session['session_id']}/position",
        json={"position": {"x": 160, "y": 400}},
    )

    assert position_response.status_code == 200
    assert position_response.json()["position"] == {"x": 160, "y": 400}


def test_character_walk_sheet_rows_match_asset_order() -> None:
    response = client.get("/game/characters")

    assert response.status_code == 200
    for character in response.json()["characters"]:
        rows_by_direction = {
            animation["name"]: animation["row"]
            for animation in character["sprite"]["animations"]
        }
        assert rows_by_direction == {
            "up": 0,
            "left": 1,
            "down": 2,
            "right": 3,
        }


def test_bookshelf_interaction_returns_document_detail() -> None:
    create_response = client.post(
        "/game/sessions",
        json={
            "user_name": "reader_1",
            "display_name": "Reader One",
            "character_id": "mage",
        },
    )
    session = create_response.json()

    interaction_response = client.post(
        "/game/interactions",
        json={
            "session_id": session["session_id"],
            "target_type": "bookshelf",
            "target_id": "BL-2026-0001",
            "question": "Open this file",
        },
    )

    assert interaction_response.status_code == 200
    payload = interaction_response.json()
    assert payload["target_type"] == "bookshelf"
    assert payload["document"]["doc_id"] == "BL-2026-0001"
