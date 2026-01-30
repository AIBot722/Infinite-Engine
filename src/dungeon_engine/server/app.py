from __future__ import annotations

from fastapi import FastAPI

from dungeon_engine.server.routes import router


def create_app() -> FastAPI:
    app = FastAPI(title="Infinite Dungeon Crawler Engine", version="0.1.0")
    app.include_router(router, prefix="/api/v1")
    return app


app = create_app()
