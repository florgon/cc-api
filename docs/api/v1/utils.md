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

Example request:
```
curl http://localhost/v1/utils/serverTime
```
