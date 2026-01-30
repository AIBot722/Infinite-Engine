from __future__ import annotations

import json
from pathlib import Path

from dungeon_engine.content.schemas import BalanceDef, ContentPack, EntityDef, ItemDef, TileDef


class ContentError(RuntimeError):
    pass


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ContentError(f"Missing content file: {path}") from exc


def load_content_pack(base_path: Path) -> ContentPack:
    tiles_raw = _load_json(base_path / "tiles.json")
    entities_raw = _load_json(base_path / "entities.json")
    items_raw = _load_json(base_path / "items.json")
    balance_raw = _load_json(base_path / "balance.json")

    tiles = {
        tile["tile_id"]: TileDef(**tile)
        for tile in tiles_raw.get("tiles", [])
    }
    entities = {
        entity["entity_id"]: EntityDef(**entity)
        for entity in entities_raw.get("entities", [])
    }
    items = {
        item["item_id"]: ItemDef(**item)
        for item in items_raw.get("items", [])
    }
    balance = BalanceDef(**balance_raw)

    if "player" not in entities:
        raise ContentError("Content pack must define a player entity")

    return ContentPack(tiles=tiles, entities=entities, items=items, balance=balance)
