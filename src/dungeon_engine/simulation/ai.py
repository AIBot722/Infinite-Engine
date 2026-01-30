from __future__ import annotations

from dataclasses import dataclass

from dungeon_engine.utils.grid import DIRECTIONS
from dungeon_engine.utils.rng import RNG

Position = tuple[int, int]


@dataclass(frozen=True)
class AiAction:
    type: str
    direction: str | None = None


def decide_action(npc_pos: Position, player_pos: Position, rng: RNG) -> AiAction:
    dx = player_pos[0] - npc_pos[0]
    dy = player_pos[1] - npc_pos[1]
    distance = abs(dx) + abs(dy)

    if distance <= 6:
        if abs(dx) > abs(dy):
            direction = "E" if dx > 0 else "W"
        elif dy != 0:
            direction = "S" if dy > 0 else "N"
        else:
            direction = None
        return AiAction("move", direction)

    direction = rng.choice(list(DIRECTIONS.keys()))
    return AiAction("move", direction)
