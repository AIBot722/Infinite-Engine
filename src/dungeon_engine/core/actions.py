from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class ActionType(str, Enum):
    MOVE = "MOVE"
    ATTACK = "ATTACK"
    PICKUP = "PICKUP"
    USE = "USE"
    WAIT = "WAIT"


@dataclass(frozen=True)
class Action:
    type: ActionType
    payload: Mapping[str, Any] | None = None

    @staticmethod
    def move(direction: str) -> "Action":
        return Action(ActionType.MOVE, {"direction": direction})

    @staticmethod
    def attack() -> "Action":
        return Action(ActionType.ATTACK, {})

    @staticmethod
    def pickup() -> "Action":
        return Action(ActionType.PICKUP, {})

    @staticmethod
    def use(item_id: str) -> "Action":
        return Action(ActionType.USE, {"item_id": item_id})

    @staticmethod
    def wait() -> "Action":
        return Action(ActionType.WAIT, {})
