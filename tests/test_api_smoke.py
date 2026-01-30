from __future__ import annotations

from fastapi.testclient import TestClient

from dungeon_engine.server.app import create_app


def test_api_smoke() -> None:
    client = TestClient(create_app())

    response = client.post("/api/v1/games", json={"seed": 111})
    assert response.status_code == 200
    game_id = response.json()["game_id"]

    response = client.get(f"/api/v1/games/{game_id}")
    assert response.status_code == 200

    response = client.post(
        f"/api/v1/games/{game_id}/action",
        json={"type": "MOVE", "payload": {"direction": "E"}},
    )
    assert response.status_code == 200
