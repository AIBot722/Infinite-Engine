# Decisions (ADR-lite)

## FastAPI + Uvicorn
FastAPI provides a minimal, typed HTTP layer with async-ready routing. Uvicorn is lightweight and production-friendly.

## Determinism
All randomness is derived from a deterministic RNG stored in the game state. Chunk generation uses `world_seed + chunk coords` hashing.

## Chunk Size
Chunks are fixed at 32x32 for predictable layout and manageable caching.

## FOV
We use Manhattan-radius visibility for a deterministic and inexpensive fog-of-war implementation.

## Progression
XP-based leveling increases HP/ATK/DEF based on `balance.json`. This avoids loot-only scaling and keeps the RPG loop clear.
