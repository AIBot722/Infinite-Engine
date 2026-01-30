from __future__ import annotations

from typing import List

from dungeon_engine.content.schemas import ContentPack
from dungeon_engine.core.events import Event
from dungeon_engine.core.state import EntityState, GameState
from dungeon_engine.utils.rng import RNG


def resolve_attack(
    state: GameState,
    attacker: EntityState,
    defender: EntityState,
    content: ContentPack,
    rng: RNG,
) -> List[Event]:
    events: List[Event] = []
    damage = max(1, attacker.stats.atk - defender.stats.defense + rng.randint(0, 2))
    defender.stats.hp -= damage
    events.append(
        Event(
            "combat",
            {
                "attacker": attacker.entity_id,
                "defender": defender.entity_id,
                "damage": damage,
                "defender_hp": defender.stats.hp,
            },
        )
    )
    if defender.stats.hp <= 0:
        events.append(Event("defeat", {"entity_id": defender.entity_id}))
        if defender.entity_id != state.player_id:
            xp_gain = content.entities[defender.entity_id].xp
            player = state.entities[state.player_id]
            player.stats.xp += xp_gain
            events.append(Event("xp", {"amount": xp_gain, "total": player.stats.xp}))
    return events


def apply_level_ups(state: GameState, content: ContentPack, events: List[Event]) -> None:
    player = state.entities[state.player_id]
    xp_table = content.balance.xp_table
    leveled = False
    while player.stats.level - 1 < len(xp_table) and player.stats.xp >= xp_table[player.stats.level - 1]:
        player.stats.level += 1
        player.stats.max_hp += content.balance.level_up_hp
        player.stats.hp = player.stats.max_hp
        player.stats.atk += content.balance.level_up_atk
        player.stats.defense += content.balance.level_up_def
        leveled = True
    if leveled:
        events.append(
            Event(
                "levelup",
                {
                    "level": player.stats.level,
                    "max_hp": player.stats.max_hp,
                    "atk": player.stats.atk,
                    "defense": player.stats.defense,
                },
            )
        )
