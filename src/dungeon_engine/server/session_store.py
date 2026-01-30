from __future__ import annotations

import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Dict

from dungeon_engine.core.engine import Engine
from dungeon_engine.core.state import GameState


@dataclass
class GameSession:
    game_id: str
    engine: Engine
    state: GameState
    content_pack: str


class SessionStore:
    def __init__(self, content_root: Path) -> None:
        self._content_root = content_root
        self._sessions: Dict[str, GameSession] = {}

    def create_game(self, seed: int, content_pack: str) -> GameSession:
        engine = Engine(Engine.load_content(self._content_root, content_pack))
        state = engine.new_game(seed)
        game_id = str(uuid.uuid4())
        session = GameSession(game_id=game_id, engine=engine, state=state, content_pack=content_pack)
        self._sessions[game_id] = session
        return session

    def get(self, game_id: str) -> GameSession:
        return self._sessions[game_id]

    def reset(self, game_id: str, seed: int | None = None) -> GameSession:
        session = self._sessions[game_id]
        new_seed = seed if seed is not None else session.state.seed
        session.state = session.engine.new_game(new_seed)
        return session
