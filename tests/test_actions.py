from __future__ import annotations

from pathlib import Path

from dungeon_engine.content.loader import load_content_pack
from dungeon_engine.core.actions import Action
from dungeon_engine.core.engine import Engine


def test_actions_flow() -> None:
    content = load_content_pack(Path(__file__).resolve().parents[1] / "content" / "default")
    engine = Engine(content)
    state = engine.new_game(321)

    start_pos = state.entities[state.player_id].position
    moved = False
    for direction in ["E", "W", "N", "S"]:
        new_pos = (
            start_pos[0] + (direction == "E") - (direction == "W"),
            start_pos[1] + (direction == "S") - (direction == "N"),
        )
        if engine.is_walkable(state, new_pos):
            engine.run_turn(state, Action.move(direction))
            moved = True
            break
    assert moved is True
    moved_pos = state.entities[state.player_id].position
    assert moved_pos != start_pos

    engine.run_turn(state, Action.pickup())
    engine.run_turn(state, Action.use("potion"))

    engine.run_turn(state, Action.attack())
    assert state.turn >= 4
