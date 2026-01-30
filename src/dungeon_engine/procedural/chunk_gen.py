from __future__ import annotations

import hashlib
from typing import List, Tuple

from dungeon_engine.core.state import Chunk, Tile
from dungeon_engine.procedural.rooms import Room
from dungeon_engine.utils.rng import RNG

Position = Tuple[int, int]


def stable_seed(*parts: object) -> int:
    data = "|".join(str(part) for part in parts).encode("utf-8")
    digest = hashlib.sha256(data).hexdigest()
    return int(digest[:16], 16)


def carve_room(tiles: List[List[Tile]], room: Room) -> None:
    for y in range(room.y1, room.y2 + 1):
        for x in range(room.x1, room.x2 + 1):
            tiles[y][x] = Tile("floor", True, True)


def carve_corridor(tiles: List[List[Tile]], start: Position, end: Position) -> None:
    x1, y1 = start
    x2, y2 = end
    if x1 == x2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            tiles[y][x1] = Tile("floor", True, True)
    elif y1 == y2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            tiles[y1][x] = Tile("floor", True, True)
    else:
        if abs(x2 - x1) > abs(y2 - y1):
            carve_corridor(tiles, (x1, y1), (x2, y1))
            carve_corridor(tiles, (x2, y1), (x2, y2))
        else:
            carve_corridor(tiles, (x1, y1), (x1, y2))
            carve_corridor(tiles, (x1, y2), (x2, y2))


def edge_opening(world_seed: int, ax: int, ay: int, bx: int, by: int) -> bool:
    seed = stable_seed("edge", world_seed, min(ax, bx), min(ay, by), max(ax, bx), max(ay, by))
    rng = RNG(seed)
    return rng.random() < 0.7


def generate_chunk(world_seed: int, chunk_x: int, chunk_y: int, size: int) -> Chunk:
    rng = RNG(stable_seed("chunk", world_seed, chunk_x, chunk_y))
    tiles: List[List[Tile]] = [
        [Tile("wall", False, False) for _ in range(size)] for _ in range(size)
    ]

    rooms: List[Room] = []
    room_count = rng.randint(4, 7)
    for _ in range(room_count):
        width = rng.randint(5, 9)
        height = rng.randint(5, 9)
        x1 = rng.randint(1, size - width - 2)
        y1 = rng.randint(1, size - height - 2)
        room = Room(x1, y1, x1 + width, y1 + height)
        if any(room.intersects(existing) for existing in rooms):
            continue
        carve_room(tiles, room)
        if rooms:
            carve_corridor(tiles, rooms[-1].center, room.center)
        rooms.append(room)

    if not rooms:
        center_room = Room(size // 2 - 3, size // 2 - 3, size // 2 + 3, size // 2 + 3)
        carve_room(tiles, center_room)
        rooms.append(center_room)

    center = rooms[0].center

    openings = {
        "W": edge_opening(world_seed, chunk_x, chunk_y, chunk_x - 1, chunk_y),
        "E": edge_opening(world_seed, chunk_x, chunk_y, chunk_x + 1, chunk_y),
        "N": edge_opening(world_seed, chunk_x, chunk_y, chunk_x, chunk_y - 1),
        "S": edge_opening(world_seed, chunk_x, chunk_y, chunk_x, chunk_y + 1),
    }
    edge_positions = {
        "W": (0, size // 2),
        "E": (size - 1, size // 2),
        "N": (size // 2, 0),
        "S": (size // 2, size - 1),
    }
    for direction, open_edge in openings.items():
        if not open_edge:
            continue
        ex, ey = edge_positions[direction]
        tiles[ey][ex] = Tile("door", True, True)
        carve_corridor(tiles, center, (ex, ey))

    return Chunk(chunk_x=chunk_x, chunk_y=chunk_y, tiles=tiles)
