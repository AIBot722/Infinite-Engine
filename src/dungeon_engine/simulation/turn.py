from __future__ import annotations

from typing import List

from dungeon_engine.content.schemas import ContentPack
from dungeon_engine.core.actions import Action, ActionType
from dungeon_engine.core.constants import FOV_RADIUS
from dungeon_engine.core.events import Event
from dungeon_engine.core.state import EntityState, GameState
from dungeon_engine.simulation.ai import decide_action
from dungeon_engine.simulation.combat import apply_level_ups, resolve_attack
from dungeon_engine.simulation.fov import visible_positions
from dungeon_engine.utils.grid import DIRECTIONS, add_pos
from dungeon_engine.utils.rng import RNG


def _entity_at(state: GameState, position: tuple[int, int]) -> EntityState | None:
    for entity in state.entities.values():
        if entity.position == position:
            return entity
    return None


def _move_entity(state: GameState, entity: EntityState, new_pos: tuple[int, int]) -> None:
    entity.position = new_pos


def _pickup_items(state: GameState, entity: EntityState) -> List[Event]:
    items = state.items_on_ground.get(entity.position)
    if not items:
        return [Event("pickup", {"result": "nothing"})]
    entity.inventory.extend(items)
    state.items_on_ground.pop(entity.position, None)
    return [Event("pickup", {"items": [item.item_id for item in items]})]


def _use_item(state: GameState, entity: EntityState, item_id: str, content: ContentPack) -> List[Event]:
    for item in entity.inventory:
        if item.item_id == item_id:
            entity.inventory.remove(item)
            item_def = content.items[item_id]
            if item_def.effect == "heal":
                entity.stats.hp = min(entity.stats.max_hp, entity.stats.hp + item_def.power)
                return [Event("use", {"item": item_id, "hp": entity.stats.hp})]
            if item_def.effect == "atk":
                entity.stats.atk += item_def.power
                return [Event("use", {"item": item_id, "atk": entity.stats.atk})]
            return [Event("use", {"item": item_id})]
    return [Event("use", {"item": item_id, "result": "missing"})]


def _attack_adjacent(state: GameState, attacker: EntityState, content: ContentPack, rng: RNG) -> List[Event]:
    events: List[Event] = []
    for delta in DIRECTIONS.values():
        target_pos = add_pos(attacker.position, delta)
        target = _entity_at(state, target_pos)
        if target and target.entity_id != attacker.entity_id:
            events.extend(resolve_attack(state, attacker, target, content, rng))
            if target.stats.hp <= 0:
                state.entities.pop(target.entity_id, None)
            return events
    return [Event("combat", {"result": "no_target"})]


def _update_fov(state: GameState) -> None:
    player = state.entities[state.player_id]
    visible = visible_positions(player.position, FOV_RADIUS)
    for pos in visible:
        state.discovered[pos] = True


def run_turn(
    state: GameState,
    action: Action,
    content: ContentPack,
    rng: RNG,
    engine,
) -> List[Event]:
    events: List[Event] = []
    player = state.entities[state.player_id]

    if action.type == ActionType.MOVE:
        direction = (action.payload or {}).get("direction")
        if direction in DIRECTIONS:
            new_pos = add_pos(player.position, DIRECTIONS[direction])
            if engine.is_walkable(state, new_pos):
                _move_entity(state, player, new_pos)
                events.append(Event("move", {"entity": player.entity_id, "to": new_pos}))
            else:
                events.append(Event("move", {"entity": player.entity_id, "result": "blocked"}))
    elif action.type == ActionType.ATTACK:
        events.extend(_attack_adjacent(state, player, content, rng))
    elif action.type == ActionType.PICKUP:
        events.extend(_pickup_items(state, player))
    elif action.type == ActionType.USE:
        item_id = (action.payload or {}).get("item_id", "")
        if item_id:
            events.extend(_use_item(state, player, item_id, content))
    elif action.type == ActionType.WAIT:
        events.append(Event("wait", {"entity": player.entity_id}))

    for entity in list(state.entities.values()):
        if entity.is_player:
            continue
        if abs(entity.position[0] - player.position[0]) + abs(entity.position[1] - player.position[1]) == 1:
            events.extend(resolve_attack(state, entity, player, content, rng))
            continue
        ai_action = decide_action(entity.position, player.position, rng)
        if ai_action.type == "move" and ai_action.direction in DIRECTIONS:
            new_pos = add_pos(entity.position, DIRECTIONS[ai_action.direction])
            if engine.is_walkable(state, new_pos):
                _move_entity(state, entity, new_pos)
                events.append(Event("move", {"entity": entity.entity_id, "to": new_pos}))

    apply_level_ups(state, content, events)
    _update_fov(state)
    return events
