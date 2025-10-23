# Structured-contents API examples
Used to fetch pre-parsed articles in their latest revision/version from all supported projects and languages.
Allows filtering and field selection. Allows to limit articles when doing cross-project, cross-language lookup.
Refer to the documentation [here](https://enterprise.wikimedia.com/docs/on-demand/#article-structured-contents-beta).

## Running the Application

To run the application, use the following command from the project's root:

```sh
python -m example.structured_contents.structuredcontents
```

i) Get pre-parsed articles with name `Montreal` from all projects in English language.

```bash
POST https://api.enterprise.wikimedia.com/v2/structured-contents/Montreal
```

with request parameter:
```json
{
    "limit": 5,
    "filters": [
        {
            "field": "in_language.identifier",
            "value": "en"
        }
    ]
}
```
Note: Max allowed limit is 10. Default limit is 3.

Response: [here](./response_i.json)


ii) Get pre-parsed articles with name `Montreal` from English Wikipedia with selected fields.

```bash
POST https://api.enterprise.wikimedia.com/v2/structured-contents/Montreal
```

with request parameter:
```json
{
    "limit": 1,
    "filters": [
        {
            "field": "is_part_of.identifier",
            "value": "enwiki"
        }
    ],
    "fields": ["abstract", "article_sections", "infobox"]
}
```

Response: [here](./response_ii.json)
