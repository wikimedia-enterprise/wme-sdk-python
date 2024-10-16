# Structured-Contents Snapshot API examples

Structured-content snapshots are bundles of pre-parsed articles in their latest revision/version. The Structured-Contents Snapshots APIs provide information on the available structured-content snapshots and their metadata, allowing you to download them. The following is the snapshot schema.
Currently, SC snapshots are available for the following projects;

- enwiki
- dewiki
- frwiki
- eswki
- itwiki
- ptwiki

i) Get metadata of all the available SC snapshots.

```bash
POST https://api.enterprise.wikimedia.com/v2/snapshots/structured-contents
```

[Response](./response_i.json)

ii) Get metadata of all the available SC snapshots in English language.

With request parameter

```jsx
{
    "filters": [
        {
            "field": "in_language.identifier",
            "value": "en"
        }
    ]
}
```  
[Response](./response_ii.json)

iii) Get metadata of a single SC snapshot with identifier.

```bash
POST https://api.enterprise.wikimedia.com/v2/snapshots/structured-contents/enwiki_namespace_0
```  

[Response](./response_iii.json)

iv) Download a single SC snapshot with identifier

```bash
 GET https://api.enterprise.wikimedia.com/v2/snapshots/structured-contents/enwiki_namespace_0/download
```  