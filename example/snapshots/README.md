# Snapshots API examples
A snapshot is a bundles of all articles in their latest revision/version from a supported project-namespace. These APIs provide information on the available snapshots, their metadata, and allow to download them.
Snapshots for each project-namespace are updated monthly (for free tier users) and daily for non-free tier.
Allows filtering and field selection when fetching snapshots metadata.
Allows parallel downloading using [Range headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range).
Refer to the documentation [here](https://enterprise.wikimedia.com/docs/snapshot/).
The articles included in the snapshots follow [this](https://gitlab.wikimedia.org/repos/wme/wikimedia-enterprise/-/blob/main/general/schema/article.go) schema.
The snapshot metadata follow [this](https://gitlab.wikimedia.org/repos/wme/wikimedia-enterprise/-/blob/main/general/schema/snapshot.go) schema.

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
python -m example.metadata.metadata
```

## Use Cases
i) Get metadata of all the available snapshots. There should be one snapshot for each supported project-namespace.

```bash
POST https://api.enterprise.wikimedia.com/v2/snapshots
```



<detail>
<summary>Response:</summary>

```json
[
    {
        "identifier": "abwiki_namespace_0",
        "version": "ff95fe528632cd9c347e8f81ab549e16",
        "date_modified": "2024-02-11T02:29:43.706662927Z",
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
            "value": 17.65e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "abwiki_namespace_10",
        "version": "90262a778595fd3712189e1b0eefcb37",
        "date_modified": "2024-02-11T02:29:48.38787207Z",
        "is_part_of": {
            "identifier": "abwiki"
        },
        "in_language": {
            "identifier": "ab"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 4.842e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "abwiki_namespace_14",
        "version": "674002668d79efc2f11deb20c595d032",
        "date_modified": "2024-02-11T02:29:51.982874902Z",
        "is_part_of": {
            "identifier": "abwiki"
        },
        "in_language": {
            "identifier": "ab"
        },
        "namespace": {
            "identifier": 14
        },
        "size": {
            "value": 5.262e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "abwiki_namespace_6",
        "version": "72d40ee0d11c34565a6d3a2ec910d683",
        "date_modified": "2024-02-11T02:29:45.526644231Z",
        "is_part_of": {
            "identifier": "abwiki"
        },
        "in_language": {
            "identifier": "ab"
        },
        "namespace": {
            "identifier": 6
        },
        "size": {
            "value": 0.009e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "acewiki_namespace_0",
        "version": "176555508fb9440731de94fea3bd229d",
        "date_modified": "2024-02-11T01:13:12.802478382Z",
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
            "value": 23.932e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "acewiki_namespace_10",
        "version": "97da2929e813e968a83d2f155be8e12e",
        "date_modified": "2024-02-11T01:13:16.402959135Z",
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
            "value": 2.929e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "acewiki_namespace_14",
        "version": "9973e7f602147ffa2cc17f4608fcdae9",
        "date_modified": "2024-02-11T01:13:18.436567013Z",
        "is_part_of": {
            "identifier": "acewiki"
        },
        "in_language": {
            "identifier": "ace"
        },
        "namespace": {
            "identifier": 14
        },
        "size": {
            "value": 0.293e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "adywiki_namespace_0",
        "version": "64abdde789ccbafa385cad49dcf27779",
        "date_modified": "2024-02-11T00:30:23.230469746Z",
        "is_part_of": {
            "identifier": "adywiki"
        },
        "in_language": {
            "identifier": "ady"
        },
        "namespace": {
            "identifier": 0
        },
        "size": {
            "value": 1.122e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "adywiki_namespace_10",
        "version": "9a12be13fd5791ba5466c9dc6c19a3bd",
        "date_modified": "2024-02-11T00:30:26.509648687Z",
        "is_part_of": {
            "identifier": "adywiki"
        },
        "in_language": {
            "identifier": "ady"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 1.597e0,
            "unit_text": "MB"
        }
    },
    .
    .
    .
]
```
</detail>


ii) Get metadata of all the available snapshots for English language.

```bash
POST https://api.enterprise.wikimedia.com/v2/snapshots
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



<detail>
<summary>Response:</summary>

```json
[
    {
        "identifier": "enwiki_namespace_0",
        "version": "7c10f092ac9cfc1947aa9a47018b0452",
        "date_modified": "2024-02-11T03:36:51.314705199Z",
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
            "value": 126211.488e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwiki_namespace_10",
        "version": "d6bc1f09c17077f13f40767c3efbcc68",
        "date_modified": "2024-02-11T03:42:45.594936917Z",
        "is_part_of": {
            "identifier": "enwiki"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 2468.057e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwiki_namespace_14",
        "version": "f0d7dcd5b9fa1435aa909155ece4dc0c",
        "date_modified": "2024-02-11T03:46:44.610528979Z",
        "is_part_of": {
            "identifier": "enwiki"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 14
        },
        "size": {
            "value": 2107.859e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwiki_namespace_6",
        "version": "62caaf96deac4cce2ccb0e0921e3bfe6",
        "date_modified": "2024-02-11T03:39:43.222693313Z",
        "is_part_of": {
            "identifier": "enwiki"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 6
        },
        "size": {
            "value": 1997.868e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikibooks_namespace_0",
        "version": "759d16fd0a46b930a62fc07ef37646b7",
        "date_modified": "2024-02-11T03:35:18.457413645Z",
        "is_part_of": {
            "identifier": "enwikibooks"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 0
        },
        "size": {
            "value": 871.104e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikibooks_namespace_10",
        "version": "bb57db5924255bb087bfb21e9d0c2ab9",
        "date_modified": "2024-02-11T03:35:24.99753494Z",
        "is_part_of": {
            "identifier": "enwikibooks"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 16.432e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikibooks_namespace_14",
        "version": "3042cfacd034171377dec52fe32177b4",
        "date_modified": "2024-02-11T03:35:28.585341575Z",
        "is_part_of": {
            "identifier": "enwikibooks"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 14
        },
        "size": {
            "value": 6.697e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikibooks_namespace_6",
        "version": "468af719bb045f02685599be2d597423",
        "date_modified": "2024-02-11T03:35:21.021676068Z",
        "is_part_of": {
            "identifier": "enwikibooks"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 6
        },
        "size": {
            "value": 2.252e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikinews_namespace_0",
        "version": "bd621b93325343630fabfdec270ab7be",
        "date_modified": "2024-02-11T04:17:55.262377999Z",
        "is_part_of": {
            "identifier": "enwikinews"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 0
        },
        "size": {
            "value": 141.677e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikinews_namespace_10",
        "version": "3b7493f40e0f40d4451388727a784412",
        "date_modified": "2024-02-11T04:18:01.810680386Z",
        "is_part_of": {
            "identifier": "enwikinews"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 5.716e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikinews_namespace_14",
        "version": "ae06b6e9c8a8907b7ec1cc1d3d77ba4a",
        "date_modified": "2024-02-11T04:18:05.819775441Z",
        "is_part_of": {
            "identifier": "enwikinews"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 14
        },
        "size": {
            "value": 12.197e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikinews_namespace_6",
        "version": "5d33d7b96b90de0b368ea408abc0b509",
        "date_modified": "2024-02-11T04:17:58.488254779Z",
        "is_part_of": {
            "identifier": "enwikinews"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 6
        },
        "size": {
            "value": 4.955e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikiquote_namespace_0",
        "version": "a6b7bd47dec724e56f760c1b6f712799",
        "date_modified": "2024-02-11T00:23:27.599563726Z",
        "is_part_of": {
            "identifier": "enwikiquote"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 0
        },
        "size": {
            "value": 505.506e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikiquote_namespace_10",
        "version": "afea7b52237b025a0225c3a281fc6e39",
        "date_modified": "2024-02-11T00:23:31.263678444Z",
        "is_part_of": {
            "identifier": "enwikiquote"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 2.442e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikiquote_namespace_14",
        "version": "862c6ec4b593f4496c7f0bc29f4dada8",
        "date_modified": "2024-02-11T00:23:33.925644229Z",
        "is_part_of": {
            "identifier": "enwikiquote"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 14
        },
        "size": {
            "value": 5.53e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikisource_namespace_0",
        "version": "5d19f901b83d91bbdc7fcaf98a503820",
        "date_modified": "2024-02-11T00:12:36.06644666Z",
        "is_part_of": {
            "identifier": "enwikisource"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 0
        },
        "size": {
            "value": 4659.78e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikisource_namespace_10",
        "version": "500a28e6e12428e246b04917e1a4f060",
        "date_modified": "2024-02-11T00:12:43.444302458Z",
        "is_part_of": {
            "identifier": "enwikisource"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 21.129e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikisource_namespace_14",
        "version": "88b27d84a2a9ea9b14b46157214eb130",
        "date_modified": "2024-02-11T00:12:46.741497737Z",
        "is_part_of": {
            "identifier": "enwikisource"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 14
        },
        "size": {
            "value": 9.526e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikisource_namespace_6",
        "version": "ee40d71519874e3bbe4094476f6fe188",
        "date_modified": "2024-02-11T00:12:39.779449136Z",
        "is_part_of": {
            "identifier": "enwikisource"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 6
        },
        "size": {
            "value": 12.377e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikiversity_namespace_0",
        "version": "778dc019cb3e15ec8efaafbc2c76f0c5",
        "date_modified": "2024-02-11T00:47:50.687661191Z",
        "is_part_of": {
            "identifier": "enwikiversity"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 0
        },
        "size": {
            "value": 382.721e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikiversity_namespace_10",
        "version": "7a7a1c7c3c2deacf0595ada112b2a77b",
        "date_modified": "2024-02-11T00:48:01.360098297Z",
        "is_part_of": {
            "identifier": "enwikiversity"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 23.952e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikiversity_namespace_14",
        "version": "129e646c005ff931f041c5e467185751",
        "date_modified": "2024-02-11T00:48:03.954668934Z",
        "is_part_of": {
            "identifier": "enwikiversity"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 14
        },
        "size": {
            "value": 3.131e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikiversity_namespace_6",
        "version": "caba0c99ef4a7bc6e19ae311fa16e492",
        "date_modified": "2024-02-11T00:47:56.969867718Z",
        "is_part_of": {
            "identifier": "enwikiversity"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 6
        },
        "size": {
            "value": 12.405e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikivoyage_namespace_0",
        "version": "ebe0a601a2a2cec206b28511cfb61f4b",
        "date_modified": "2024-02-11T04:06:50.035040944Z",
        "is_part_of": {
            "identifier": "enwikivoyage"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 0
        },
        "size": {
            "value": 524.572e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikivoyage_namespace_10",
        "version": "66a23f77420dd55aa2113ef377bcfa6d",
        "date_modified": "2024-02-11T04:06:55.188780473Z",
        "is_part_of": {
            "identifier": "enwikivoyage"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 6.184e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikivoyage_namespace_14",
        "version": "b5bc7dafb7176792016bc401af3170d3",
        "date_modified": "2024-02-11T04:06:57.660870627Z",
        "is_part_of": {
            "identifier": "enwikivoyage"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 14
        },
        "size": {
            "value": 1.4e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwikivoyage_namespace_6",
        "version": "b69d4593a283d05411792662c72e27dc",
        "date_modified": "2024-02-11T04:06:52.575331768Z",
        "is_part_of": {
            "identifier": "enwikivoyage"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 6
        },
        "size": {
            "value": 1.92e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwiktionary_namespace_0",
        "version": "4f2dcf95b5220ff35e0f1cd60783472e",
        "date_modified": "2024-02-11T05:50:57.119988994Z",
        "is_part_of": {
            "identifier": "enwiktionary"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 0
        },
        "size": {
            "value": 10057.219e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwiktionary_namespace_10",
        "version": "5a28dabfea4f649dd886df6b4aaaaaf2",
        "date_modified": "2024-02-11T05:51:15.666570245Z",
        "is_part_of": {
            "identifier": "enwiktionary"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 10
        },
        "size": {
            "value": 148.155e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwiktionary_namespace_14",
        "version": "1715ecbcfd418a4d2b3292aca1895764",
        "date_modified": "2024-02-11T05:52:45.122660333Z",
        "is_part_of": {
            "identifier": "enwiktionary"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 14
        },
        "size": {
            "value": 532.275e0,
            "unit_text": "MB"
        }
    },
    {
        "identifier": "enwiktionary_namespace_6",
        "version": "761bf708b2b1af688f1d679176cfd06f",
        "date_modified": "2024-02-11T05:50:59.067937478Z",
        "is_part_of": {
            "identifier": "enwiktionary"
        },
        "in_language": {
            "identifier": "en"
        },
        "namespace": {
            "identifier": 6
        },
        "size": {
            "value": 0.023e0,
            "unit_text": "MB"
        }
    }
]
```
</detail>

iii) Get metadata on a single snapshot.

```bash
POST https://api.enterprise.wikimedia.com/v2/snapshots/enwiki_namespace_0
```

Response:
```json
{
    "identifier": "enwiki_namespace_0",
    "version": "a2fc61696534ae1a2fda990cb8858a43",
    "date_modified": "2024-02-12T03:35:30.181816177Z",
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
        "value": 125215.975e0,
        "unit_text": "MB"
    }
}
```

iv) Get header information (last modified, content-length, etc.) on a single snapshot.

```bash
HEAD https://api.enterprise.wikimedia.com/v2/snapshots/afwikibooks_namespace_0/download
```

Response headers:
![Response headers](./response_headers.png)

Here, the size (content length) is 215077 bytes.



v) Download a snapshot. You can parallel download using `Range` header.

```bash
GET https://api.enterprise.wikimedia.com/v2/snapshots/afwikibooks_namespace_0/download
```

with header:
```json
{
    "Range": "bytes=0-99000"
}
```

```bash
GET https://api.enterprise.wikimedia.com/v2/snapshots/afwikibooks_namespace_0/download
```

with header:
```json
{
    "Range": "bytes=99001-215077"
}
```

## Expected Output

The script will log its progress for each of the five use cases. A successful run will look similar to this:

```
INFO:__main__:Setting up authentication...
INFO:__main__:Succesfully authenticated!

INFO:__main__:Starting Snapshot examples...

INFO:__main__:--- Metadata of all available Snapshots ---
INFO:__main__:1) Get metadata of all available Snapshots:
INFO:__main__:Printing metadata for all available snapshots:
INFO:__main__:[
  {
    "identifier": "aawiki_namespace_0",
    "version": "...",
    "in_language": {
      "identifier": "aa"
    },
    ...
  },
  ...
]

INFO:__main__:--- Metadata of English Snapshots ---
INFO:__main__:2) Get metadata of English Snapshots:
INFO:__main__:Filtered English Snapshots:
INFO:__main__:[
  {
    "identifier": "enwiki_namespace_0",
    "version": "...",
    "in_language": {
      "identifier": "en"
    },
    ...
  },
  ...
]

INFO:__main__:--- Metadata of a single snapshot ---
INFO:__main__:3) Get metadata of a single Snapshots:
INFO:__main__:Filtered single snapshot (Spanish)
INFO:__main__:{
  "identifier": "eswiki_namespace_0",
  "version": "...",
  "in_language": {
    "identifier": "es"
  },
  ...
}

INFO:__main__:4) Get HEAD metadata for snapshot 'eswikibooks_namespace_0':
INFO:__main__:Headers for 'eswikibooks_namespace_0':
INFO:__main__:{
  "ETag": "...",
  "Content-Type": "application/gzip",
  "Content-Length": 1234567,
  ...
}
INFO:__main__:Content-Length from HEAD: 1234567 bytes

INFO:__main__:5) Download and read snapshot 'eswikibooks_namespace_0':
INFO:__main__:Downloading 'eswikibooks_namespace_0' (1234567 bytes) into memory...
INFO:__main__:Downloaded 1.18 MB in 1.23 s
INFO:__main__:Processing the downloaded archive...
INFO:__main__:Succesfully processed 150 articles from snapshot.
INFO:__main__:First 5 article names/identifiers: ['Main Page', 'Chapter 1', 'Chapter 2', 'Chapter 3', 'Chapter 4']

INFO:__main__:--- Snapshot API examples complete ---
INFO:__main__:Shutting down helper and revoking tokens...
INFO:__main__:Exiting!
```
