from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Tuple


Position = Tuple[int, int]


@dataclass
class Stats:
    max_hp: int
    hp: int
    atk: int
    defense: int
    xp: int = 0
    level: int = 1


@dataclass
class EntityState:
    entity_id: str
    name: str
    position: Position
    stats: Stats
    is_player: bool = False
    ai: str | None = None
    inventory: List["ItemStack"] = field(default_factory=list)


@dataclass
class ItemStack:
    item_id: str
    quantity: int = 1


@dataclass
class Tile:
    tile_id: str
    walkable: bool
    transparent: bool


@dataclass
class Chunk:
    chunk_x: int
    chunk_y: int
    tiles: List[List[Tile]]


@dataclass
class GameState:
    seed: int
    rng_state: Any
    turn: int
    player_id: str
    entities: Dict[str, EntityState]
    items_on_ground: Dict[Position, List[ItemStack]]
    chunks: Dict[Tuple[int, int], Chunk]
    discovered: Dict[Position, bool] = field(default_factory=dict)
    event_log: List[str] = field(default_factory=list)
    pending_events: List[Mapping[str, Any]] = field(default_factory=list)

    def clone_event_log(self) -> List[str]:
        return list(self.event_log)
