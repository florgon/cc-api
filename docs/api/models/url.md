## Url model
Short url JSON model.
```json
{
    "id": <int>,
    "redirect_url": <string>,
    "hash": <string>,
    "expires_at": <timestamp>,
    "is_expired": <boolean>,
    "stats_is_public": <boolean>,
    "is_deleted": <boolean>,
    "_links": {
        "qr": {
            "href": <string>,
        },
        <<< optional
        "stats": {
            "href": <string>
        }
        >>>
    },
}
```

Fields:

`id` - database primary key.

`redirect_url` - external long url.

`hash` - 6-letters hash.

`expires_at` - expiration date in unix timestamp format.

`is_expired` - true if url is expired, else false.

`stats_is_public` - true is stats is visible for all, false if stats is visible only for author.

`is_deleted` - true if url is deleted, else false

`_links` - contains various links to api resources.

`_links/qr/href` - link to qr-code image of short url.

`_links/stats/href` (optional) - link to stats resourse of this url.
This field is presented only if you have access to this url stats.
