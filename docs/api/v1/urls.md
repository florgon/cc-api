# Urls
Contains views for interacting with short urls.

## GET /v1/urls/
**AUTH REQUIRED**

Returns all user's short urls.

Request params: None

Response body format:
```json
{
    "urls" [UrlModel(without stats link)..]
}
```

Example request:
```
curl -H "Authorization: <auth token>" http://localhost/v1/urls/
```

## POST /v1/urls/
Creates new short url.

POST request params:
- `url` <string> -- Long url.
- `stats_is_public` <boolean> (auth required) -- Make stats awailable for all.

Response body format:
```json
{
    "url": UrlModel(stats link is included if you are owner or stats for this url is public)
}
```

Example request:
```
curl -X POST -d "url=gnu.org" http://localhost/v1/urls/
```

## GET /v1/urls/<url_hash>/
Returns info about short url with <url_hash>.

Request params: None

Response body format:
```json
{
    "url": UrlModel(stats link is included if you are owner or stats for this url is public)
}
```

Example request:
```
curl http://localhost/v1/urls/abc123/
```

## DELETE /v1/urls/<url_hash>/
**AUTH REQUIRED**, **OWNERSHIP REQUIRED**

Deletes short url with <url_hash>.

Request params: None

If successfully deleted, returns *204 HTTP response** with empty body.

Example request:
```
curl -H "Authorization: <auth token>" -X DELETE http://localhost/v1/urls/abc123/
```

## PATCH /v1/urls/<url_hash>/
This method is not implemented yet.

## GET /v1/urls/<url_hash>/qr
Returns qr-code image of short url with <url_hash>.

GET request params:
 - `result_type` <string> - Type of result. May be `svg`, `png` or `txt`. Defaults to `svg`.
 - `scale` <int> - Image scaling. May be integer from 1 to 8. Defaults to 3.
 - `quiet_zone` <int> - White border around qr-code. May be from 0 to 25. Defaults to 4.

Response body: `png` or `svg` image, or plain text

Example request:
```
curl http://localhost/v1/urls/abc123/qr
```

## GET /v1/urls/<url_hash>/open
Redirects user to long url.

## GET /v1/urls/<url_hash>/stats
**STATS ACCESS REQUIRED**

Return statistics for short url with <url_hash>.

## DELETE /v1/urls/<url_hash>/stats
**OWNERSHIP REQUIRED**

Cleares statistics for short url with <url_hash>.

If successfully cleared, return *204 HTTP response with empty body

