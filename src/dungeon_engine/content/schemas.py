from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class TileDef:
    tile_id: str
    walkable: bool
    transparent: bool
    sprite_id: str
    fg_color: str
    bg_color: str
    ascii: str


@dataclass(frozen=True)
class EntityDef:
    entity_id: str
    name: str
    base_hp: int
    base_atk: int
    base_def: int
    xp: int
    sprite_id: str
    fg_color: str
    bg_color: str
    ascii: str
    ai: str | None = None


@dataclass(frozen=True)
class ItemDef:
    item_id: str
    name: str
    effect: str
    power: int
    sprite_id: str
    fg_color: str
    bg_color: str
    ascii: str


@dataclass(frozen=True)
class BalanceDef:
    xp_table: List[int]
    level_up_hp: int
    level_up_atk: int
    level_up_def: int


@dataclass(frozen=True)
class ContentPack:
    tiles: Dict[str, TileDef]
    entities: Dict[str, EntityDef]
    items: Dict[str, ItemDef]
    balance: BalanceDef
