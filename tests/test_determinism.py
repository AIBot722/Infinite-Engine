from __future__ import annotations

import json
from pathlib import Path

from dungeon_engine.content.loader import load_content_pack
from dungeon_engine.core.actions import Action
from dungeon_engine.core.engine import Engine


def _state_hash(state) -> str:
    entities = {
        key: {
            "pos": entity.position,
            "hp": entity.stats.hp,
            "max_hp": entity.stats.max_hp,
            "atk": entity.stats.atk,
            "def": entity.stats.defense,
            "xp": entity.stats.xp,
            "lvl": entity.stats.level,
        }
        for key, entity in sorted(state.entities.items())
    }
    items = {
        f"{pos[0]},{pos[1]}": [stack.item_id for stack in stacks]
        for pos, stacks in sorted(state.items_on_ground.items())
    }
    chunks = {
        f"{key[0]},{key[1]}": [[tile.tile_id for tile in row] for row in chunk.tiles]
        for key, chunk in sorted(state.chunks.items())
    }
    payload = {
        "seed": state.seed,
        "turn": state.turn,
        "entities": entities,
        "items": items,
        "chunks": chunks,
        "discovered": sorted(state.discovered.keys()),
    }
    return json.dumps(payload, sort_keys=True)


def test_determinism() -> None:
    content = load_content_pack(Path(__file__).resolve().parents[1] / "content" / "default")
    engine = Engine(content)
    actions = [
        Action.move("E"),
        Action.move("S"),
        Action.attack(),
        Action.wait(),
    ]

    state_a = engine.new_game(123)
    state_b = engine.new_game(123)

    for action in actions:
        engine.run_turn(state_a, action)
        engine.run_turn(state_b, action)

    assert _state_hash(state_a) == _state_hash(state_b)
