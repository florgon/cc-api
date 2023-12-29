# Source
Contains views for accessing the source code.

## GET /v1/source/
Request params: None

Response format:
```json
{
    "license": "AGPLv3-or-later",
    "repository": "https://github.com/florgon/cc-api",
    "download": "https://github.com/florgon/cc-api/archive/refs/heads/main.zip",
}
```
(Response values may be different)

If you fork this repo, you should edit *repository* and *download* properties.

Example request:
```
curl http://localhost/v1/source/
```
