# Statistics model
Represents statistics for url and paste.
```json
{
    "views": {
        "total": <int>
        <<< optional
        "by_referers": <int> 
        "by_dates": <int>
    }
}
```

Fields:

`total` - total views count

`by_referers` (represented only if total > 0) - object in format {referer: count of views}

`by_dates` (represented only if total > 0) - object in format {date in dd.mm.yyyy format: count of views}
