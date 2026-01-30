from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from dungeon_engine.core.actions import Action, ActionType
from dungeon_engine.core.constants import FOV_RADIUS, STATE_VERSION, VIEW_RADIUS
from dungeon_engine.simulation.fov import visible_positions
from dungeon_engine.server.schemas import (
    ActionRequest,
    CreateGameRequest,
    CreateGameResponse,
    GameStateResponse,
    HealthResponse,
    MapResponse,
    ResetRequest,
)
from dungeon_engine.server.session_store import SessionStore

router = APIRouter()

CONTENT_ROOT = Path(__file__).resolve().parents[3] / "content"
store = SessionStore(CONTENT_ROOT)


def _action_from_request(request: ActionRequest) -> Action:
    try:
        action_type = ActionType(request.type)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Unknown action type") from exc
    return Action(action_type, request.payload or {})


def _view_window(session) -> Dict[str, Any]:
    state = session.state
    engine = session.engine
    player = state.entities[state.player_id]
    visible = visible_positions(player.position, FOV_RADIUS)

    tiles: List[List[Dict[str, Any]]] = []
    discovered_grid: List[List[bool]] = []
    for y in range(player.position[1] - VIEW_RADIUS, player.position[1] + VIEW_RADIUS + 1):
        row: List[Dict[str, Any]] = []
        row_disc: List[bool] = []
        for x in range(player.position[0] - VIEW_RADIUS, player.position[0] + VIEW_RADIUS + 1):
            pos = (x, y)
            is_visible = pos in visible
            discovered = state.discovered.get(pos, False) or is_visible
            row_disc.append(discovered)
            if not discovered:
                row.append({"tile_id": None, "visible": False})
                continue
            tile = engine.get_tile(state, pos)
            tile_def = session.engine.content.tiles[tile.tile_id]
            row.append(
                {
                    "tile_id": tile.tile_id,
                    "visible": is_visible,
                    "sprite_id": tile_def.sprite_id,
                    "ascii": tile_def.ascii,
                    "fg": tile_def.fg_color,
                    "bg": tile_def.bg_color,
                }
            )
        tiles.append(row)
        discovered_grid.append(row_disc)

    entities: List[Dict[str, Any]] = []
    for entity in state.entities.values():
        if entity.position in visible:
            entity_def = session.engine.content.entities[entity.entity_id]
            entities.append(
                {
                    "entity_id": entity.entity_id,
                    "name": entity.name,
                    "position": list(entity.position),
                    "sprite_id": entity_def.sprite_id,
                    "ascii": entity_def.ascii,
                    "fg": entity_def.fg_color,
                    "bg": entity_def.bg_color,
                }
            )

    items: List[Dict[str, Any]] = []
    for pos, stacks in state.items_on_ground.items():
        if pos in visible:
            for item in stacks:
                item_def = session.engine.content.items[item.item_id]
                items.append(
                    {
                        "item_id": item.item_id,
                        "position": list(pos),
                        "sprite_id": item_def.sprite_id,
                        "ascii": item_def.ascii,
                        "fg": item_def.fg_color,
                        "bg": item_def.bg_color,
                    }
                )

    return {
        "center": list(player.position),
        "radius": VIEW_RADIUS,
        "tiles": tiles,
        "entities": entities,
        "items": items,
        "discovered": discovered_grid,
    }


@router.get("/healthz", response_model=HealthResponse)
def healthz() -> HealthResponse:
    return HealthResponse()


@router.post("/games", response_model=CreateGameResponse)
def create_game(request: CreateGameRequest) -> CreateGameResponse:
    seed = request.seed or 12345
    content_pack = request.content_pack or "default"
    session = store.create_game(seed, content_pack)
    return CreateGameResponse(game_id=session.game_id, seed=session.state.seed)


@router.get("/games/{game_id}", response_model=GameStateResponse)
def get_game(game_id: str) -> GameStateResponse:
    try:
        session = store.get(game_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Game not found") from exc

    state = session.state
    player = state.entities[state.player_id]
    view = _view_window(session)
    stats = {
        "hp": player.stats.hp,
        "max_hp": player.stats.max_hp,
        "atk": player.stats.atk,
        "defense": player.stats.defense,
        "xp": player.stats.xp,
        "level": player.stats.level,
    }
    return GameStateResponse(
        state_version=STATE_VERSION,
        turn=state.turn,
        player={"id": player.entity_id, "position": list(player.position)},
        stats=stats,
        view=view,
        events=state.pending_events,
        log=state.clone_event_log(),
    )


@router.post("/games/{game_id}/action", response_model=GameStateResponse)
def action(game_id: str, request: ActionRequest) -> GameStateResponse:
    try:
        session = store.get(game_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Game not found") from exc
    action_obj = _action_from_request(request)
    session.engine.run_turn(session.state, action_obj)
    return get_game(game_id)


@router.post("/games/{game_id}/reset", response_model=CreateGameResponse)
def reset(game_id: str, request: ResetRequest) -> CreateGameResponse:
    try:
        session = store.reset(game_id, request.seed)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Game not found") from exc
    return CreateGameResponse(game_id=session.game_id, seed=session.state.seed)


@router.get("/games/{game_id}/map", response_model=MapResponse)
def map_view(game_id: str) -> MapResponse:
    try:
        session = store.get(game_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Game not found") from exc
    view = _view_window(session)
    return MapResponse(**view)
