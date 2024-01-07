# Access rights
In documentation you can see some access rights marks.

**AUTH REQUIRED** - Valid florgon authorization token needed. Pass it in `Authorization` header.

**OWNERSHIP REQUIRED** - You should be owner of url/paste (url's user_id should be equal to your user id).

**STATS ACCESS REQUIRED** - If url/paste has `stats_is_public=True`, resource with this access right is available to any user. If url/paste has `stats_is_public=False`, this access right is equal to **OWNERSHIP REQUIRED** (you should be owner to see stats).
