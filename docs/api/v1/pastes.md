# Pastes
Contains views for interacting with pastes.

## GET /v1/pastes/
**AUTH REQUIRED**

Returns all user's pastes

Request params: None

Response body format:
```json
{
    "pastes": PasteModel(without stats link)
}
```

Response HTTP codes:
- `200` - success
- `400` - auth token problems
- `401` - auth required

Example request:
```
curl -H "Authorization: <auth token>" http://localhost/v1/pastes/
```

## POST /v1/pastes/
Creates new paste.

POST request params:
 - `text` <string> - Text of paste.
 - `language` <string> - Programming language of paste.
 - `stats_is_public` <bool> - Make paste stats public. Defaults to False.
 - `burn_after_read` <bool> - Paste will be deleted after first reading. Defaults to False.

Response body format:
```json
{
    "paste": PasteModel(stats link if you are authorized)
}
```

Response HTTP codes:
- `200` - success
- `400` - auth token problems
- `400` - invalid request params

Example request:
```
curl -X POST -d "text=example_short_text" http://localhost/v1/pastes/
```

## GET /v1/pastes/<paste_hash>/
Returns info about paste with <paste_hash>.

Request params: None

Response body format:
```json
{
    "paste": PasteModel(if you are accessed to stats)
}
```

Response HTTP codes:
- `200` - success
- `400` - auth token problems
- `404` - paste not found

Example request:
```
curl http://localhost/v1/pastes/abc123/
```

## DELETE /v1/pastes/<paste_hash>/
**AUTH REQUIRED**, **OWNERSHIP REQURED**

Deletes paste with <paste_hash>.

Request params: None

If successfully deleted, returns *204 HTTP response** with empty body.

Response HTTP codes:
- `204` - success
- `400` - auth token problems
- `401` - auth required
- `403` - forbidden (you are not owner)
- `404` - url not found

Example request:
```
curl -H "Authorization: <auth token>" -X DELETE http://localhost/v1/pastes/abc123/
```

## PATCH /v1/pastes/<paste_hash>/
**AUTH REQUIRED**, **OWNERSHIP REQURED**

Edits text or language of paste with <paste_hash>.

PATCH request params:
- `text` <string> - new paste text
- `language` <string> - new paste programming language

Response body format:
```json
{
    "paste": PasteModel(with stats link)
}
```

Response HTTP codes:
- `200` - success
- `400` - invalid request params
- `400` - auth token problems
- `401` - auth required
- `403` - forbidden (you are not owner)
- `404` - paste not found

Example request:
```
curl -X PATCH -d "text=some short text" http://localhost/v1/pastes/abc123/
```

## GET /v1/pastes/<paste_hash>/stats
**STATS ACCESS REQURED**

Returns statistics of paste with <paste_hash>.

Request params: None

Response body format:
```json
StatsModel()
```

Response HTTP codes:
- `200` - success
- `404` - paste not found

Example request:
```
curl http://localhost/v1/pastes/abc123/stats
```

## DELETE /v1/pastes/<paste_hash>/stats
**AUTH REQUIRED**, **OWNERSHIP REQURED**

Cleares paste statistics with <paste_hash>.

Request params: None

If successfully cleared, return *204 HTTP response* with empty body

Response HTTP codes:
- `204` - success
- `400` - auth token problems
- `401` - auth required
- `403` - forbidden (you are not owner)
- `404` - paste not found

Example request:
```
curl -X DELETE -H "Authorization: <auth token>" http://localhost/v1/pastes/abc123/stats
```
