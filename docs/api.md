# API (v1)

Base path: `/api/v1`

## POST /games

Create a new game.

**Request**

```json
{
  "seed": 12345,
  "content_pack": "default"
}
```

**Response**

```json
{
  "game_id": "uuid",
  "seed": 12345
}
```

## GET /games/{id}

Get a full state snapshot.

**Response**

```json
{
  "state_version": 1,
  "turn": 3,
  "player": {"id": "player", "position": [0, 1]},
  "stats": {"hp": 20, "max_hp": 20, "atk": 5, "defense": 2, "xp": 0, "level": 1},
  "view": {"center": [0, 1], "radius": 10, "tiles": [], "entities": [], "items": [], "discovered": []},
  "events": [],
  "log": []
}
```

## POST /games/{id}/action

Apply a player action.

**Request**

```json
{
  "type": "MOVE",
  "payload": {"direction": "N"}
}
```

Supported types: `MOVE`, `ATTACK`, `PICKUP`, `USE`, `WAIT`.

**Response**

Returns the same payload as `GET /games/{id}`.

## POST /games/{id}/reset

Reset an existing game.

**Request**

```json
{
  "seed": 999
}
```

**Response**

```json
{
  "game_id": "uuid",
  "seed": 999
}
```

## GET /games/{id}/map

Get the visible window around the player.

**Response**

```json
{
  "center": [0, 0],
  "radius": 10,
  "tiles": [],
  "entities": [],
  "discovered": []
}
```

## GET /healthz

**Response**

```json
{"ok": true}
```
