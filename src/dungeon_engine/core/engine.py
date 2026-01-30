from __future__ import annotations

from pathlib import Path

from dungeon_engine.content.loader import load_content_pack
from dungeon_engine.content.schemas import ContentPack
from dungeon_engine.core.constants import CHUNK_SIZE, EVENT_LOG_LIMIT, FOV_RADIUS
from dungeon_engine.core.state import Chunk, EntityState, GameState, ItemStack, Stats, Tile
from dungeon_engine.procedural.chunk_gen import generate_chunk
from dungeon_engine.simulation.fov import visible_positions
from dungeon_engine.simulation.turn import run_turn
from dungeon_engine.utils.grid import chunk_coords
from dungeon_engine.utils.rng import RNG


class Engine:
    def __init__(self, content_pack: ContentPack) -> None:
        self.content = content_pack

    @staticmethod
    def load_content(content_root: Path, pack_name: str) -> ContentPack:
        return load_content_pack(content_root / pack_name)

    def new_game(self, seed: int) -> GameState:
        rng = RNG(seed)
        player_def = self.content.entities["player"]
        player = EntityState(
            entity_id="player",
            name=player_def.name,
            position=(0, 0),
            stats=Stats(
                max_hp=player_def.base_hp,
                hp=player_def.base_hp,
                atk=player_def.base_atk,
                defense=player_def.base_def,
            ),
            is_player=True,
        )
        state = GameState(
            seed=seed,
            rng_state=rng.state,
            turn=0,
            player_id="player",
            entities={"player": player},
            items_on_ground={},
            chunks={},
        )
        start_chunk = self.ensure_chunk(state, 0, 0)
        local_x = player.position[0] - 0 * CHUNK_SIZE
        local_y = player.position[1] - 0 * CHUNK_SIZE
        start_chunk.tiles[local_y][local_x] = Tile("floor", True, True)
        self._spawn_initial_entities(state)
        visible = visible_positions(player.position, FOV_RADIUS)
        for pos in visible:
            state.discovered[pos] = True
        state.rng_state = rng.state
        return state

    def _spawn_initial_entities(self, state: GameState) -> None:
        npc_ids = ["rat", "slime", "skeleton"]
        positions = [(2, 1), (3, -2), (-2, 2)]
        for idx, npc_id in enumerate(npc_ids):
            npc_def = self.content.entities[npc_id]
            position = positions[idx]
            cx, cy = chunk_coords(position)
            chunk = self.ensure_chunk(state, cx, cy)
            local_x = position[0] - cx * CHUNK_SIZE
            local_y = position[1] - cy * CHUNK_SIZE
            chunk.tiles[local_y][local_x] = Tile("floor", True, True)
            state.entities[npc_id] = EntityState(
                entity_id=npc_id,
                name=npc_def.name,
                position=position,
                stats=Stats(
                    max_hp=npc_def.base_hp,
                    hp=npc_def.base_hp,
                    atk=npc_def.base_atk,
                    defense=npc_def.base_def,
                ),
                ai=npc_def.ai,
            )
        state.items_on_ground[(1, 0)] = [ItemStack("potion", 1)]
        state.items_on_ground[(0, 2)] = [ItemStack("gold", 5)]
        state.items_on_ground[(2, 0)] = [ItemStack("weapon", 1)]

    def ensure_chunk(self, state: GameState, chunk_x: int, chunk_y: int) -> Chunk:
        key = (chunk_x, chunk_y)
        if key not in state.chunks:
            state.chunks[key] = generate_chunk(state.seed, chunk_x, chunk_y, CHUNK_SIZE)
        return state.chunks[key]

    def get_tile(self, state: GameState, position: tuple[int, int]):
        cx, cy = chunk_coords(position)
        chunk = self.ensure_chunk(state, cx, cy)
        local_x = position[0] - cx * CHUNK_SIZE
        local_y = position[1] - cy * CHUNK_SIZE
        return chunk.tiles[local_y][local_x]

    def is_walkable(self, state: GameState, position: tuple[int, int]) -> bool:
        tile = self.get_tile(state, position)
        if not tile.walkable:
            return False
        for entity in state.entities.values():
            if entity.position == position:
                return False
        return True

    def run_turn(self, state: GameState, action) -> None:
        rng = RNG(state.seed, state.rng_state)
        events = run_turn(state, action, self.content, rng, self)
        state.rng_state = rng.state
        state.turn += 1
        state.pending_events = [event.payload | {"type": event.type} for event in events]
        for event in events:
            state.event_log.append(f"{event.type}: {event.payload}")
        if len(state.event_log) > EVENT_LOG_LIMIT:
            state.event_log = state.event_log[-EVENT_LOG_LIMIT:]
