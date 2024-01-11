# Overview

Once you run API, you can test it manually. It is running on *http://localhost/* by default.

All API routes starts with version name (e.g. `/v1/`). Now only `/v1/` awailable.

So, check API status with curl, wget, postman or just your browser:
```bash
curl http://localhost/v1/utils/serverTime
```
It should return successful response and server time.

`utils` in url is the *router* or *view*. Awailable `source`, `utils`, `urls`, `pastes` routers

## Get source code

Florgon CC API is licensed under AGPLv3, so you can access source code at `/v1/sources/`
