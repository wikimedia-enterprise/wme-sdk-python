# Batches API examples
A batch is a bundles of all articles in their latest revision/version from a supported project-namespace that have been updated on a given day. A batch generation starts at the beginning of the day in UTC, and they are updated every hour. So, at the end of the day, a batch contains all the articles that were updated that day.
Batches are kept for 14 days.

These APIs provide information on the available batches, their metadata, and allow to download them.
Allows filtering and field selection when fetching batches metadata. 
Allows parallel downloading using [Range headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range).
Refer to the documentation [here](https://enterprise.wikimedia.com/docs/realtime/#available-hourly-batches).
The articles included in the batches follow [this](https://gitlab.wikimedia.org/repos/wme/wikimedia-enterprise/-/blob/main/general/schema/article.go) schema.
The batches metadata follow [this](https://gitlab.wikimedia.org/repos/wme/wikimedia-enterprise/-/blob/main/general/schema/snapshot.go) schema.



i) Get metadata of all the available batches for a day.

```bash
POST https://api.enterprise.wikimedia.com/batches/2024-03-03
```



<detail>
<summary>Response:</summary> 

```json
[
    {
        "identifier": "abwiki_namespace_0",
        "version": "34462a47ee37113b765e59936d8fd7c8",
        "date_modified": "2024-03-04T00:18:03.207394118Z",
        "is_part_of": {
            "identifier": "abwiki"
        },
        "in_language": {
            "identifier": "ab"
        },
        "namespace": {
            "identifier": 0
        },
        "size": {
            "value": 0.027e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "acewiki_namespace_0",
        "version": "9e348387411cccdedda5111164748014",
        "date_modified": "2024-03-04T00:06:14.411661839Z",
        "is_part_of": {
            "identifier": "acewiki"
        },
        "in_language": {
            "identifier": "ace"
        },
        "namespace": {
            "identifier": 0
        },
        "size": {
            "value": 0.003e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "acewiki_namespace_10",
        "version": "f38e117df0d85dd94dd3379bcc2080a3",
        "date_modified": "2024-03-04T00:06:16.892227533Z",
        "is_part_of": {
            "identifier": "acewiki"
        },
        "in_language": {
            "identifier": "ace"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 0.002e0,
            "unit_text": "MB"
        }
    },
    .
    .
    .
]
```
</detail>


ii) Get metadata of all the available batches for English language for a day.

```bash
POST https://api.enterprise.wikimedia.com/batches/2024-03-03
```

with request parameters:
```json
{
    "filters": [
        {
            "field": "in_language.identifier",
            "value": "en"
        }
    ]
}
```


iii) Get metadata on a single batch. 

```bash
POST https://api.enterprise.wikimedia.com/v2/batches/2024-03-03/enwiki_namespace_0
```

Response:
```json
{
    "identifier": "enwiki_namespace_0",
    "version": "4464d27eb28f52d69850ebd3f6f5f224",
    "date_modified": "2024-03-04T00:12:20.744959737Z",
    "is_part_of": {
        "identifier": "enwiki"
    },
    "in_language": {
        "identifier": "en"
    },
    "namespace": {
        "identifier": 0
    },
    "size": {
        "value": 5551.221e0,
        "unit_text": "MB"
    }
}
```

iv) Get header information (last modified, content-length, etc.) on a single batch. 

```bash
HEAD https://api.enterprise.wikimedia.com/v2/batches/2024-03-03/afwikibooks_namespace_0/download
```


v) Download a batch. You can parallel download using `Range` header.

```bash
GET https://api.enterprise.wikimedia.com/v2/batches/2024-03-03/afwikibooks_namespace_0/download
```

with header:
```json
{
    "Range": "bytes=0-20"
}
```

```bash
GET https://api.enterprise.wikimedia.com/v2/batches/2024-03-03/afwikibooks_namespace_0/download
```

with header:
```json
{
    "Range": "bytes=21-36"
}
```

