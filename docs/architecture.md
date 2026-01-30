# Architecture

## Layers

- **core/**: Pure game model and engine orchestration. No FastAPI/Uvicorn imports.
- **procedural/**: Deterministic chunk generation based on `world_seed + chunk coords`.
- **simulation/**: Turn resolution, combat, AI, and FOV.
- **content/**: JSON content pack loader and schema validation.
- **server/**: FastAPI adapter, session store, and DTOs.
- **utils/**: RNG and grid helpers.

## Data Flow

1. HTTP request hits `server/routes.py`.
2. SessionStore resolves the `GameSession`.
3. `Engine.run_turn` applies the action.
4. State is serialized into a view window for the response.

## Determinism

The game state is fully reproducible with `seed + ordered action history`. All procedural generation and combat randomness rely on a deterministic RNG stored in the game state.
