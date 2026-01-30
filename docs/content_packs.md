# Content Packs

Content packs live under `content/<pack_name>/` and include:

- `tiles.json`
- `entities.json`
- `items.json`
- `balance.json`

## Example: New Pack

1. Create a new directory:

```bash
mkdir -p content/frost
```

2. Copy the default pack and tweak values:

```bash
cp content/default/tiles.json content/frost/tiles.json
cp content/default/entities.json content/frost/entities.json
cp content/default/items.json content/frost/items.json
cp content/default/balance.json content/frost/balance.json
```

3. Start a game with the new pack:

```bash
curl -s -X POST http://localhost:8000/api/v1/games \
  -H "Content-Type: application/json" \
  -d '{"content_pack": "frost"}'
```
