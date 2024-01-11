# API Response

API Response may be successful or not.

Error response is always in JSON format.
Successful response is usually in JSON format, but also may be response with **empty body**

Error response structure:
```json
{
    "v": <version of API in semantic version format>,
    "error": {
        "message": <error message in string format>,
        "code": <own API return code in integer>,
        "status": <HTTP status code in integer>,
        <optional and additional data>
    }
}
```

Successful response structure:
```json
{
    "v": <version of API in semantic version format>,
    "success": {
        <data>
    }
}
```

