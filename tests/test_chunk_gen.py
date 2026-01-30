from __future__ import annotations

from dungeon_engine.procedural.chunk_gen import generate_chunk
from dungeon_engine.core.constants import CHUNK_SIZE


def test_chunk_determinism() -> None:
    chunk_a = generate_chunk(42, 0, 0, CHUNK_SIZE)
    chunk_b = generate_chunk(42, 0, 0, CHUNK_SIZE)
    assert [tile.tile_id for tile in chunk_a.tiles[0]] == [
        tile.tile_id for tile in chunk_b.tiles[0]
    ]


def test_chunk_edge_consistency() -> None:
    chunk_a = generate_chunk(42, 0, 0, CHUNK_SIZE)
    chunk_b = generate_chunk(42, 1, 0, CHUNK_SIZE)
    east_tile = chunk_a.tiles[CHUNK_SIZE // 2][CHUNK_SIZE - 1].tile_id
    west_tile = chunk_b.tiles[CHUNK_SIZE // 2][0].tile_id
    assert (east_tile == "door") == (west_tile == "door")
