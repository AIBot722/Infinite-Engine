# Infinite Dungeon Crawler Engine (Headless)

**Quickstart (local)**

```bash
make install
make run
```

**Quickstart (Docker)**

```bash
docker build -t infinite-engine .
docker run -p 8000:8000 infinite-engine
```

**API Examples**

```bash
curl -s -X POST http://localhost:8000/api/v1/games \
  -H "Content-Type: application/json" \
  -d '{"seed": 12345}'
```

```bash
curl -s http://localhost:8000/api/v1/games/<GAME_ID>
```

```bash
curl -s -X POST http://localhost:8000/api/v1/games/<GAME_ID>/action \
  -H "Content-Type: application/json" \
  -d '{"type": "MOVE", "payload": {"direction": "E"}}'
```

## Developer Experience

- `make install` sets up a local virtualenv and installs dependencies.
- `make test` runs pytest.
- `make lint` runs ruff.
- `make fmt` formats with ruff.
- `make run` runs the FastAPI server on port 8000.

## Documentation

- [Architecture](docs/architecture.md)
- [API](docs/api.md)
- [Content Packs](docs/content_packs.md)
- [Decisions](docs/decisions.md)
- [AI Guide](docs/ai_guide.md)
