from __future__ import annotations

from typing import Iterable, Set, Tuple

from dungeon_engine.utils.grid import iter_positions

Position = Tuple[int, int]


def visible_positions(center: Position, radius: int) -> Set[Position]:
    visible: Set[Position] = set()
    cx, cy = center
    for x, y in iter_positions(center, radius):
        if abs(x - cx) + abs(y - cy) <= radius:
            visible.add((x, y))
    return visible
