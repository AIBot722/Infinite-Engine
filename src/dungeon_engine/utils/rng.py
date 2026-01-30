from __future__ import annotations

import random
from typing import Iterable, TypeVar

T = TypeVar("T")


class RNG:
    def __init__(self, seed: int, state: object | None = None) -> None:
        self._random = random.Random(seed)
        if state is not None:
            self._random.setstate(state)

    @property
    def state(self) -> object:
        return self._random.getstate()

    def randint(self, a: int, b: int) -> int:
        return self._random.randint(a, b)

    def choice(self, items: Iterable[T]) -> T:
        seq = list(items)
        if not seq:
            raise ValueError("choice requires at least one item")
        return self._random.choice(seq)

    def random(self) -> float:
        return self._random.random()
