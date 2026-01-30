from __future__ import annotations

from typing import Any, Dict, List, Mapping

from pydantic import BaseModel, Field


class CreateGameRequest(BaseModel):
    seed: int | None = None
    content_pack: str | None = None


class CreateGameResponse(BaseModel):
    game_id: str
    seed: int


class ActionRequest(BaseModel):
    type: str
    payload: Dict[str, Any] | None = None


class ResetRequest(BaseModel):
    seed: int | None = None


class GameStateResponse(BaseModel):
    state_version: int
    turn: int
    player: Mapping[str, Any]
    stats: Mapping[str, Any]
    view: Mapping[str, Any]
    events: List[Mapping[str, Any]]
    log: List[str]


class MapResponse(BaseModel):
    center: List[int]
    radius: int
    tiles: List[List[Dict[str, Any]]]
    entities: List[Dict[str, Any]]
    items: List[Dict[str, Any]]
    discovered: List[List[bool]]


class HealthResponse(BaseModel):
    ok: bool = Field(default=True)
