# Utils
Contains various utilities for API.

## GET /v1/utils/serverTime
Request params: None

Response body format:
```json
{
    "server_time": <current unix timestamp>
}
```

Response HTTP codes:
- `200` - success

Example request:
```
curl http://localhost/v1/utils/serverTime
```
