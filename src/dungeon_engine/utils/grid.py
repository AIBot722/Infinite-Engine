from __future__ import annotations

import math
from typing import Iterable, Iterator, Tuple

from dungeon_engine.core.constants import CHUNK_SIZE

Position = Tuple[int, int]

DIRECTIONS = {
    "N": (0, -1),
    "S": (0, 1),
    "W": (-1, 0),
    "E": (1, 0),
}


def add_pos(a: Position, b: Position) -> Position:
    return a[0] + b[0], a[1] + b[1]


def chunk_coords(position: Position) -> Tuple[int, int]:
    x, y = position
    return math.floor(x / CHUNK_SIZE), math.floor(y / CHUNK_SIZE)


def local_coords(position: Position) -> Tuple[int, int]:
    cx, cy = chunk_coords(position)
    return position[0] - cx * CHUNK_SIZE, position[1] - cy * CHUNK_SIZE


def iter_positions(center: Position, radius: int) -> Iterator[Position]:
    cx, cy = center
    for y in range(cy - radius, cy + radius + 1):
        for x in range(cx - radius, cx + radius + 1):
            yield x, y


def neighbors(position: Position) -> Iterable[Position]:
    for delta in DIRECTIONS.values():
        yield add_pos(position, delta)
