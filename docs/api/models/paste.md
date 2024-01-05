# Paste model
Paste JSON model
```json
{
    "id": <int>,
    "hash": <string>,
    "text": <string>,
    "language": <string>,
    "expires_at": <float>,
    "is_expired": <boolean>,
    "stats_is_public": <boolean>,
    "burn_after_read": <boolean>,
    "is_deleted": <boolean>,
    <<< optional
    "_links": {
        "stats": {
            "href": <string>
        }
    },
    >>> optional
}
```

Fields:

`id` - database primary key.

`hash` - 6-letters hash.

`text` - text of paste

`language` - programming language of paste (default is *plain*)

`expires_at` - expiration date in unix timestamp format.

`is_expired` - true if url is expired, else false.

`stats_is_public` - true is stats is visible for all, false if stats is visible only for author.

`burn_after_read` - if true, paste will be deleted after first read.

`is_deleted` - true if url is deleted, else false

`_links` - contains various links to api resources.

`_links/stats/href` (optional) - link to stats resourse of this url.
This field is presented only if you have access to this url stats.
