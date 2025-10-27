# Batches API examples

A batch is a bundles of all articles in their latest revision/version from a supported project-namespace that have been updated on a given day and hour. Batches are generated once per hour every day. For example, at 3am UTC, batches containing all updates that occurred between 2am and 3am UTC are generated, and are available at /v2/batches/{date}/02.

Batches are kept for 2 days.

These APIs:

- Provide information on the available batches, their metadata, and allow to download them.
- Allow filtering and field selection when fetching batches metadata.
- Allow parallel downloads using [Range headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range).

Refer to the documentation [here](https://enterprise.wikimedia.com/docs/realtime/#available-hourly-batches).

The articles included in the batches follow [this](https://gitlab.wikimedia.org/repos/wme/wikimedia-enterprise/-/blob/main/general/schema/article.go) schema.

The batches metadata follow [this](https://gitlab.wikimedia.org/repos/wme/wikimedia-enterprise/-/blob/main/general/schema/snapshot.go) schema.

## Prerequisites

Before running this script, you must have your environment set up.

1.  **Environment Variables:** The script requires user credentials to authenticate with the API. Ensure the following environment variables are set on the .env file:

    ```bash
    WME_USERNAME="your_username"
    WME_PASSWORD="your_password"
    ```

2.  **Python Dependencies:** You must have the required packages, like `httpx` and the SDK's modules, available in your Python environment.

## How to Run

This script is designed to be run from the **virtual enviroment** of the SDK. Once within the virtual enviroment, execute the script:

```bash
python -m example.batches.batches
```

## Use Cases

i) Get metadata of all the available batches for a day and hour.

```bash
POST https://api.enterprise.wikimedia.com/batches/2025-07-16/05
```



<detail>
<summary>Response:</summary>

```json
[
    {
        "identifier": "abwiki_namespace_0",
        "version": "34462a47ee37113b765e59936d8fd7c8",
        "date_modified": "2024-07-16T06:06:16.892227533Z",
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
        "date_modified": "2024-07-16T06:06:16.892227533Z",
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
        "date_modified": "2024-07-16T06:06:16.892227533Z",
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


ii) Get metadata of all the available batches for English language for a day and hour.

```bash
POST https://api.enterprise.wikimedia.com/batches/2025-07-16/05
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
POST https://api.enterprise.wikimedia.com/v2/batches/2025-07-16/05/enwiki_namespace_0
```

Response:
```json
{
    "identifier": "enwiki_namespace_0",
    "version": "4464d27eb28f52d69850ebd3f6f5f224",
    "date_modified": "2024-07-16T06:12:20.744959737Z",
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
HEAD https://api.enterprise.wikimedia.com/v2/batches/2025-07-16/05/afwikibooks_namespace_0/download
```


v) Download a batch. You can download in parallel using `Range` header.

```bash
GET https://api.enterprise.wikimedia.com/v2/batches/2025-07-16/05/afwikibooks_namespace_0/download
```

with header:
```json
{
    "Range": "bytes=0-20"
}
```

```bash
GET https://api.enterprise.wikimedia.com/v2/batches/2025-07-16/05/afwikibooks_namespace_0/download
```

with header:
```json
{
    "Range": "bytes=21-36"
}
```

## Expected Output

The script will log its progress for each of the five use cases. A successful run will look similar to this:

```
INFO:__main__:Successfully authenticated.
INFO:__main__:--- Targeting batches for 2025-10-26 10:00 UTC ---

INFO:__main__:--- i) Get metadata for all available batches ---
INFO:__main__:Found 150 total batches.
INFO:__main__:Metadata for the first batch:
INFO:__main__:{
  "identifier": "arwiki_namespace_0",
  "version": "...",
  ...
}

INFO:__main__:--- ii) Get metadata for 'en' (English) batches ---
INFO:__main__:Found 12 'en' batches.
INFO:__main__:Metadata for the first 'en' batch:
INFO:__main__:{
  "identifier": "enwiki_namespace_0",
  ...
}

INFO:__main__:--- iii) Get metadata for a single batch (enwiki_namespace_0) ---
INFO:__main__:Metadata for 'enwiki_namespace_0':
INFO:__main__:{
  "identifier": "enwiki_namespace_0",
  "version": "...",
  ...
}

INFO:__main__:--- iv) Get HEAD metadata for a single batch (enwiki_namespace_0) ---
INFO:__main__:Headers for 'enwiki_namespace_0':
INFO:__main__:{
  "ETag": "...",
  "Content-Type": "application/gzip",
  "Content-Length": 123456789
}
INFO:__main__:Content-Length from HEAD: 123456789 bytes

INFO:__main__:--- v) Download and read a batch (enwiki_namespace_0) ---
INFO:__main__:Downloading 'enwiki_namespace_0' into an in-memory buffer...
INFO:__main__:Downloaded 117.74 MB in 8.34 s
INFO:__main__:Processing the downloaded archive...
INFO:__main__:Successfully processed 25148 articles from the batch.
INFO:__main__:First 5 article identifiers: ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
INFO:__main__:Shutting down helper and revoking tokens...
INFO:__main__:Exiting.
```
