# Metadata API examples
Used to get information on supported projects, namespaces, languages and project codes (types).
Refer to the documentation [here](https://enterprise.wikimedia.com/docs/metadata/).

## Project code example
Get metadata on available project codes (types).
Allows filtering and field selection.

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

i) Without any parameters. Returns all the project codes.

```bash
GET https://api.enterprise.wikimedia.com/v2/codes
```

Response:
```json
[
    {
        "identifier": "wiki",
        "name": "Wikipedia",
        "description": "The free encyclopedia."
    },
    {
        "identifier": "wikibooks",
        "name": "Wikibooks",
        "description": "E-book textbooks and annotated texts."
    },
    {
        "identifier": "wikinews",
        "name": "Wikinews",
        "description": "The free news source."
    },
    {
        "identifier": "wikiquote",
        "name": "Wikiquote",
        "description": "Quotes across your favorite books, movies, authors, and more."
    },
    {
        "identifier": "wikisource",
        "name": "Wikisource",
        "description": "The free digital library."
    },
    {
        "identifier": "wikivoyage",
        "name": "Wikivoyage",
        "description": "The ultimate worldwide travel guide."
    },
    {
        "identifier": "wiktionary",
        "name": "Wiktionary",
        "description": "A dictionary for over 170 languages."
    }
]
```

ii) Selet fields that you want to see.

```bash
POST https://api.enterprise.wikimedia.com/v2/codes
```

with request parameter
```json
{
    "fields": [
        "identifier"
    ]
}
```

Response:
```json
[
    {
        "identifier": "wiki"
    },
    {
        "identifier": "wikibooks"
    },
    {
        "identifier": "wikinews"
    },
    {
        "identifier": "wikiquote"
    },
    {
        "identifier": "wikisource"
    },
    {
        "identifier": "wikivoyage"
    },
    {
        "identifier": "wiktionary"
    }
]
```

iii) With filters and field selection

```bash
POST https://api.enterprise.wikimedia.com/v2/codes
```

with request parameter
```json
{
    "fields": [
        "identifier"
    ],
    "filters": [
        {
            "field": "identifier",
            "value": "wiki"
        }
    ]
}
```

Response:
```json
[
    {
        "identifier": "wiki"
    }
]
```

iv) Query specific project code

```bash
POST https://api.enterprise.wikimedia.com/v2/codes/wiktionary
```

Response:

```json
{
    "identifier": "wiktionary",
    "name": "Wiktionary",
    "description": "A dictionary for over 170 languages."
}
```

v) Query specific project code with field selection

```bash
POST https://api.enterprise.wikimedia.com/v2/codes/wiktionary
```
with request parameter
```json
{
    "fields": [
        "identifier"
    ]
}
```

Response:

```json
{
    "identifier": "wiktionary"
}
```

## Language example
Get all the supported languages with their metadata. Supports filtering and field selection.

i) All languages without filter or field selection.
```bash
GET https://api.enterprise.wikimedia.com/v2/languages
```
<details>
<summary>Response:</summary>

```json
[
    {
        "identifier": "cv",
        "name": "Chuvash",
        "alternate_name": "чӑвашла",
        "direction": "ltr"
    },
    {
        "identifier": "id",
        "name": "Indonesian",
        "alternate_name": "Bahasa Indonesia",
        "direction": "ltr"
    },
    {
        "identifier": "vi",
        "name": "Vietnamese",
        "alternate_name": "Tiếng Việt",
        "direction": "ltr"
    },
    {
        "identifier": "dv",
        "name": "Divehi",
        "alternate_name": "ދިވެހިބަސް",
        "direction": "rtl"
    },
    {
        "identifier": "new",
        "name": "Newari",
        "alternate_name": "नेपाल भाषा",
        "direction": "ltr"
    },
    {
        "identifier": "rw",
        "name": "Kinyarwanda",
        "alternate_name": "Ikinyarwanda",
        "direction": "ltr"
    },
    {
        "identifier": "srn",
        "name": "Sranan Tongo",
        "alternate_name": "Sranantongo",
        "direction": "ltr"
    },
    {
        "identifier": "eo",
        "name": "Esperanto",
        "alternate_name": "Esperanto",
        "direction": "ltr"
    },
    {
        "identifier": "kv",
        "name": "Komi",
        "alternate_name": "коми",
        "direction": "ltr"
    },
    {
        "identifier": "mzn",
        "name": "Mazanderani",
        "alternate_name": "مازِرونی",
        "direction": "rtl"
    },
    {
        "identifier": "nah",
        "name": "Nāhuatl",
        "alternate_name": "Nāhuatl",
        "direction": "ltr"
    },
    {
        "identifier": "ne",
        "name": "Nepali",
        "alternate_name": "नेपाली",
        "direction": "ltr"
    },
    {
        "identifier": "nqo",
        "name": "N’Ko",
        "alternate_name": "ߒߞߏ",
        "direction": "rtl"
    },
    {
        "identifier": "tr",
        "name": "Turkish",
        "alternate_name": "Türkçe",
        "direction": "ltr"
    },
    {
        "identifier": "gn",
        "name": "Guarani",
        "alternate_name": "Avañe'ẽ",
        "direction": "ltr"
    },
    {
        "identifier": "ha",
        "name": "Hausa",
        "alternate_name": "Hausa",
        "direction": "ltr"
    },
    {
        "identifier": "it",
        "name": "Italian",
        "alternate_name": "italiano",
        "direction": "ltr"
    },
    {
        "identifier": "lt",
        "name": "Lithuanian",
        "alternate_name": "lietuvių",
        "direction": "ltr"
    },
    {
        "identifier": "mo",
        "name": "Moldovan",
        "alternate_name": "молдовеняскэ",
        "direction": "ltr"
    },
    {
        "identifier": "tn",
        "name": "Tswana",
        "alternate_name": "Setswana",
        "direction": "ltr"
    },
    {
        "identifier": "am",
        "name": "Amharic",
        "alternate_name": "አማርኛ",
        "direction": "ltr"
    },
    {
        "identifier": "bug",
        "name": "Buginese",
        "alternate_name": "Basa Ugi",
        "direction": "ltr"
    },
    {
        "identifier": "ch",
        "name": "Chamorro",
        "alternate_name": "Chamoru",
        "direction": "ltr"
    },
    {
        "identifier": "ml",
        "name": "Malayalam",
        "alternate_name": "മലയാളം",
        "direction": "ltr"
    },
    {
        "identifier": "nrm",
        "name": "Norman",
        "alternate_name": "Nouormand",
        "direction": "ltr"
    },
    {
        "identifier": "nv",
        "name": "Navajo",
        "alternate_name": "Diné bizaad",
        "direction": "ltr"
    },
    {
        "identifier": "scn",
        "name": "Sicilian",
        "alternate_name": "sicilianu",
        "direction": "ltr"
    },
    {
        "identifier": "yi",
        "name": "Yiddish",
        "alternate_name": "ייִדיש",
        "direction": "rtl"
    },
    {
        "identifier": "shi",
        "name": "Tachelhit",
        "alternate_name": "Taclḥit",
        "direction": "ltr"
    },
    {
        "identifier": "als",
        "name": "Alemannisch",
        "alternate_name": "Alemannisch",
        "direction": "ltr"
    },
    {
        "identifier": "ary",
        "name": "Moroccan Arabic",
        "alternate_name": "الدارجة",
        "direction": "rtl"
    },
    {
        "identifier": "btm",
        "name": "Batak Mandailing",
        "alternate_name": "Batak Mandailing",
        "direction": "ltr"
    },
    {
        "identifier": "cdo",
        "name": "Min Dong Chinese",
        "alternate_name": "閩東語 / Mìng-dĕ̤ng-ngṳ̄",
        "direction": "ltr"
    },
    {
        "identifier": "ja",
        "name": "Japanese",
        "alternate_name": "日本語",
        "direction": "ltr"
    },
    {
        "identifier": "kbp",
        "name": "Kabiye",
        "alternate_name": "Kabɩyɛ",
        "direction": "ltr"
    },
    {
        "identifier": "oc",
        "name": "Occitan",
        "alternate_name": "occitan",
        "direction": "ltr"
    },
    {
        "identifier": "skr",
        "name": "Saraiki",
        "alternate_name": "سرائیکی",
        "direction": "rtl"
    },
    {
        "identifier": "vo",
        "name": "Volapük",
        "alternate_name": "Volapük",
        "direction": "ltr"
    },
    {
        "identifier": "din",
        "name": "Dinka",
        "alternate_name": "Thuɔŋjäŋ",
        "direction": "ltr"
    },
    {
        "identifier": "ff",
        "name": "Fula",
        "alternate_name": "Fulfulde",
        "direction": "ltr"
    },
    {
        "identifier": "lld",
        "name": "Ladin",
        "alternate_name": "Ladin",
        "direction": "ltr"
    },
    {
        "identifier": "nov",
        "name": "Novial",
        "alternate_name": "Novial",
        "direction": "ltr"
    },
    {
        "identifier": "ur",
        "name": "Urdu",
        "alternate_name": "اردو",
        "direction": "rtl"
    },
    {
        "identifier": "zea",
        "name": "Zeelandic",
        "alternate_name": "Zeêuws",
        "direction": "ltr"
    },
    {
        "identifier": "fat",
        "name": "Fanti",
        "alternate_name": "mfantse",
        "direction": "ltr"
    },
    {
        "identifier": "frp",
        "name": "Arpitan",
        "alternate_name": "arpetan",
        "direction": "ltr"
    },
    {
        "identifier": "inh",
        "name": "Ingush",
        "alternate_name": "гӀалгӀай",
        "direction": "ltr"
    },
    {
        "identifier": "pi",
        "name": "Pali",
        "alternate_name": "पालि",
        "direction": "ltr"
    },
    {
        "identifier": "kn",
        "name": "Kannada",
        "alternate_name": "ಕನ್ನಡ",
        "direction": "ltr"
    },
    {
        "identifier": "no",
        "name": "Norwegian",
        "alternate_name": "norsk",
        "direction": "ltr"
    },
    {
        "identifier": "rn",
        "name": "Rundi",
        "alternate_name": "ikirundi",
        "direction": "ltr"
    },
    {
        "identifier": "ln",
        "name": "Lingala",
        "alternate_name": "lingála",
        "direction": "ltr"
    },
    {
        "identifier": "ps",
        "name": "Pashto",
        "alternate_name": "پښتو",
        "direction": "rtl"
    },
    {
        "identifier": "sv",
        "name": "Swedish",
        "alternate_name": "svenska",
        "direction": "ltr"
    },
    {
        "identifier": "war",
        "name": "Waray",
        "alternate_name": "Winaray",
        "direction": "ltr"
    },
    {
        "identifier": "cho",
        "name": "Choctaw",
        "alternate_name": "Chahta anumpa",
        "direction": "ltr"
    },
    {
        "identifier": "smn",
        "name": "Inari Sami",
        "alternate_name": "anarâškielâ",
        "direction": "ltr"
    },
    {
        "identifier": "uk",
        "name": "Ukrainian",
        "alternate_name": "українська",
        "direction": "ltr"
    },
    {
        "identifier": "vls",
        "name": "West Flemish",
        "alternate_name": "West-Vlams",
        "direction": "ltr"
    },
    {
        "identifier": "fa",
        "name": "Persian",
        "alternate_name": "فارسی",
        "direction": "rtl"
    },
    {
        "identifier": "or",
        "name": "Odia",
        "alternate_name": "ଓଡ଼ିଆ",
        "direction": "ltr"
    },
    {
        "identifier": "zh-min-nan",
        "name": "Chinese (Min Nan)",
        "alternate_name": "Bân-lâm-gú",
        "direction": "ltr"
    },
    {
        "identifier": "cbk-zam",
        "name": "Chavacano",
        "alternate_name": "Chavacano de Zamboanga",
        "direction": "ltr"
    },
    {
        "identifier": "chy",
        "name": "Cheyenne",
        "alternate_name": "Tsetsêhestâhese",
        "direction": "ltr"
    },
    {
        "identifier": "de",
        "name": "German",
        "alternate_name": "Deutsch",
        "direction": "ltr"
    },
    {
        "identifier": "kaa",
        "name": "Kara-Kalpak",
        "alternate_name": "Qaraqalpaqsha",
        "direction": "ltr"
    },
    {
        "identifier": "pap",
        "name": "Papiamento",
        "alternate_name": "Papiamentu",
        "direction": "ltr"
    },
    {
        "identifier": "se",
        "name": "Northern Sami",
        "alternate_name": "davvisámegiella",
        "direction": "ltr"
    },
    {
        "identifier": "fi",
        "name": "Finnish",
        "alternate_name": "suomi",
        "direction": "ltr"
    },
    {
        "identifier": "ki",
        "name": "Kikuyu",
        "alternate_name": "Gĩkũyũ",
        "direction": "ltr"
    },
    {
        "identifier": "mwl",
        "name": "Mirandese",
        "alternate_name": "Mirandés",
        "direction": "ltr"
    },
    {
        "identifier": "pcm",
        "name": "Nigerian Pidgin",
        "alternate_name": "Naijá",
        "direction": "ltr"
    },
    {
        "identifier": "ext",
        "name": "Extremaduran",
        "alternate_name": "estremeñu",
        "direction": "ltr"
    },
    {
        "identifier": "haw",
        "name": "Hawaiian",
        "alternate_name": "Hawaiʻi",
        "direction": "ltr"
    },
    {
        "identifier": "nia",
        "name": "Nias",
        "alternate_name": "Li Niha",
        "direction": "ltr"
    },
    {
        "identifier": "ru",
        "name": "Russian",
        "alternate_name": "русский",
        "direction": "ltr"
    },
    {
        "identifier": "nn",
        "name": "Norwegian Nynorsk",
        "alternate_name": "norsk nynorsk",
        "direction": "ltr"
    },
    {
        "identifier": "ay",
        "name": "Aymara",
        "alternate_name": "Aymar aru",
        "direction": "ltr"
    },
    {
        "identifier": "gd",
        "name": "Scottish Gaelic",
        "alternate_name": "Gàidhlig",
        "direction": "ltr"
    },
    {
        "identifier": "roa-tara",
        "name": "Tarantino",
        "alternate_name": "tarandíne",
        "direction": "ltr"
    },
    {
        "identifier": "sat",
        "name": "Santali",
        "alternate_name": "ᱥᱟᱱᱛᱟᱲᱤ",
        "direction": "ltr"
    },
    {
        "identifier": "su",
        "name": "Sundanese",
        "alternate_name": "Sunda",
        "direction": "ltr"
    },
    {
        "identifier": "bm",
        "name": "Bambara",
        "alternate_name": "bamanankan",
        "direction": "ltr"
    },
    {
        "identifier": "ee",
        "name": "Ewe",
        "alternate_name": "eʋegbe",
        "direction": "ltr"
    },
    {
        "identifier": "he",
        "name": "Hebrew",
        "alternate_name": "עברית",
        "direction": "rtl"
    },
    {
        "identifier": "jam",
        "name": "Jamaican Creole English",
        "alternate_name": "Patois",
        "direction": "ltr"
    },
    {
        "identifier": "ug",
        "name": "Uyghur",
        "alternate_name": "ئۇيغۇرچە / Uyghurche",
        "direction": "rtl"
    },
    {
        "identifier": "xh",
        "name": "Xhosa",
        "alternate_name": "isiXhosa",
        "direction": "ltr"
    },
    {
        "identifier": "as",
        "name": "Assamese",
        "alternate_name": "অসমীয়া",
        "direction": "ltr"
    },
    {
        "identifier": "az",
        "name": "Azerbaijani",
        "alternate_name": "azərbaycanca",
        "direction": "ltr"
    },
    {
        "identifier": "blk",
        "name": "Pa'O",
        "alternate_name": "ပအိုဝ်ႏဘာႏသာႏ",
        "direction": "ltr"
    },
    {
        "identifier": "lb",
        "name": "Luxembourgish",
        "alternate_name": "Lëtzebuergesch",
        "direction": "ltr"
    },
    {
        "identifier": "mad",
        "name": "Madurese",
        "alternate_name": "Madhurâ",
        "direction": "ltr"
    },
    {
        "identifier": "nap",
        "name": "Neapolitan",
        "alternate_name": "Napulitano",
        "direction": "ltr"
    },
    {
        "identifier": "tay",
        "name": "Tayal",
        "alternate_name": "Tayal",
        "direction": "ltr"
    },
    {
        "identifier": "ba",
        "name": "Bashkir",
        "alternate_name": "башҡортса",
        "direction": "ltr"
    },
    {
        "identifier": "ceb",
        "name": "Cebuano",
        "alternate_name": "Cebuano",
        "direction": "ltr"
    },
    {
        "identifier": "mrj",
        "name": "Western Mari",
        "alternate_name": "кырык мары",
        "direction": "ltr"
    },
    {
        "identifier": "tw",
        "name": "Twi",
        "alternate_name": "Twi",
        "direction": "ltr"
    },
    {
        "identifier": "gag",
        "name": "Gagauz",
        "alternate_name": "Gagauz",
        "direction": "ltr"
    },
    {
        "identifier": "simple",
        "name": "Simple English",
        "alternate_name": "Simple English",
        "direction": "ltr"
    },
    {
        "identifier": "stq",
        "name": "Saterland Frisian",
        "alternate_name": "Seeltersk",
        "direction": "ltr"
    },
    {
        "identifier": "aa",
        "name": "Afar",
        "alternate_name": "Qafár af",
        "direction": "ltr"
    },
    {
        "identifier": "ast",
        "name": "Asturian",
        "alternate_name": "asturianu",
        "direction": "ltr"
    },
    {
        "identifier": "kl",
        "name": "Kalaallisut",
        "alternate_name": "kalaallisut",
        "direction": "ltr"
    },
    {
        "identifier": "zh-yue",
        "name": "Cantonese",
        "alternate_name": "粵語",
        "direction": "ltr"
    },
    {
        "identifier": "ar",
        "name": "Arabic",
        "alternate_name": "العربية",
        "direction": "rtl"
    },
    {
        "identifier": "dty",
        "name": "Doteli",
        "alternate_name": "डोटेली",
        "direction": "ltr"
    },
    {
        "identifier": "guw",
        "name": "Gun",
        "alternate_name": "gungbe",
        "direction": "ltr"
    },
    {
        "identifier": "lrc",
        "name": "Northern Luri",
        "alternate_name": "لۊری شومالی",
        "direction": "rtl"
    },
    {
        "identifier": "ti",
        "name": "Tigrinya",
        "alternate_name": "ትግርኛ",
        "direction": "ltr"
    },
    {
        "identifier": "tt",
        "name": "Tatar",
        "alternate_name": "татарча / tatarça",
        "direction": "ltr"
    },
    {
        "identifier": "bs",
        "name": "Bosnian",
        "alternate_name": "bosanski",
        "direction": "ltr"
    },
    {
        "identifier": "lij",
        "name": "Ligurian",
        "alternate_name": "Ligure",
        "direction": "ltr"
    },
    {
        "identifier": "min",
        "name": "Minangkabau",
        "alternate_name": "Minangkabau",
        "direction": "ltr"
    },
    {
        "identifier": "olo",
        "name": "Livvi-Karelian",
        "alternate_name": "livvinkarjala",
        "direction": "ltr"
    },
    {
        "identifier": "si",
        "name": "Sinhala",
        "alternate_name": "සිංහල",
        "direction": "ltr"
    },
    {
        "identifier": "ami",
        "name": "Amis",
        "alternate_name": "Pangcah",
        "direction": "ltr"
    },
    {
        "identifier": "es",
        "name": "Spanish",
        "alternate_name": "español",
        "direction": "ltr"
    },
    {
        "identifier": "pag",
        "name": "Pangasinan",
        "alternate_name": "Pangasinan",
        "direction": "ltr"
    },
    {
        "identifier": "pt",
        "name": "Portuguese",
        "alternate_name": "português",
        "direction": "ltr"
    },
    {
        "identifier": "gpe",
        "name": "Ghanaian Pidgin",
        "alternate_name": "Ghanaian Pidgin",
        "direction": "ltr"
    },
    {
        "identifier": "guc",
        "name": "Wayuu",
        "alternate_name": "wayuunaiki",
        "direction": "ltr"
    },
    {
        "identifier": "hu",
        "name": "Hungarian",
        "alternate_name": "magyar",
        "direction": "ltr"
    },
    {
        "identifier": "li",
        "name": "Limburgish",
        "alternate_name": "Limburgs",
        "direction": "ltr"
    },
    {
        "identifier": "pwn",
        "name": "Paiwan",
        "alternate_name": "pinayuanan",
        "direction": "ltr"
    },
    {
        "identifier": "ta",
        "name": "Tamil",
        "alternate_name": "தமிழ்",
        "direction": "ltr"
    },
    {
        "identifier": "wa",
        "name": "Walloon",
        "alternate_name": "walon",
        "direction": "ltr"
    },
    {
        "identifier": "bh",
        "name": "Bhojpuri",
        "alternate_name": "भोजपुरी",
        "direction": "ltr"
    },
    {
        "identifier": "cu",
        "name": "Church Slavic",
        "alternate_name": "словѣньскъ / ⰔⰎⰑⰂⰡⰐⰠⰔⰍⰟ",
        "direction": "ltr"
    },
    {
        "identifier": "lmo",
        "name": "Lombard",
        "alternate_name": "lombard",
        "direction": "ltr"
    },
    {
        "identifier": "pms",
        "name": "Piedmontese",
        "alternate_name": "Piemontèis",
        "direction": "ltr"
    },
    {
        "identifier": "rmy",
        "name": "Vlax Romani",
        "alternate_name": "romani čhib",
        "direction": "ltr"
    },
    {
        "identifier": "sc",
        "name": "Sardinian",
        "alternate_name": "sardu",
        "direction": "ltr"
    },
    {
        "identifier": "ty",
        "name": "Tahitian",
        "alternate_name": "reo tahiti",
        "direction": "ltr"
    },
    {
        "identifier": "ig",
        "name": "Igbo",
        "alternate_name": "Igbo",
        "direction": "ltr"
    },
    {
        "identifier": "ng",
        "name": "Ndonga",
        "alternate_name": "Oshiwambo",
        "direction": "ltr"
    },
    {
        "identifier": "roa-rup",
        "name": "Aromanian",
        "alternate_name": "armãneashti",
        "direction": "ltr"
    },
    {
        "identifier": "uz",
        "name": "Uzbek",
        "alternate_name": "oʻzbekcha / ўзбекча",
        "direction": "ltr"
    },
    {
        "identifier": "awa",
        "name": "Awadhi",
        "alternate_name": "अवधी",
        "direction": "ltr"
    },
    {
        "identifier": "azb",
        "name": "South Azerbaijani",
        "alternate_name": "تۆرکجه",
        "direction": "rtl"
    },
    {
        "identifier": "fiu-vro",
        "name": "võro",
        "alternate_name": "võro",
        "direction": "ltr"
    },
    {
        "identifier": "gv",
        "name": "Manx",
        "alternate_name": "Gaelg",
        "direction": "ltr"
    },
    {
        "identifier": "ro",
        "name": "Romanian",
        "alternate_name": "română",
        "direction": "ltr"
    },
    {
        "identifier": "sa",
        "name": "Sanskrit",
        "alternate_name": "संस्कृतम्",
        "direction": "ltr"
    },
    {
        "identifier": "sg",
        "name": "Sango",
        "alternate_name": "Sängö",
        "direction": "ltr"
    },
    {
        "identifier": "ve",
        "name": "Venda",
        "alternate_name": "Tshivenda",
        "direction": "ltr"
    },
    {
        "identifier": "wo",
        "name": "Wolof",
        "alternate_name": "Wolof",
        "direction": "ltr"
    },
    {
        "identifier": "cy",
        "name": "Welsh",
        "alternate_name": "Cymraeg",
        "direction": "ltr"
    },
    {
        "identifier": "dz",
        "name": "Dzongkha",
        "alternate_name": "ཇོང་ཁ",
        "direction": "ltr"
    },
    {
        "identifier": "ht",
        "name": "Haitian Creole",
        "alternate_name": "Kreyòl ayisyen",
        "direction": "ltr"
    },
    {
        "identifier": "be",
        "name": "Belarusian",
        "alternate_name": "беларуская",
        "direction": "ltr"
    },
    {
        "identifier": "ckb",
        "name": "Central Kurdish",
        "alternate_name": "کوردی",
        "direction": "rtl"
    },
    {
        "identifier": "eml",
        "name": "Emiliano-Romagnolo",
        "alternate_name": "emiliàn e rumagnòl",
        "direction": "ltr"
    },
    {
        "identifier": "kr",
        "name": "Kanuri",
        "alternate_name": "kanuri",
        "direction": "ltr"
    },
    {
        "identifier": "th",
        "name": "Thai",
        "alternate_name": "ไทย",
        "direction": "ltr"
    },
    {
        "identifier": "udm",
        "name": "Udmurt",
        "alternate_name": "удмурт",
        "direction": "ltr"
    },
    {
        "identifier": "el",
        "name": "Greek",
        "alternate_name": "Ελληνικά",
        "direction": "ltr"
    },
    {
        "identifier": "io",
        "name": "Ido",
        "alternate_name": "Ido",
        "direction": "ltr"
    },
    {
        "identifier": "pih",
        "name": "Norfuk / Pitkern",
        "alternate_name": "Norfuk / Pitkern",
        "direction": "ltr"
    },
    {
        "identifier": "sd",
        "name": "Sindhi",
        "alternate_name": "سنڌي",
        "direction": "rtl"
    },
    {
        "identifier": "sw",
        "name": "Swahili",
        "alternate_name": "Kiswahili",
        "direction": "ltr"
    },
    {
        "identifier": "xal",
        "name": "Kalmyk",
        "alternate_name": "хальмг",
        "direction": "ltr"
    },
    {
        "identifier": "hr",
        "name": "Croatian",
        "alternate_name": "hrvatski",
        "direction": "ltr"
    },
    {
        "identifier": "na",
        "name": "Nauru",
        "alternate_name": "Dorerin Naoero",
        "direction": "ltr"
    },
    {
        "identifier": "shy",
        "name": "Shawiya",
        "alternate_name": "tacawit",
        "direction": "ltr"
    },
    {
        "identifier": "sr",
        "name": "Serbian",
        "alternate_name": "српски / srpski",
        "direction": "ltr"
    },
    {
        "identifier": "ksh",
        "name": "Colognian",
        "alternate_name": "Ripoarisch",
        "direction": "ltr"
    },
    {
        "identifier": "lad",
        "name": "Ladino",
        "alternate_name": "Ladino",
        "direction": "ltr"
    },
    {
        "identifier": "ms",
        "name": "Malay",
        "alternate_name": "Bahasa Melayu",
        "direction": "ltr"
    },
    {
        "identifier": "tg",
        "name": "Tajik",
        "alternate_name": "тоҷикӣ",
        "direction": "ltr"
    },
    {
        "identifier": "bar",
        "name": "Bavarian",
        "alternate_name": "Boarisch",
        "direction": "ltr"
    },
    {
        "identifier": "zh",
        "name": "Chinese",
        "alternate_name": "中文",
        "direction": "ltr"
    },
    {
        "identifier": "vep",
        "name": "Veps",
        "alternate_name": "vepsän kel’",
        "direction": "ltr"
    },
    {
        "identifier": "fr",
        "name": "French",
        "alternate_name": "français",
        "direction": "ltr"
    },
    {
        "identifier": "kcg",
        "name": "Tyap",
        "alternate_name": "Tyap",
        "direction": "ltr"
    },
    {
        "identifier": "ny",
        "name": "Nyanja",
        "alternate_name": "Chi-Chewa",
        "direction": "ltr"
    },
    {
        "identifier": "pam",
        "name": "Pampanga",
        "alternate_name": "Kapampangan",
        "direction": "ltr"
    },
    {
        "identifier": "sah",
        "name": "Yakut",
        "alternate_name": "саха тыла",
        "direction": "ltr"
    },
    {
        "identifier": "shn",
        "name": "Shan",
        "alternate_name": "ၽႃႇသႃႇတႆး ",
        "direction": "ltr"
    },
    {
        "identifier": "sq",
        "name": "Albanian",
        "alternate_name": "shqip",
        "direction": "ltr"
    },
    {
        "identifier": "be-tarask",
        "name": "Belarusian (Taraškievica orthography)",
        "alternate_name": "беларуская (тарашкевіца)",
        "direction": "ltr"
    },
    {
        "identifier": "bi",
        "name": "Bislama",
        "alternate_name": "Bislama",
        "direction": "ltr"
    },
    {
        "identifier": "szy",
        "name": "Sakizaya",
        "alternate_name": "Sakizaya",
        "direction": "ltr"
    },
    {
        "identifier": "tk",
        "name": "Turkmen",
        "alternate_name": "Türkmençe",
        "direction": "ltr"
    },
    {
        "identifier": "got",
        "name": "Gothic",
        "alternate_name": "𐌲𐌿𐍄𐌹𐍃𐌺",
        "direction": "ltr"
    },
    {
        "identifier": "hak",
        "name": "Hakka Chinese",
        "alternate_name": "客家語/Hak-kâ-ngî",
        "direction": "ltr"
    },
    {
        "identifier": "mn",
        "name": "Mongolian",
        "alternate_name": "монгол",
        "direction": "ltr"
    },
    {
        "identifier": "tyv",
        "name": "Tuvinian",
        "alternate_name": "тыва дыл",
        "direction": "ltr"
    },
    {
        "identifier": "om",
        "name": "Oromo",
        "alternate_name": "Oromoo",
        "direction": "ltr"
    },
    {
        "identifier": "alt",
        "name": "Southern Altai",
        "alternate_name": "алтай тил",
        "direction": "ltr"
    },
    {
        "identifier": "bo",
        "name": "Tibetan",
        "alternate_name": "བོད་ཡིག",
        "direction": "ltr"
    },
    {
        "identifier": "diq",
        "name": "Zazaki",
        "alternate_name": "Zazaki",
        "direction": "ltr"
    },
    {
        "identifier": "fy",
        "name": "Western Frisian",
        "alternate_name": "Frysk",
        "direction": "ltr"
    },
    {
        "identifier": "ie",
        "name": "Interlingue",
        "alternate_name": "Interlingue",
        "direction": "ltr"
    },
    {
        "identifier": "lv",
        "name": "Latvian",
        "alternate_name": "latviešu",
        "direction": "ltr"
    },
    {
        "identifier": "mni",
        "name": "Manipuri",
        "alternate_name": "ꯃꯤꯇꯩ ꯂꯣꯟ",
        "direction": "ltr"
    },
    {
        "identifier": "os",
        "name": "Ossetic",
        "alternate_name": "ирон",
        "direction": "ltr"
    },
    {
        "identifier": "ts",
        "name": "Tsonga",
        "alternate_name": "Xitsonga",
        "direction": "ltr"
    },
    {
        "identifier": "arz",
        "name": "Egyptian Arabic",
        "alternate_name": "مصرى",
        "direction": "rtl"
    },
    {
        "identifier": "ky",
        "name": "Kyrgyz",
        "alternate_name": "кыргызча",
        "direction": "ltr"
    },
    {
        "identifier": "ltg",
        "name": "Latgalian",
        "alternate_name": "latgaļu",
        "direction": "ltr"
    },
    {
        "identifier": "mai",
        "name": "Maithili",
        "alternate_name": "मैथिली",
        "direction": "ltr"
    },
    {
        "identifier": "pnt",
        "name": "Pontic",
        "alternate_name": "Ποντιακά",
        "direction": "ltr"
    },
    {
        "identifier": "fj",
        "name": "Fijian",
        "alternate_name": "Na Vosa Vakaviti",
        "direction": "ltr"
    },
    {
        "identifier": "iu",
        "name": "Inuktitut",
        "alternate_name": "ᐃᓄᒃᑎᑐᑦ / inuktitut",
        "direction": "ltr"
    },
    {
        "identifier": "pl",
        "name": "Polish",
        "alternate_name": "polski",
        "direction": "ltr"
    },
    {
        "identifier": "ady",
        "name": "Adyghe",
        "alternate_name": "адыгабзэ",
        "direction": "ltr"
    },
    {
        "identifier": "cr",
        "name": "Cree",
        "alternate_name": "Nēhiyawēwin / ᓀᐦᐃᔭᐍᐏᐣ",
        "direction": "ltr"
    },
    {
        "identifier": "nl",
        "name": "Dutch",
        "alternate_name": "Nederlands",
        "direction": "ltr"
    },
    {
        "identifier": "qu",
        "name": "Quechua",
        "alternate_name": "Runa Simi",
        "direction": "ltr"
    },
    {
        "identifier": "sl",
        "name": "Slovenian",
        "alternate_name": "slovenščina",
        "direction": "ltr"
    },
    {
        "identifier": "bn",
        "name": "Bangla",
        "alternate_name": "বাংলা",
        "direction": "ltr"
    },
    {
        "identifier": "dag",
        "name": "Dagbani",
        "alternate_name": "dagbanli",
        "direction": "ltr"
    },
    {
        "identifier": "fo",
        "name": "Faroese",
        "alternate_name": "føroyskt",
        "direction": "ltr"
    },
    {
        "identifier": "ho",
        "name": "Hiri Motu",
        "alternate_name": "Hiri Motu",
        "direction": "ltr"
    },
    {
        "identifier": "kg",
        "name": "Kongo",
        "alternate_name": "Kongo",
        "direction": "ltr"
    },
    {
        "identifier": "rm",
        "name": "Romansh",
        "alternate_name": "rumantsch",
        "direction": "ltr"
    },
    {
        "identifier": "tpi",
        "name": "Tok Pisin",
        "alternate_name": "Tok Pisin",
        "direction": "ltr"
    },
    {
        "identifier": "nds-nl",
        "name": "Low Saxon",
        "alternate_name": "Nedersaksies",
        "direction": "ltr"
    },
    {
        "identifier": "ak",
        "name": "Akan",
        "alternate_name": "Akan",
        "direction": "ltr"
    },
    {
        "identifier": "ban",
        "name": "Balinese",
        "alternate_name": "Basa Bali",
        "direction": "ltr"
    },
    {
        "identifier": "hy",
        "name": "Armenian",
        "alternate_name": "հայերեն",
        "direction": "ltr"
    },
    {
        "identifier": "jbo",
        "name": "Lojban",
        "alternate_name": "la .lojban.",
        "direction": "ltr"
    },
    {
        "identifier": "km",
        "name": "Khmer",
        "alternate_name": "ភាសាខ្មែរ",
        "direction": "ltr"
    },
    {
        "identifier": "lbe",
        "name": "Lak",
        "alternate_name": "лакку",
        "direction": "ltr"
    },
    {
        "identifier": "lfn",
        "name": "Lingua Franca Nova",
        "alternate_name": "Lingua Franca Nova",
        "direction": "ltr"
    },
    {
        "identifier": "bcl",
        "name": "Central Bikol",
        "alternate_name": "Bikol Central",
        "direction": "ltr"
    },
    {
        "identifier": "hyw",
        "name": "Western Armenian",
        "alternate_name": "Արեւմտահայերէն",
        "direction": "ltr"
    },
    {
        "identifier": "kk",
        "name": "Kazakh",
        "alternate_name": "қазақша",
        "direction": "ltr"
    },
    {
        "identifier": "ang",
        "name": "Old English",
        "alternate_name": "Ænglisc",
        "direction": "ltr"
    },
    {
        "identifier": "atj",
        "name": "Atikamekw",
        "alternate_name": "Atikamekw",
        "direction": "ltr"
    },
    {
        "identifier": "be-x-old",
        "name": "Belarusian (Taraškievica orthography)",
        "alternate_name": "беларуская (тарашкевіца)",
        "direction": "ltr"
    },
    {
        "identifier": "br",
        "name": "Breton",
        "alternate_name": "brezhoneg",
        "direction": "ltr"
    },
    {
        "identifier": "gcr",
        "name": "Guianan Creole",
        "alternate_name": "kriyòl gwiyannen",
        "direction": "ltr"
    },
    {
        "identifier": "hi",
        "name": "Hindi",
        "alternate_name": "हिन्दी",
        "direction": "ltr"
    },
    {
        "identifier": "ab",
        "name": "Abkhazian",
        "alternate_name": "аԥсшәа",
        "direction": "ltr"
    },
    {
        "identifier": "bjn",
        "name": "Banjar",
        "alternate_name": "Banjar",
        "direction": "ltr"
    },
    {
        "identifier": "hsb",
        "name": "Upper Sorbian",
        "alternate_name": "hornjoserbsce",
        "direction": "ltr"
    },
    {
        "identifier": "mus",
        "name": "Muscogee",
        "alternate_name": "Mvskoke",
        "direction": "ltr"
    },
    {
        "identifier": "myv",
        "name": "Erzya",
        "alternate_name": "эрзянь",
        "direction": "ltr"
    },
    {
        "identifier": "wuu",
        "name": "Wu Chinese",
        "alternate_name": "吴语",
        "direction": "ltr"
    },
    {
        "identifier": "bg",
        "name": "Bulgarian",
        "alternate_name": "български",
        "direction": "ltr"
    },
    {
        "identifier": "co",
        "name": "Corsican",
        "alternate_name": "corsu",
        "direction": "ltr"
    },
    {
        "identifier": "cs",
        "name": "Czech",
        "alternate_name": "čeština",
        "direction": "ltr"
    },
    {
        "identifier": "fur",
        "name": "Friulian",
        "alternate_name": "furlan",
        "direction": "ltr"
    },
    {
        "identifier": "gan",
        "name": "Gan Chinese",
        "alternate_name": "贛語",
        "direction": "ltr"
    },
    {
        "identifier": "krc",
        "name": "Karachay-Balkar",
        "alternate_name": "къарачай-малкъар",
        "direction": "ltr"
    },
    {
        "identifier": "lg",
        "name": "Ganda",
        "alternate_name": "Luganda",
        "direction": "ltr"
    },
    {
        "identifier": "sco",
        "name": "Scots",
        "alternate_name": "Scots",
        "direction": "ltr"
    },
    {
        "identifier": "mhr",
        "name": "Eastern Mari",
        "alternate_name": "олык марий",
        "direction": "ltr"
    },
    {
        "identifier": "ace",
        "name": "Achinese",
        "alternate_name": "Acèh",
        "direction": "ltr"
    },
    {
        "identifier": "af",
        "name": "Afrikaans",
        "alternate_name": "Afrikaans",
        "direction": "ltr"
    },
    {
        "identifier": "csb",
        "name": "Kashubian",
        "alternate_name": "kaszëbsczi",
        "direction": "ltr"
    },
    {
        "identifier": "frr",
        "name": "Northern Frisian",
        "alternate_name": "Nordfriisk",
        "direction": "ltr"
    },
    {
        "identifier": "gom",
        "name": "Goan Konkani",
        "alternate_name": "गोंयची कोंकणी / Gõychi Konknni",
        "direction": "ltr"
    },
    {
        "identifier": "ia",
        "name": "Interlingua",
        "alternate_name": "interlingua",
        "direction": "ltr"
    },
    {
        "identifier": "mg",
        "name": "Malagasy",
        "alternate_name": "Malagasy",
        "direction": "ltr"
    },
    {
        "identifier": "mt",
        "name": "Maltese",
        "alternate_name": "Malti",
        "direction": "ltr"
    },
    {
        "identifier": "dsb",
        "name": "Lower Sorbian",
        "alternate_name": "dolnoserbski",
        "direction": "ltr"
    },
    {
        "identifier": "koi",
        "name": "Komi-Permyak",
        "alternate_name": "перем коми",
        "direction": "ltr"
    },
    {
        "identifier": "nso",
        "name": "Northern Sotho",
        "alternate_name": "Sesotho sa Leboa",
        "direction": "ltr"
    },
    {
        "identifier": "st",
        "name": "Southern Sotho",
        "alternate_name": "Sesotho",
        "direction": "ltr"
    },
    {
        "identifier": "tum",
        "name": "Tumbuka",
        "alternate_name": "chiTumbuka",
        "direction": "ltr"
    },
    {
        "identifier": "zu",
        "name": "Zulu",
        "alternate_name": "isiZulu",
        "direction": "ltr"
    },
    {
        "identifier": "et",
        "name": "Estonian",
        "alternate_name": "eesti",
        "direction": "ltr"
    },
    {
        "identifier": "ga",
        "name": "Irish",
        "alternate_name": "Gaeilge",
        "direction": "ltr"
    },
    {
        "identifier": "glk",
        "name": "Gilaki",
        "alternate_name": "گیلکی",
        "direction": "rtl"
    },
    {
        "identifier": "sn",
        "name": "Shona",
        "alternate_name": "chiShona",
        "direction": "ltr"
    },
    {
        "identifier": "jv",
        "name": "Javanese",
        "alternate_name": "Jawa",
        "direction": "ltr"
    },
    {
        "identifier": "lez",
        "name": "Lezghian",
        "alternate_name": "лезги",
        "direction": "ltr"
    },
    {
        "identifier": "map-bms",
        "name": "Basa Banyumasan",
        "alternate_name": "Basa Banyumasan",
        "direction": "ltr"
    },
    {
        "identifier": "my",
        "name": "Burmese",
        "alternate_name": "မြန်မာဘာသာ",
        "direction": "ltr"
    },
    {
        "identifier": "pa",
        "name": "Punjabi",
        "alternate_name": "ਪੰਜਾਬੀ",
        "direction": "ltr"
    },
    {
        "identifier": "sh",
        "name": "Serbo-Croatian",
        "alternate_name": "srpskohrvatski / српскохрватски",
        "direction": "ltr"
    },
    {
        "identifier": "gu",
        "name": "Gujarati",
        "alternate_name": "ગુજરાતી",
        "direction": "ltr"
    },
    {
        "identifier": "kj",
        "name": "Kuanyama",
        "alternate_name": "Kwanyama",
        "direction": "ltr"
    },
    {
        "identifier": "lo",
        "name": "Lao",
        "alternate_name": "ລາວ",
        "direction": "ltr"
    },
    {
        "identifier": "mh",
        "name": "Marshallese",
        "alternate_name": "Ebon",
        "direction": "ltr"
    },
    {
        "identifier": "nds",
        "name": "Low German",
        "alternate_name": "Plattdüütsch",
        "direction": "ltr"
    },
    {
        "identifier": "yo",
        "name": "Yoruba",
        "alternate_name": "Yorùbá",
        "direction": "ltr"
    },
    {
        "identifier": "xmf",
        "name": "Mingrelian",
        "alternate_name": "მარგალური",
        "direction": "ltr"
    },
    {
        "identifier": "avk",
        "name": "Kotava",
        "alternate_name": "Kotava",
        "direction": "ltr"
    },
    {
        "identifier": "ca",
        "name": "Catalan",
        "alternate_name": "català",
        "direction": "ltr"
    },
    {
        "identifier": "ii",
        "name": "Sichuan Yi",
        "alternate_name": "ꆇꉙ",
        "direction": "ltr"
    },
    {
        "identifier": "mk",
        "name": "Macedonian",
        "alternate_name": "македонски",
        "direction": "ltr"
    },
    {
        "identifier": "mr",
        "name": "Marathi",
        "alternate_name": "मराठी",
        "direction": "ltr"
    },
    {
        "identifier": "te",
        "name": "Telugu",
        "alternate_name": "తెలుగు",
        "direction": "ltr"
    },
    {
        "identifier": "to",
        "name": "Tongan",
        "alternate_name": "lea faka-Tonga",
        "direction": "ltr"
    },
    {
        "identifier": "an",
        "name": "Aragonese",
        "alternate_name": "aragonés",
        "direction": "ltr"
    },
    {
        "identifier": "bxr",
        "name": "Russia Buriat",
        "alternate_name": "буряад",
        "direction": "ltr"
    },
    {
        "identifier": "ik",
        "name": "Inupiaq",
        "alternate_name": "Iñupiatun",
        "direction": "ltr"
    },
    {
        "identifier": "kbd",
        "name": "Kabardian",
        "alternate_name": "адыгэбзэ",
        "direction": "ltr"
    },
    {
        "identifier": "sm",
        "name": "Samoan",
        "alternate_name": "Gagana Samoa",
        "direction": "ltr"
    },
    {
        "identifier": "arc",
        "name": "Aramaic",
        "alternate_name": "ܐܪܡܝܐ",
        "direction": "rtl"
    },
    {
        "identifier": "ilo",
        "name": "Iloko",
        "alternate_name": "Ilokano",
        "direction": "ltr"
    },
    {
        "identifier": "is",
        "name": "Icelandic",
        "alternate_name": "íslenska",
        "direction": "ltr"
    },
    {
        "identifier": "ko",
        "name": "Korean",
        "alternate_name": "한국어",
        "direction": "ltr"
    },
    {
        "identifier": "ku",
        "name": "Kurdish",
        "alternate_name": "kurdî",
        "direction": "ltr"
    },
    {
        "identifier": "za",
        "name": "Zhuang",
        "alternate_name": "Vahcuengh",
        "direction": "ltr"
    },
    {
        "identifier": "mnw",
        "name": "Mon",
        "alternate_name": "ဘာသာ မန်",
        "direction": "ltr"
    },
    {
        "identifier": "bat-smg",
        "name": "Samogitian",
        "alternate_name": "žemaitėška",
        "direction": "ltr"
    },
    {
        "identifier": "da",
        "name": "Danish",
        "alternate_name": "dansk",
        "direction": "ltr"
    },
    {
        "identifier": "gl",
        "name": "Galician",
        "alternate_name": "galego",
        "direction": "ltr"
    },
    {
        "identifier": "gur",
        "name": "Frafra",
        "alternate_name": "farefare",
        "direction": "ltr"
    },
    {
        "identifier": "hz",
        "name": "Herero",
        "alternate_name": "Otsiherero",
        "direction": "ltr"
    },
    {
        "identifier": "ks",
        "name": "Kashmiri",
        "alternate_name": "कॉशुर / کٲشُر",
        "direction": "rtl"
    },
    {
        "identifier": "mi",
        "name": "Māori",
        "alternate_name": "Māori",
        "direction": "ltr"
    },
    {
        "identifier": "pcd",
        "name": "Picard",
        "alternate_name": "Picard",
        "direction": "ltr"
    },
    {
        "identifier": "pfl",
        "name": "Palatine German",
        "alternate_name": "Pälzisch",
        "direction": "ltr"
    },
    {
        "identifier": "bpy",
        "name": "Bishnupriya",
        "alternate_name": "বিষ্ণুপ্রিয়া মণিপুরী",
        "direction": "ltr"
    },
    {
        "identifier": "crh",
        "name": "Crimean Tatar",
        "alternate_name": "qırımtatarca",
        "direction": "ltr"
    },
    {
        "identifier": "vec",
        "name": "Venetian",
        "alternate_name": "vèneto",
        "direction": "ltr"
    },
    {
        "identifier": "av",
        "name": "Avaric",
        "alternate_name": "авар",
        "direction": "ltr"
    },
    {
        "identifier": "chr",
        "name": "Cherokee",
        "alternate_name": "ᏣᎳᎩ",
        "direction": "ltr"
    },
    {
        "identifier": "rue",
        "name": "Rusyn",
        "alternate_name": "русиньскый",
        "direction": "ltr"
    },
    {
        "identifier": "tcy",
        "name": "Tulu",
        "alternate_name": "ತುಳು",
        "direction": "ltr"
    },
    {
        "identifier": "eu",
        "name": "Basque",
        "alternate_name": "euskara",
        "direction": "ltr"
    },
    {
        "identifier": "gor",
        "name": "Gorontalo",
        "alternate_name": "Bahasa Hulontalo",
        "direction": "ltr"
    },
    {
        "identifier": "hif",
        "name": "Fiji Hindi",
        "alternate_name": "Fiji Hindi",
        "direction": "ltr"
    },
    {
        "identifier": "la",
        "name": "Latin",
        "alternate_name": "Latina",
        "direction": "ltr"
    },
    {
        "identifier": "mdf",
        "name": "Moksha",
        "alternate_name": "мокшень",
        "direction": "ltr"
    },
    {
        "identifier": "pnb",
        "name": "Western Punjabi",
        "alternate_name": "پنجابی",
        "direction": "rtl"
    },
    {
        "identifier": "szl",
        "name": "Silesian",
        "alternate_name": "ślůnski",
        "direction": "ltr"
    },
    {
        "identifier": "anp",
        "name": "Angika",
        "alternate_name": "अंगिका",
        "direction": "ltr"
    },
    {
        "identifier": "ce",
        "name": "Chechen",
        "alternate_name": "нохчийн",
        "direction": "ltr"
    },
    {
        "identifier": "en",
        "name": "English",
        "alternate_name": "English",
        "direction": "ltr"
    },
    {
        "identifier": "kw",
        "name": "Cornish",
        "alternate_name": "kernowek",
        "direction": "ltr"
    },
    {
        "identifier": "sk",
        "name": "Slovak",
        "alternate_name": "slovenčina",
        "direction": "ltr"
    },
    {
        "identifier": "so",
        "name": "Somali",
        "alternate_name": "Soomaaliga",
        "direction": "ltr"
    },
    {
        "identifier": "ss",
        "name": "Swati",
        "alternate_name": "SiSwati",
        "direction": "ltr"
    },
    {
        "identifier": "tl",
        "name": "Tagalog",
        "alternate_name": "Tagalog",
        "direction": "ltr"
    },
    {
        "identifier": "trv",
        "name": "Taroko",
        "alternate_name": "Seediq",
        "direction": "ltr"
    },
    {
        "identifier": "ka",
        "name": "Georgian",
        "alternate_name": "ქართული",
        "direction": "ltr"
    },
    {
        "identifier": "kab",
        "name": "Kabyle",
        "alternate_name": "Taqbaylit",
        "direction": "ltr"
    },
    {
        "identifier": "pdc",
        "name": "Pennsylvania German",
        "alternate_name": "Deitsch",
        "direction": "ltr"
    },
    {
        "identifier": "tet",
        "name": "Tetum",
        "alternate_name": "tetun",
        "direction": "ltr"
    },
    {
        "identifier": "yue",
        "name": "Cantonese",
        "alternate_name": "粵語",
        "direction": "ltr"
    },
    {
        "identifier": "zh-classical",
        "name": "Classical Chinese",
        "alternate_name": "文言",
        "direction": "ltr"
    }
]
```
</details>

ii) Metadata on a specific language, without filter or field selection

```bash
GET https://api.enterprise.wikimedia.com/v2/languages/fr
```

Response:
```json
{
    "identifier": "fr",
    "name": "French",
    "alternate_name": "français",
    "direction": "ltr"
}
```

## Projects metadata
Get information on all the supported projects. Supports filtering and field selection. Allows to query single project.

```bash
GET https://api.enterprise.wikimedia.com/v2/projects
```

<details>
<summary>Response: </summary>

```json
[
    {
        "name": "Википеди",
        "identifier": "cvwiki",
        "url": "https://cv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "cv"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "cvwikibooks",
        "url": "https://cv.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "cv"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "idwiki",
        "url": "https://id.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "id"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "idwiktionary",
        "url": "https://id.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "id"
        }
    },
    {
        "name": "Wikibuku",
        "identifier": "idwikibooks",
        "url": "https://id.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "id"
        }
    },
    {
        "name": "Wikikutip",
        "identifier": "idwikiquote",
        "url": "https://id.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "id"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "idwikisource",
        "url": "https://id.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "id"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "viwiki",
        "url": "https://vi.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "vi"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "viwiktionary",
        "url": "https://vi.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "vi"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "viwikibooks",
        "url": "https://vi.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "vi"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "viwikiquote",
        "url": "https://vi.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "vi"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "viwikisource",
        "url": "https://vi.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "vi"
        }
    },
    {
        "name": "Wikivoyage",
        "identifier": "viwikivoyage",
        "url": "https://vi.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "vi"
        }
    },
    {
        "name": "ވިކިޕީޑިއާ",
        "identifier": "dvwiki",
        "url": "https://dv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "dv"
        }
    },
    {
        "name": "ވިކިރަދީފު",
        "identifier": "dvwiktionary",
        "url": "https://dv.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "dv"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "newwiki",
        "url": "https://new.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "new"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "rwwiki",
        "url": "https://rw.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "rw"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "rwwiktionary",
        "url": "https://rw.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "rw"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "srnwiki",
        "url": "https://srn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "srn"
        }
    },
    {
        "name": "Vikipedio",
        "identifier": "eowiki",
        "url": "https://eo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "eo"
        }
    },
    {
        "name": "Vikivortaro",
        "identifier": "eowiktionary",
        "url": "https://eo.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "eo"
        }
    },
    {
        "name": "Vikilibroj",
        "identifier": "eowikibooks",
        "url": "https://eo.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "eo"
        }
    },
    {
        "name": "Vikinovaĵoj",
        "identifier": "eowikinews",
        "url": "https://eo.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "eo"
        }
    },
    {
        "name": "Vikicitaro",
        "identifier": "eowikiquote",
        "url": "https://eo.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "eo"
        }
    },
    {
        "name": "Vikifontaro",
        "identifier": "eowikisource",
        "url": "https://eo.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "eo"
        }
    },
    {
        "name": "Vikivojaĝo",
        "identifier": "eowikivoyage",
        "url": "https://eo.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "eo"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "kvwiki",
        "url": "https://kv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kv"
        }
    },
    {
        "name": "ویکی‌پدیا",
        "identifier": "mznwiki",
        "url": "https://mzn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mzn"
        }
    },
    {
        "name": "Huiquipedia",
        "identifier": "nahwiki",
        "url": "https://nah.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nah"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "nahwiktionary",
        "url": "https://nah.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "nah"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "nahwikibooks",
        "url": "https://nah.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "nah"
        }
    },
    {
        "name": "विकिपिडिया",
        "identifier": "newiki",
        "url": "https://ne.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ne"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "newiktionary",
        "url": "https://ne.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ne"
        }
    },
    {
        "name": "विकिपुस्तक",
        "identifier": "newikibooks",
        "url": "https://ne.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ne"
        }
    },
    {
        "name": "ߥߞߌߔߘߋߞߎ",
        "identifier": "nqowiki",
        "url": "https://nqo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nqo"
        }
    },
    {
        "name": "Vikipedi",
        "identifier": "trwiki",
        "url": "https://tr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tr"
        }
    },
    {
        "name": "Vikisözlük",
        "identifier": "trwiktionary",
        "url": "https://tr.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "tr"
        }
    },
    {
        "name": "Vikikitap",
        "identifier": "trwikibooks",
        "url": "https://tr.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "tr"
        }
    },
    {
        "name": "Vikihaber",
        "identifier": "trwikinews",
        "url": "https://tr.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "tr"
        }
    },
    {
        "name": "Vikisöz",
        "identifier": "trwikiquote",
        "url": "https://tr.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "tr"
        }
    },
    {
        "name": "Vikikaynak",
        "identifier": "trwikisource",
        "url": "https://tr.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "tr"
        }
    },
    {
        "name": "Vikigezgin",
        "identifier": "trwikivoyage",
        "url": "https://tr.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "tr"
        }
    },
    {
        "name": "Vikipetã",
        "identifier": "gnwiki",
        "url": "https://gn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gn"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "gnwiktionary",
        "url": "https://gn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "gn"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "gnwikibooks",
        "url": "https://gn.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "gn"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "hawiki",
        "url": "https://ha.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ha"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "hawiktionary",
        "url": "https://ha.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ha"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "itwiki",
        "url": "https://it.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "it"
        }
    },
    {
        "name": "Wikizionario",
        "identifier": "itwiktionary",
        "url": "https://it.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "it"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "itwikibooks",
        "url": "https://it.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "it"
        }
    },
    {
        "name": "Wikinotizie",
        "identifier": "itwikinews",
        "url": "https://it.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "it"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "itwikiquote",
        "url": "https://it.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "it"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "itwikisource",
        "url": "https://it.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "it"
        }
    },
    {
        "name": "Wikiversità",
        "identifier": "itwikiversity",
        "url": "https://it.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "it"
        }
    },
    {
        "name": "Wikivoyage",
        "identifier": "itwikivoyage",
        "url": "https://it.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "it"
        }
    },
    {
        "name": "Vikipedija",
        "identifier": "ltwiki",
        "url": "https://lt.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lt"
        }
    },
    {
        "name": "Vikižodynas",
        "identifier": "ltwiktionary",
        "url": "https://lt.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "lt"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "ltwikibooks",
        "url": "https://lt.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "lt"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "ltwikiquote",
        "url": "https://lt.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "lt"
        }
    },
    {
        "name": "Vikišaltiniai",
        "identifier": "ltwikisource",
        "url": "https://lt.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "lt"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "tnwiki",
        "url": "https://tn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tn"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "tnwiktionary",
        "url": "https://tn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "tn"
        }
    },
    {
        "name": "ውክፔዲያ",
        "identifier": "amwiki",
        "url": "https://am.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "am"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "amwiktionary",
        "url": "https://am.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "am"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "amwikiquote",
        "url": "https://am.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "am"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "bugwiki",
        "url": "https://bug.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bug"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "chwiki",
        "url": "https://ch.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ch"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "chwiktionary",
        "url": "https://ch.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ch"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "chwikibooks",
        "url": "https://ch.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ch"
        }
    },
    {
        "name": "വിക്കിപീഡിയ",
        "identifier": "mlwiki",
        "url": "https://ml.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ml"
        }
    },
    {
        "name": "വിക്കിനിഘണ്ടു",
        "identifier": "mlwiktionary",
        "url": "https://ml.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ml"
        }
    },
    {
        "name": "വിക്കിപാഠശാല",
        "identifier": "mlwikibooks",
        "url": "https://ml.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ml"
        }
    },
    {
        "name": "വിക്കിചൊല്ലുകൾ",
        "identifier": "mlwikiquote",
        "url": "https://ml.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ml"
        }
    },
    {
        "name": "വിക്കിഗ്രന്ഥശാല",
        "identifier": "mlwikisource",
        "url": "https://ml.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ml"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "nrmwiki",
        "url": "https://nrm.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nrm"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "nvwiki",
        "url": "https://nv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nv"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "scnwiki",
        "url": "https://scn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "scn"
        }
    },
    {
        "name": "Wikizziunariu",
        "identifier": "scnwiktionary",
        "url": "https://scn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "scn"
        }
    },
    {
        "name": "װיקיפּעדיע",
        "identifier": "yiwiki",
        "url": "https://yi.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "yi"
        }
    },
    {
        "name": "װיקיװערטערבוך",
        "identifier": "yiwiktionary",
        "url": "https://yi.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "yi"
        }
    },
    {
        "name": "װיקיביבליאָטעק",
        "identifier": "yiwikisource",
        "url": "https://yi.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "yi"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "shiwiki",
        "url": "https://shi.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "shi"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "alswiki",
        "url": "https://als.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "als"
        }
    },
    {
        "name": "ويكيپيديا",
        "identifier": "arywiki",
        "url": "https://ary.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ary"
        }
    },
    {
        "name": "Wikikamus",
        "identifier": "btmwiktionary",
        "url": "https://btm.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "btm"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "cdowiki",
        "url": "https://cdo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "cdo"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "jawiki",
        "url": "https://ja.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ja"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "jawiktionary",
        "url": "https://ja.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ja"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "jawikibooks",
        "url": "https://ja.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ja"
        }
    },
    {
        "name": "ウィキニュース",
        "identifier": "jawikinews",
        "url": "https://ja.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "ja"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "jawikiquote",
        "url": "https://ja.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ja"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "jawikisource",
        "url": "https://ja.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ja"
        }
    },
    {
        "name": "ウィキバーシティ",
        "identifier": "jawikiversity",
        "url": "https://ja.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "ja"
        }
    },
    {
        "name": "ウィキボヤージュ",
        "identifier": "jawikivoyage",
        "url": "https://ja.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "ja"
        }
    },
    {
        "name": "Wikipediya",
        "identifier": "kbpwiki",
        "url": "https://kbp.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kbp"
        }
    },
    {
        "name": "Wikipèdia",
        "identifier": "ocwiki",
        "url": "https://oc.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "oc"
        }
    },
    {
        "name": "Wikiccionari",
        "identifier": "ocwiktionary",
        "url": "https://oc.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "oc"
        }
    },
    {
        "name": "Wikilibres",
        "identifier": "ocwikibooks",
        "url": "https://oc.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "oc"
        }
    },
    {
        "name": "وکیپیڈیا",
        "identifier": "skrwiki",
        "url": "https://skr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "skr"
        }
    },
    {
        "name": "وکشنری",
        "identifier": "skrwiktionary",
        "url": "https://skr.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "skr"
        }
    },
    {
        "name": "Vükiped",
        "identifier": "vowiki",
        "url": "https://vo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "vo"
        }
    },
    {
        "name": "Vükivödabuk",
        "identifier": "vowiktionary",
        "url": "https://vo.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "vo"
        }
    },
    {
        "name": "Vükibuks",
        "identifier": "vowikibooks",
        "url": "https://vo.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "vo"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "vowikiquote",
        "url": "https://vo.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "vo"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "dinwiki",
        "url": "https://din.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "din"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "ffwiki",
        "url": "https://ff.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ff"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "lldwiki",
        "url": "https://lld.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lld"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "novwiki",
        "url": "https://nov.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nov"
        }
    },
    {
        "name": "ویکیپیڈیا",
        "identifier": "urwiki",
        "url": "https://ur.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ur"
        }
    },
    {
        "name": "ویکی لغت",
        "identifier": "urwiktionary",
        "url": "https://ur.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ur"
        }
    },
    {
        "name": "ویکی کتب",
        "identifier": "urwikibooks",
        "url": "https://ur.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ur"
        }
    },
    {
        "name": "ویکی اقتباس",
        "identifier": "urwikiquote",
        "url": "https://ur.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ur"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "zeawiki",
        "url": "https://zea.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "zea"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "fatwiki",
        "url": "https://fat.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "fat"
        }
    },
    {
        "name": "Vouiquipèdia",
        "identifier": "frpwiki",
        "url": "https://frp.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "frp"
        }
    },
    {
        "name": "Википеди",
        "identifier": "inhwiki",
        "url": "https://inh.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "inh"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "piwiki",
        "url": "https://pi.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pi"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "piwiktionary",
        "url": "https://pi.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "pi"
        }
    },
    {
        "name": "ವಿಕಿಪೀಡಿಯ",
        "identifier": "knwiki",
        "url": "https://kn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kn"
        }
    },
    {
        "name": "ವಿಕ್ಷನರಿ",
        "identifier": "knwiktionary",
        "url": "https://kn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "kn"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "knwikibooks",
        "url": "https://kn.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "kn"
        }
    },
    {
        "name": "ವಿಕಿಕೋಟ್",
        "identifier": "knwikiquote",
        "url": "https://kn.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "kn"
        }
    },
    {
        "name": "ವಿಕಿಸೋರ್ಸ್",
        "identifier": "knwikisource",
        "url": "https://kn.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "kn"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "nowiki",
        "url": "https://no.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "no"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "nowiktionary",
        "url": "https://no.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "no"
        }
    },
    {
        "name": "Wikibøker",
        "identifier": "nowikibooks",
        "url": "https://no.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "no"
        }
    },
    {
        "name": "Wikinytt",
        "identifier": "nowikinews",
        "url": "https://no.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "no"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "nowikiquote",
        "url": "https://no.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "no"
        }
    },
    {
        "name": "Wikikilden",
        "identifier": "nowikisource",
        "url": "https://no.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "no"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "rnwiki",
        "url": "https://rn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "rn"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "rnwiktionary",
        "url": "https://rn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "rn"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "lnwiki",
        "url": "https://ln.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ln"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "lnwiktionary",
        "url": "https://ln.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ln"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "lnwikibooks",
        "url": "https://ln.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ln"
        }
    },
    {
        "name": "ويکيپېډيا",
        "identifier": "pswiki",
        "url": "https://ps.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ps"
        }
    },
    {
        "name": "ويکيسيند",
        "identifier": "pswiktionary",
        "url": "https://ps.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ps"
        }
    },
    {
        "name": "ويکيتابونه",
        "identifier": "pswikibooks",
        "url": "https://ps.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ps"
        }
    },
    {
        "name": "ويکيسفر",
        "identifier": "pswikivoyage",
        "url": "https://ps.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "ps"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "svwiki",
        "url": "https://sv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sv"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "svwiktionary",
        "url": "https://sv.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sv"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "svwikibooks",
        "url": "https://sv.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "sv"
        }
    },
    {
        "name": "Wikinews",
        "identifier": "svwikinews",
        "url": "https://sv.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "sv"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "svwikiquote",
        "url": "https://sv.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "sv"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "svwikisource",
        "url": "https://sv.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "sv"
        }
    },
    {
        "name": "Wikiversity",
        "identifier": "svwikiversity",
        "url": "https://sv.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "sv"
        }
    },
    {
        "name": "Wikivoyage",
        "identifier": "svwikivoyage",
        "url": "https://sv.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "sv"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "warwiki",
        "url": "https://war.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "war"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "chowiki",
        "url": "https://cho.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "cho"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "smnwiki",
        "url": "https://smn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "smn"
        }
    },
    {
        "name": "Вікіпедія",
        "identifier": "ukwiki",
        "url": "https://uk.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "uk"
        }
    },
    {
        "name": "Вікісловник",
        "identifier": "ukwiktionary",
        "url": "https://uk.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "uk"
        }
    },
    {
        "name": "Вікіпідручник",
        "identifier": "ukwikibooks",
        "url": "https://uk.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "uk"
        }
    },
    {
        "name": "Вікіновини",
        "identifier": "ukwikinews",
        "url": "https://uk.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "uk"
        }
    },
    {
        "name": "Вікіцитати",
        "identifier": "ukwikiquote",
        "url": "https://uk.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "uk"
        }
    },
    {
        "name": "Вікіджерела",
        "identifier": "ukwikisource",
        "url": "https://uk.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "uk"
        }
    },
    {
        "name": "Вікімандри",
        "identifier": "ukwikivoyage",
        "url": "https://uk.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "uk"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "vlswiki",
        "url": "https://vls.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "vls"
        }
    },
    {
        "name": "ویکی‌پدیا",
        "identifier": "fawiki",
        "url": "https://fa.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "fa"
        }
    },
    {
        "name": "ویکی‌واژه",
        "identifier": "fawiktionary",
        "url": "https://fa.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "fa"
        }
    },
    {
        "name": "ویکی‌کتاب",
        "identifier": "fawikibooks",
        "url": "https://fa.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "fa"
        }
    },
    {
        "name": "ویکی‌خبر",
        "identifier": "fawikinews",
        "url": "https://fa.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "fa"
        }
    },
    {
        "name": "ویکی‌گفتاورد",
        "identifier": "fawikiquote",
        "url": "https://fa.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "fa"
        }
    },
    {
        "name": "ویکی‌نبشته",
        "identifier": "fawikisource",
        "url": "https://fa.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "fa"
        }
    },
    {
        "name": "ویکی‌سفر",
        "identifier": "fawikivoyage",
        "url": "https://fa.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "fa"
        }
    },
    {
        "name": "ଉଇକିପିଡ଼ିଆ",
        "identifier": "orwiki",
        "url": "https://or.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "or"
        }
    },
    {
        "name": "ଉଇକିଅଭିଧାନ",
        "identifier": "orwiktionary",
        "url": "https://or.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "or"
        }
    },
    {
        "name": "ଉଇକିପାଠାଗାର",
        "identifier": "orwikisource",
        "url": "https://or.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "or"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "zh_min_nanwiki",
        "url": "https://zh-min-nan.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "zh-min-nan"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "zh_min_nanwiktionary",
        "url": "https://zh-min-nan.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "zh-min-nan"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "zh_min_nanwikibooks",
        "url": "https://zh-min-nan.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "zh-min-nan"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "zh_min_nanwikiquote",
        "url": "https://zh-min-nan.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "zh-min-nan"
        }
    },
    {
        "name": "Wiki Tô·-su-kóan",
        "identifier": "zh_min_nanwikisource",
        "url": "https://zh-min-nan.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "zh-min-nan"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "cbk_zamwiki",
        "url": "https://cbk-zam.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "cbk-zam"
        }
    },
    {
        "name": "Tsétsêhéstâhese Wikipedia",
        "identifier": "chywiki",
        "url": "https://chy.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "chy"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "dewiki",
        "url": "https://de.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "de"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "dewiktionary",
        "url": "https://de.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "de"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "dewikibooks",
        "url": "https://de.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "de"
        }
    },
    {
        "name": "Wikinews",
        "identifier": "dewikinews",
        "url": "https://de.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "de"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "dewikiquote",
        "url": "https://de.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "de"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "dewikisource",
        "url": "https://de.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "de"
        }
    },
    {
        "name": "Wikiversity",
        "identifier": "dewikiversity",
        "url": "https://de.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "de"
        }
    },
    {
        "name": "Wikivoyage",
        "identifier": "dewikivoyage",
        "url": "https://de.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "de"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "kaawiki",
        "url": "https://kaa.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kaa"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "papwiki",
        "url": "https://pap.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pap"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "sewiki",
        "url": "https://se.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "se"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "sewikibooks",
        "url": "https://se.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "se"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "fiwiki",
        "url": "https://fi.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "fi"
        }
    },
    {
        "name": "Wikisanakirja",
        "identifier": "fiwiktionary",
        "url": "https://fi.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "fi"
        }
    },
    {
        "name": "Wikikirjasto",
        "identifier": "fiwikibooks",
        "url": "https://fi.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "fi"
        }
    },
    {
        "name": "Wikiuutiset",
        "identifier": "fiwikinews",
        "url": "https://fi.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "fi"
        }
    },
    {
        "name": "Wikisitaatit",
        "identifier": "fiwikiquote",
        "url": "https://fi.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "fi"
        }
    },
    {
        "name": "Wikiaineisto",
        "identifier": "fiwikisource",
        "url": "https://fi.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "fi"
        }
    },
    {
        "name": "Wikiopisto",
        "identifier": "fiwikiversity",
        "url": "https://fi.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "fi"
        }
    },
    {
        "name": "Wikimatkat",
        "identifier": "fiwikivoyage",
        "url": "https://fi.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "fi"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "kiwiki",
        "url": "https://ki.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ki"
        }
    },
    {
        "name": "Biquipédia",
        "identifier": "mwlwiki",
        "url": "https://mwl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mwl"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "pcmwiki",
        "url": "https://pcm.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pcm"
        }
    },
    {
        "name": "Güiquipeya",
        "identifier": "extwiki",
        "url": "https://ext.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ext"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "hawwiki",
        "url": "https://haw.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "haw"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "niawiki",
        "url": "https://nia.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nia"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "niawiktionary",
        "url": "https://nia.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "nia"
        }
    },
    {
        "name": "Википедия",
        "identifier": "ruwiki",
        "url": "https://ru.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ru"
        }
    },
    {
        "name": "Викисловарь",
        "identifier": "ruwiktionary",
        "url": "https://ru.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ru"
        }
    },
    {
        "name": "Викиучебник",
        "identifier": "ruwikibooks",
        "url": "https://ru.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ru"
        }
    },
    {
        "name": "Викиновости",
        "identifier": "ruwikinews",
        "url": "https://ru.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "ru"
        }
    },
    {
        "name": "Викицитатник",
        "identifier": "ruwikiquote",
        "url": "https://ru.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ru"
        }
    },
    {
        "name": "Викитека",
        "identifier": "ruwikisource",
        "url": "https://ru.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ru"
        }
    },
    {
        "name": "Викиверситет",
        "identifier": "ruwikiversity",
        "url": "https://ru.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "ru"
        }
    },
    {
        "name": "Wikivoyage",
        "identifier": "ruwikivoyage",
        "url": "https://ru.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "ru"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "nnwiki",
        "url": "https://nn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nn"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "nnwiktionary",
        "url": "https://nn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "nn"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "nnwikiquote",
        "url": "https://nn.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "nn"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "aywiki",
        "url": "https://ay.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ay"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "aywiktionary",
        "url": "https://ay.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ay"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "aywikibooks",
        "url": "https://ay.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ay"
        }
    },
    {
        "name": "Uicipeid",
        "identifier": "gdwiki",
        "url": "https://gd.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gd"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "gdwiktionary",
        "url": "https://gd.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "gd"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "roa_tarawiki",
        "url": "https://roa-tara.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "roa-tara"
        }
    },
    {
        "name": "ᱣᱤᱠᱤᱯᱤᱰᱤᱭᱟ",
        "identifier": "satwiki",
        "url": "https://sat.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sat"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "suwiki",
        "url": "https://su.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "su"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "suwiktionary",
        "url": "https://su.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "su"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "suwikibooks",
        "url": "https://su.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "su"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "suwikiquote",
        "url": "https://su.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "su"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "bmwiki",
        "url": "https://bm.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bm"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "bmwiktionary",
        "url": "https://bm.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "bm"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "bmwikibooks",
        "url": "https://bm.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "bm"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "bmwikiquote",
        "url": "https://bm.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "bm"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "eewiki",
        "url": "https://ee.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ee"
        }
    },
    {
        "name": "ויקיפדיה",
        "identifier": "hewiki",
        "url": "https://he.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "he"
        }
    },
    {
        "name": "ויקימילון",
        "identifier": "hewiktionary",
        "url": "https://he.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "he"
        }
    },
    {
        "name": "ויקיספר",
        "identifier": "hewikibooks",
        "url": "https://he.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "he"
        }
    },
    {
        "name": "ויקיחדשות",
        "identifier": "hewikinews",
        "url": "https://he.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "he"
        }
    },
    {
        "name": "ויקיציטוט",
        "identifier": "hewikiquote",
        "url": "https://he.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "he"
        }
    },
    {
        "name": "ויקיטקסט",
        "identifier": "hewikisource",
        "url": "https://he.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "he"
        }
    },
    {
        "name": "ויקימסע",
        "identifier": "hewikivoyage",
        "url": "https://he.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "he"
        }
    },
    {
        "name": "Wikipidia",
        "identifier": "jamwiki",
        "url": "https://jam.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "jam"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "ugwiki",
        "url": "https://ug.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ug"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "ugwiktionary",
        "url": "https://ug.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ug"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "ugwikibooks",
        "url": "https://ug.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ug"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "ugwikiquote",
        "url": "https://ug.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ug"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "xhwiki",
        "url": "https://xh.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "xh"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "xhwiktionary",
        "url": "https://xh.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "xh"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "xhwikibooks",
        "url": "https://xh.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "xh"
        }
    },
    {
        "name": "অসমীয়া ৱিকিপিডিয়া",
        "identifier": "aswiki",
        "url": "https://as.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "as"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "aswiktionary",
        "url": "https://as.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "as"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "aswikibooks",
        "url": "https://as.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "as"
        }
    },
    {
        "name": "ৱিকিউদ্ধৃতি",
        "identifier": "aswikiquote",
        "url": "https://as.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "as"
        }
    },
    {
        "name": "ৱিকিউৎস",
        "identifier": "aswikisource",
        "url": "https://as.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "as"
        }
    },
    {
        "name": "Vikipediya",
        "identifier": "azwiki",
        "url": "https://az.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "az"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "azwiktionary",
        "url": "https://az.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "az"
        }
    },
    {
        "name": "Vikikitab",
        "identifier": "azwikibooks",
        "url": "https://az.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "az"
        }
    },
    {
        "name": "Vikisitat",
        "identifier": "azwikiquote",
        "url": "https://az.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "az"
        }
    },
    {
        "name": "Vikimənbə",
        "identifier": "azwikisource",
        "url": "https://az.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "az"
        }
    },
    {
        "name": "ဝီခီပီးဒီးယား",
        "identifier": "blkwiki",
        "url": "https://blk.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "blk"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "lbwiki",
        "url": "https://lb.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lb"
        }
    },
    {
        "name": "Wiktionnaire",
        "identifier": "lbwiktionary",
        "url": "https://lb.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "lb"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "lbwikibooks",
        "url": "https://lb.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "lb"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "lbwikiquote",
        "url": "https://lb.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "lb"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "madwiki",
        "url": "https://mad.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mad"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "napwiki",
        "url": "https://nap.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nap"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "napwikisource",
        "url": "https://nap.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "nap"
        }
    },
    {
        "name": "Wikipidia",
        "identifier": "taywiki",
        "url": "https://tay.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tay"
        }
    },
    {
        "name": "Википедия",
        "identifier": "bawiki",
        "url": "https://ba.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ba"
        }
    },
    {
        "name": "Викидәреслек",
        "identifier": "bawikibooks",
        "url": "https://ba.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ba"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "cebwiki",
        "url": "https://ceb.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ceb"
        }
    },
    {
        "name": "Википеди",
        "identifier": "mrjwiki",
        "url": "https://mrj.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mrj"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "twwiki",
        "url": "https://tw.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tw"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "twwiktionary",
        "url": "https://tw.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "tw"
        }
    },
    {
        "name": "Vikipediya",
        "identifier": "gagwiki",
        "url": "https://gag.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gag"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "simplewiki",
        "url": "https://simple.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "simple"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "simplewiktionary",
        "url": "https://simple.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "simple"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "simplewikibooks",
        "url": "https://simple.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "simple"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "simplewikiquote",
        "url": "https://simple.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "simple"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "stqwiki",
        "url": "https://stq.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "stq"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "aawiki",
        "url": "https://aa.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "aa"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "aawiktionary",
        "url": "https://aa.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "aa"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "aawikibooks",
        "url": "https://aa.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "aa"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "astwiki",
        "url": "https://ast.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ast"
        }
    },
    {
        "name": "Wikcionariu",
        "identifier": "astwiktionary",
        "url": "https://ast.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ast"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "astwikibooks",
        "url": "https://ast.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ast"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "astwikiquote",
        "url": "https://ast.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ast"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "klwiki",
        "url": "https://kl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kl"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "klwiktionary",
        "url": "https://kl.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "kl"
        }
    },
    {
        "name": "維基百科",
        "identifier": "zh_yuewiki",
        "url": "https://zh-yue.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "zh-yue"
        }
    },
    {
        "name": "ويكيبيديا",
        "identifier": "arwiki",
        "url": "https://ar.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ar"
        }
    },
    {
        "name": "ويكاموس",
        "identifier": "arwiktionary",
        "url": "https://ar.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ar"
        }
    },
    {
        "name": "ويكي الكتب",
        "identifier": "arwikibooks",
        "url": "https://ar.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ar"
        }
    },
    {
        "name": "ويكي الأخبار",
        "identifier": "arwikinews",
        "url": "https://ar.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "ar"
        }
    },
    {
        "name": "ويكي الاقتباس",
        "identifier": "arwikiquote",
        "url": "https://ar.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ar"
        }
    },
    {
        "name": "ويكي مصدر",
        "identifier": "arwikisource",
        "url": "https://ar.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ar"
        }
    },
    {
        "name": "ويكي الجامعة",
        "identifier": "arwikiversity",
        "url": "https://ar.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "ar"
        }
    },
    {
        "name": "विकिपिडिया",
        "identifier": "dtywiki",
        "url": "https://dty.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "dty"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "guwwiki",
        "url": "https://guw.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "guw"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "guwwiktionary",
        "url": "https://guw.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "guw"
        }
    },
    {
        "name": "Wikilinlin",
        "identifier": "guwwikinews",
        "url": "https://guw.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "guw"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "guwwikiquote",
        "url": "https://guw.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "guw"
        }
    },
    {
        "name": "ڤیکیپئدیا",
        "identifier": "lrcwiki",
        "url": "https://lrc.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lrc"
        }
    },
    {
        "name": "ዊኪፔዲያ",
        "identifier": "tiwiki",
        "url": "https://ti.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ti"
        }
    },
    {
        "name": "ዊኪ-መዝገበ-ቃላት",
        "identifier": "tiwiktionary",
        "url": "https://ti.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ti"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "ttwiki",
        "url": "https://tt.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tt"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "ttwiktionary",
        "url": "https://tt.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "tt"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "ttwikibooks",
        "url": "https://tt.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "tt"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "ttwikiquote",
        "url": "https://tt.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "tt"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "bswiki",
        "url": "https://bs.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bs"
        }
    },
    {
        "name": "Wikirječnik",
        "identifier": "bswiktionary",
        "url": "https://bs.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "bs"
        }
    },
    {
        "name": "Wikiknjige",
        "identifier": "bswikibooks",
        "url": "https://bs.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "bs"
        }
    },
    {
        "name": "Wikivijesti",
        "identifier": "bswikinews",
        "url": "https://bs.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "bs"
        }
    },
    {
        "name": "Wikicitati",
        "identifier": "bswikiquote",
        "url": "https://bs.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "bs"
        }
    },
    {
        "name": "Wikizvor",
        "identifier": "bswikisource",
        "url": "https://bs.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "bs"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "lijwiki",
        "url": "https://lij.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lij"
        }
    },
    {
        "name": "Wikivivàgna",
        "identifier": "lijwikisource",
        "url": "https://lij.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "lij"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "minwiki",
        "url": "https://min.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "min"
        }
    },
    {
        "name": "Wikikato",
        "identifier": "minwiktionary",
        "url": "https://min.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "min"
        }
    },
    {
        "name": "Wikipedii",
        "identifier": "olowiki",
        "url": "https://olo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "olo"
        }
    },
    {
        "name": "විකිපීඩියා",
        "identifier": "siwiki",
        "url": "https://si.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "si"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "siwiktionary",
        "url": "https://si.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "si"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "siwikibooks",
        "url": "https://si.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "si"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "amiwiki",
        "url": "https://ami.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ami"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "eswiki",
        "url": "https://es.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "es"
        }
    },
    {
        "name": "Wikcionario",
        "identifier": "eswiktionary",
        "url": "https://es.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "es"
        }
    },
    {
        "name": "Wikilibros",
        "identifier": "eswikibooks",
        "url": "https://es.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "es"
        }
    },
    {
        "name": "Wikinoticias",
        "identifier": "eswikinews",
        "url": "https://es.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "es"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "eswikiquote",
        "url": "https://es.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "es"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "eswikisource",
        "url": "https://es.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "es"
        }
    },
    {
        "name": "Wikiversidad",
        "identifier": "eswikiversity",
        "url": "https://es.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "es"
        }
    },
    {
        "name": "Wikiviajes",
        "identifier": "eswikivoyage",
        "url": "https://es.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "es"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "pagwiki",
        "url": "https://pag.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pag"
        }
    },
    {
        "name": "Wikipédia",
        "identifier": "ptwiki",
        "url": "https://pt.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pt"
        }
    },
    {
        "name": "Wikcionário",
        "identifier": "ptwiktionary",
        "url": "https://pt.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "pt"
        }
    },
    {
        "name": "Wikilivros",
        "identifier": "ptwikibooks",
        "url": "https://pt.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "pt"
        }
    },
    {
        "name": "Wikinotícias",
        "identifier": "ptwikinews",
        "url": "https://pt.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "pt"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "ptwikiquote",
        "url": "https://pt.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "pt"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "ptwikisource",
        "url": "https://pt.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "pt"
        }
    },
    {
        "name": "Wikiversidade",
        "identifier": "ptwikiversity",
        "url": "https://pt.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "pt"
        }
    },
    {
        "name": "Wikivoyage",
        "identifier": "ptwikivoyage",
        "url": "https://pt.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "pt"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "gpewiki",
        "url": "https://gpe.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gpe"
        }
    },
    {
        "name": "Wikipeetia",
        "identifier": "gucwiki",
        "url": "https://guc.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "guc"
        }
    },
    {
        "name": "Wikipédia",
        "identifier": "huwiki",
        "url": "https://hu.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "hu"
        }
    },
    {
        "name": "Wikiszótár",
        "identifier": "huwiktionary",
        "url": "https://hu.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "hu"
        }
    },
    {
        "name": "Wikikönyvek",
        "identifier": "huwikibooks",
        "url": "https://hu.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "hu"
        }
    },
    {
        "name": "Wikihírek",
        "identifier": "huwikinews",
        "url": "https://hu.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "hu"
        }
    },
    {
        "name": "Wikidézet",
        "identifier": "huwikiquote",
        "url": "https://hu.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "hu"
        }
    },
    {
        "name": "Wikiforrás",
        "identifier": "huwikisource",
        "url": "https://hu.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "hu"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "liwiki",
        "url": "https://li.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "li"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "liwiktionary",
        "url": "https://li.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "li"
        }
    },
    {
        "name": "Wikibeuk",
        "identifier": "liwikibooks",
        "url": "https://li.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "li"
        }
    },
    {
        "name": "Wikinuujs",
        "identifier": "liwikinews",
        "url": "https://li.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "li"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "liwikiquote",
        "url": "https://li.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "li"
        }
    },
    {
        "name": "Wikibrónne",
        "identifier": "liwikisource",
        "url": "https://li.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "li"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "pwnwiki",
        "url": "https://pwn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pwn"
        }
    },
    {
        "name": "விக்கிப்பீடியா",
        "identifier": "tawiki",
        "url": "https://ta.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ta"
        }
    },
    {
        "name": "விக்சனரி",
        "identifier": "tawiktionary",
        "url": "https://ta.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ta"
        }
    },
    {
        "name": "விக்கிநூல்கள்",
        "identifier": "tawikibooks",
        "url": "https://ta.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ta"
        }
    },
    {
        "name": "விக்கிசெய்தி",
        "identifier": "tawikinews",
        "url": "https://ta.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "ta"
        }
    },
    {
        "name": "விக்கிமேற்கோள்",
        "identifier": "tawikiquote",
        "url": "https://ta.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ta"
        }
    },
    {
        "name": "விக்கிமூலம்",
        "identifier": "tawikisource",
        "url": "https://ta.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ta"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "wawiki",
        "url": "https://wa.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "wa"
        }
    },
    {
        "name": "Wiccionaire",
        "identifier": "wawiktionary",
        "url": "https://wa.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "wa"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "wawikibooks",
        "url": "https://wa.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "wa"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "wawikisource",
        "url": "https://wa.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "wa"
        }
    },
    {
        "name": "विकिपीडिया",
        "identifier": "bhwiki",
        "url": "https://bh.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bh"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "bhwiktionary",
        "url": "https://bh.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "bh"
        }
    },
    {
        "name": "Википєдїꙗ",
        "identifier": "cuwiki",
        "url": "https://cu.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "cu"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "lmowiki",
        "url": "https://lmo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lmo"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "lmowiktionary",
        "url": "https://lmo.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "lmo"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "pmswiki",
        "url": "https://pms.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pms"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "pmswikisource",
        "url": "https://pms.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "pms"
        }
    },
    {
        "name": "Vikipidiya",
        "identifier": "rmywiki",
        "url": "https://rmy.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "rmy"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "scwiki",
        "url": "https://sc.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sc"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "scwiktionary",
        "url": "https://sc.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sc"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "tywiki",
        "url": "https://ty.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ty"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "igwiki",
        "url": "https://ig.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ig"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "igwiktionary",
        "url": "https://ig.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ig"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "igwikiquote",
        "url": "https://ig.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ig"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "ngwiki",
        "url": "https://ng.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ng"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "roa_rupwiki",
        "url": "https://roa-rup.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "roa-rup"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "roa_rupwiktionary",
        "url": "https://roa-rup.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "roa-rup"
        }
    },
    {
        "name": "Vikipediya",
        "identifier": "uzwiki",
        "url": "https://uz.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "uz"
        }
    },
    {
        "name": "Vikilug‘at",
        "identifier": "uzwiktionary",
        "url": "https://uz.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "uz"
        }
    },
    {
        "name": "Vikikitob",
        "identifier": "uzwikibooks",
        "url": "https://uz.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "uz"
        }
    },
    {
        "name": "Vikiiqtibos",
        "identifier": "uzwikiquote",
        "url": "https://uz.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "uz"
        }
    },
    {
        "name": "विकिपीडिया",
        "identifier": "awawiki",
        "url": "https://awa.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "awa"
        }
    },
    {
        "name": "ویکی‌پدیا",
        "identifier": "azbwiki",
        "url": "https://azb.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "azb"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "fiu_vrowiki",
        "url": "https://fiu-vro.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "fiu-vro"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "gvwiki",
        "url": "https://gv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gv"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "gvwiktionary",
        "url": "https://gv.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "gv"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "rowiki",
        "url": "https://ro.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ro"
        }
    },
    {
        "name": "Wikționar",
        "identifier": "rowiktionary",
        "url": "https://ro.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ro"
        }
    },
    {
        "name": "Wikimanuale",
        "identifier": "rowikibooks",
        "url": "https://ro.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ro"
        }
    },
    {
        "name": "Wikiștiri",
        "identifier": "rowikinews",
        "url": "https://ro.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "ro"
        }
    },
    {
        "name": "Wikicitat",
        "identifier": "rowikiquote",
        "url": "https://ro.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ro"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "rowikisource",
        "url": "https://ro.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ro"
        }
    },
    {
        "name": "Wikivoyage",
        "identifier": "rowikivoyage",
        "url": "https://ro.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "ro"
        }
    },
    {
        "name": "विकिपीडिया",
        "identifier": "sawiki",
        "url": "https://sa.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sa"
        }
    },
    {
        "name": "विकिशब्दकोशः",
        "identifier": "sawiktionary",
        "url": "https://sa.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sa"
        }
    },
    {
        "name": "विकिपुस्तकानि",
        "identifier": "sawikibooks",
        "url": "https://sa.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "sa"
        }
    },
    {
        "name": "विकिसूक्तिः",
        "identifier": "sawikiquote",
        "url": "https://sa.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "sa"
        }
    },
    {
        "name": "विकिस्रोतः",
        "identifier": "sawikisource",
        "url": "https://sa.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "sa"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "sgwiki",
        "url": "https://sg.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sg"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "sgwiktionary",
        "url": "https://sg.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sg"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "vewiki",
        "url": "https://ve.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ve"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "wowiki",
        "url": "https://wo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "wo"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "wowiktionary",
        "url": "https://wo.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "wo"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "wowikiquote",
        "url": "https://wo.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "wo"
        }
    },
    {
        "name": "Wicipedia",
        "identifier": "cywiki",
        "url": "https://cy.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "cy"
        }
    },
    {
        "name": "Wiciadur",
        "identifier": "cywiktionary",
        "url": "https://cy.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "cy"
        }
    },
    {
        "name": "Wicilyfrau",
        "identifier": "cywikibooks",
        "url": "https://cy.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "cy"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "cywikiquote",
        "url": "https://cy.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "cy"
        }
    },
    {
        "name": "Wicidestun",
        "identifier": "cywikisource",
        "url": "https://cy.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "cy"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "dzwiki",
        "url": "https://dz.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "dz"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "dzwiktionary",
        "url": "https://dz.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "dz"
        }
    },
    {
        "name": "Wikipedya",
        "identifier": "htwiki",
        "url": "https://ht.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ht"
        }
    },
    {
        "name": "Wikisòrs",
        "identifier": "htwikisource",
        "url": "https://ht.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ht"
        }
    },
    {
        "name": "Вікіпедыя",
        "identifier": "bewiki",
        "url": "https://be.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "be"
        }
    },
    {
        "name": "Вікіслоўнік",
        "identifier": "bewiktionary",
        "url": "https://be.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "be"
        }
    },
    {
        "name": "Вікікнігі",
        "identifier": "bewikibooks",
        "url": "https://be.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "be"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "bewikiquote",
        "url": "https://be.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "be"
        }
    },
    {
        "name": "Вікікрыніцы",
        "identifier": "bewikisource",
        "url": "https://be.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "be"
        }
    },
    {
        "name": "ویکیپیدیا",
        "identifier": "ckbwiki",
        "url": "https://ckb.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ckb"
        }
    },
    {
        "name": "ویکیفەرھەنگ",
        "identifier": "ckbwiktionary",
        "url": "https://ckb.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ckb"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "emlwiki",
        "url": "https://eml.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "eml"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "krwiki",
        "url": "https://kr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kr"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "krwikiquote",
        "url": "https://kr.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "kr"
        }
    },
    {
        "name": "วิกิพีเดีย",
        "identifier": "thwiki",
        "url": "https://th.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "th"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "thwiktionary",
        "url": "https://th.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "th"
        }
    },
    {
        "name": "วิกิตำรา",
        "identifier": "thwikibooks",
        "url": "https://th.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "th"
        }
    },
    {
        "name": "Wikinews",
        "identifier": "thwikinews",
        "url": "https://th.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "th"
        }
    },
    {
        "name": "วิกิคำคม",
        "identifier": "thwikiquote",
        "url": "https://th.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "th"
        }
    },
    {
        "name": "วิกิซอร์ซ",
        "identifier": "thwikisource",
        "url": "https://th.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "th"
        }
    },
    {
        "name": "Википедия",
        "identifier": "udmwiki",
        "url": "https://udm.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "udm"
        }
    },
    {
        "name": "Βικιπαίδεια",
        "identifier": "elwiki",
        "url": "https://el.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "el"
        }
    },
    {
        "name": "Βικιλεξικό",
        "identifier": "elwiktionary",
        "url": "https://el.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "el"
        }
    },
    {
        "name": "Βικιβιβλία",
        "identifier": "elwikibooks",
        "url": "https://el.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "el"
        }
    },
    {
        "name": "Βικινέα",
        "identifier": "elwikinews",
        "url": "https://el.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "el"
        }
    },
    {
        "name": "Βικιφθέγματα",
        "identifier": "elwikiquote",
        "url": "https://el.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "el"
        }
    },
    {
        "name": "Βικιθήκη",
        "identifier": "elwikisource",
        "url": "https://el.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "el"
        }
    },
    {
        "name": "Βικιεπιστήμιο",
        "identifier": "elwikiversity",
        "url": "https://el.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "el"
        }
    },
    {
        "name": "Βικιταξίδια",
        "identifier": "elwikivoyage",
        "url": "https://el.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "el"
        }
    },
    {
        "name": "Wikipedio",
        "identifier": "iowiki",
        "url": "https://io.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "io"
        }
    },
    {
        "name": "Wikivortaro",
        "identifier": "iowiktionary",
        "url": "https://io.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "io"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "pihwiki",
        "url": "https://pih.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pih"
        }
    },
    {
        "name": "وڪيپيڊيا",
        "identifier": "sdwiki",
        "url": "https://sd.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sd"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "sdwiktionary",
        "url": "https://sd.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sd"
        }
    },
    {
        "name": "Wikinews",
        "identifier": "sdwikinews",
        "url": "https://sd.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "sd"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "swwiki",
        "url": "https://sw.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sw"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "swwiktionary",
        "url": "https://sw.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sw"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "swwikibooks",
        "url": "https://sw.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "sw"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "xalwiki",
        "url": "https://xal.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "xal"
        }
    },
    {
        "name": "Wikipedija",
        "identifier": "hrwiki",
        "url": "https://hr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "hr"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "hrwiktionary",
        "url": "https://hr.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "hr"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "hrwikibooks",
        "url": "https://hr.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "hr"
        }
    },
    {
        "name": "Wikicitat",
        "identifier": "hrwikiquote",
        "url": "https://hr.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "hr"
        }
    },
    {
        "name": "Wikizvor",
        "identifier": "hrwikisource",
        "url": "https://hr.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "hr"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "nawiki",
        "url": "https://na.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "na"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "nawiktionary",
        "url": "https://na.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "na"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "nawikibooks",
        "url": "https://na.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "na"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "nawikiquote",
        "url": "https://na.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "na"
        }
    },
    {
        "name": "Wikasegzawal",
        "identifier": "shywiktionary",
        "url": "https://shy.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "shy"
        }
    },
    {
        "name": "Википедија",
        "identifier": "srwiki",
        "url": "https://sr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sr"
        }
    },
    {
        "name": "Викиречник",
        "identifier": "srwiktionary",
        "url": "https://sr.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sr"
        }
    },
    {
        "name": "Викикњиге",
        "identifier": "srwikibooks",
        "url": "https://sr.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "sr"
        }
    },
    {
        "name": "Викиновости",
        "identifier": "srwikinews",
        "url": "https://sr.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "sr"
        }
    },
    {
        "name": "Викицитат",
        "identifier": "srwikiquote",
        "url": "https://sr.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "sr"
        }
    },
    {
        "name": "Викизворник",
        "identifier": "srwikisource",
        "url": "https://sr.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "sr"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "kshwiki",
        "url": "https://ksh.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ksh"
        }
    },
    {
        "name": "Vikipedya",
        "identifier": "ladwiki",
        "url": "https://lad.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lad"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "mswiki",
        "url": "https://ms.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ms"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "mswiktionary",
        "url": "https://ms.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ms"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "mswikibooks",
        "url": "https://ms.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ms"
        }
    },
    {
        "name": "Википедиа",
        "identifier": "tgwiki",
        "url": "https://tg.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tg"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "tgwiktionary",
        "url": "https://tg.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "tg"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "tgwikibooks",
        "url": "https://tg.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "tg"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "barwiki",
        "url": "https://bar.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bar"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "zhwiki",
        "url": "https://zh.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "zh"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "zhwiktionary",
        "url": "https://zh.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "zh"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "zhwikibooks",
        "url": "https://zh.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "zh"
        }
    },
    {
        "name": "Wikinews",
        "identifier": "zhwikinews",
        "url": "https://zh.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "zh"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "zhwikiquote",
        "url": "https://zh.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "zh"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "zhwikisource",
        "url": "https://zh.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "zh"
        }
    },
    {
        "name": "維基學院",
        "identifier": "zhwikiversity",
        "url": "https://zh.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "zh"
        }
    },
    {
        "name": "维基导游",
        "identifier": "zhwikivoyage",
        "url": "https://zh.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "zh"
        }
    },
    {
        "name": "Vikipedii",
        "identifier": "vepwiki",
        "url": "https://vep.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "vep"
        }
    },
    {
        "name": "Wikipédia",
        "identifier": "frwiki",
        "url": "https://fr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "fr"
        }
    },
    {
        "name": "Wiktionnaire",
        "identifier": "frwiktionary",
        "url": "https://fr.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "fr"
        }
    },
    {
        "name": "Wikilivres",
        "identifier": "frwikibooks",
        "url": "https://fr.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "fr"
        }
    },
    {
        "name": "Wikinews",
        "identifier": "frwikinews",
        "url": "https://fr.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "fr"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "frwikiquote",
        "url": "https://fr.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "fr"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "frwikisource",
        "url": "https://fr.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "fr"
        }
    },
    {
        "name": "Wikiversité",
        "identifier": "frwikiversity",
        "url": "https://fr.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "fr"
        }
    },
    {
        "name": "Wikivoyage",
        "identifier": "frwikivoyage",
        "url": "https://fr.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "fr"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "kcgwiki",
        "url": "https://kcg.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kcg"
        }
    },
    {
        "name": "Swánga̱lyiatwuki",
        "identifier": "kcgwiktionary",
        "url": "https://kcg.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "kcg"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "nywiki",
        "url": "https://ny.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ny"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "pamwiki",
        "url": "https://pam.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pam"
        }
    },
    {
        "name": "Бикипиэдьийэ",
        "identifier": "sahwiki",
        "url": "https://sah.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sah"
        }
    },
    {
        "name": "Биики_Домох",
        "identifier": "sahwikiquote",
        "url": "https://sah.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "sah"
        }
    },
    {
        "name": "Бикитиэкэ",
        "identifier": "sahwikisource",
        "url": "https://sah.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "sah"
        }
    },
    {
        "name": "ဝီႇၶီႇၽီးတီးယႃး",
        "identifier": "shnwiki",
        "url": "https://shn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "shn"
        }
    },
    {
        "name": "ဝိၵ်ႇသျိၼ်ႇၼရီႇ",
        "identifier": "shnwiktionary",
        "url": "https://shn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "shn"
        }
    },
    {
        "name": "ဝီႇၶီႇပပ်ႉ",
        "identifier": "shnwikibooks",
        "url": "https://shn.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "shn"
        }
    },
    {
        "name": "ဝီႇၶီႇဝွႆးဢဵတ်ႇꩡ်",
        "identifier": "shnwikivoyage",
        "url": "https://shn.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "shn"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "sqwiki",
        "url": "https://sq.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sq"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "sqwiktionary",
        "url": "https://sq.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sq"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "sqwikibooks",
        "url": "https://sq.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "sq"
        }
    },
    {
        "name": "Wikilajme",
        "identifier": "sqwikinews",
        "url": "https://sq.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "sq"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "sqwikiquote",
        "url": "https://sq.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "sq"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "biwiki",
        "url": "https://bi.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bi"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "biwiktionary",
        "url": "https://bi.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "bi"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "biwikibooks",
        "url": "https://bi.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "bi"
        }
    },
    {
        "name": "Wikipitiya",
        "identifier": "szywiki",
        "url": "https://szy.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "szy"
        }
    },
    {
        "name": "Wikipediýa",
        "identifier": "tkwiki",
        "url": "https://tk.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tk"
        }
    },
    {
        "name": "Wikisözlük",
        "identifier": "tkwiktionary",
        "url": "https://tk.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "tk"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "tkwikibooks",
        "url": "https://tk.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "tk"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "tkwikiquote",
        "url": "https://tk.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "tk"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "gotwiki",
        "url": "https://got.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "got"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "gotwikibooks",
        "url": "https://got.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "got"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "hakwiki",
        "url": "https://hak.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "hak"
        }
    },
    {
        "name": "Википедиа",
        "identifier": "mnwiki",
        "url": "https://mn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mn"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "mnwiktionary",
        "url": "https://mn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "mn"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "mnwikibooks",
        "url": "https://mn.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "mn"
        }
    },
    {
        "name": "Википедия",
        "identifier": "tyvwiki",
        "url": "https://tyv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tyv"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "omwiki",
        "url": "https://om.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "om"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "omwiktionary",
        "url": "https://om.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "om"
        }
    },
    {
        "name": "Википедия",
        "identifier": "altwiki",
        "url": "https://alt.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "alt"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "bowiki",
        "url": "https://bo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bo"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "bowiktionary",
        "url": "https://bo.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "bo"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "bowikibooks",
        "url": "https://bo.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "bo"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "diqwiki",
        "url": "https://diq.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "diq"
        }
    },
    {
        "name": "Wikiqısebend",
        "identifier": "diqwiktionary",
        "url": "https://diq.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "diq"
        }
    },
    {
        "name": "Wikipedy",
        "identifier": "fywiki",
        "url": "https://fy.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "fy"
        }
    },
    {
        "name": "Wikiwurdboek",
        "identifier": "fywiktionary",
        "url": "https://fy.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "fy"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "fywikibooks",
        "url": "https://fy.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "fy"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "iewiki",
        "url": "https://ie.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ie"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "iewiktionary",
        "url": "https://ie.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ie"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "iewikibooks",
        "url": "https://ie.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ie"
        }
    },
    {
        "name": "Vikipēdija",
        "identifier": "lvwiki",
        "url": "https://lv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lv"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "lvwiktionary",
        "url": "https://lv.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "lv"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "lvwikibooks",
        "url": "https://lv.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "lv"
        }
    },
    {
        "name": "ꯋꯤꯀꯤꯄꯦꯗꯤꯌꯥ",
        "identifier": "mniwiki",
        "url": "https://mni.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mni"
        }
    },
    {
        "name": "ꯋꯤꯛꯁꯟꯅꯔꯤ",
        "identifier": "mniwiktionary",
        "url": "https://mni.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "mni"
        }
    },
    {
        "name": "Википеди",
        "identifier": "oswiki",
        "url": "https://os.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "os"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "tswiki",
        "url": "https://ts.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ts"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "tswiktionary",
        "url": "https://ts.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ts"
        }
    },
    {
        "name": "ويكيبيديا",
        "identifier": "arzwiki",
        "url": "https://arz.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "arz"
        }
    },
    {
        "name": "Википедия",
        "identifier": "kywiki",
        "url": "https://ky.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ky"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "kywiktionary",
        "url": "https://ky.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ky"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "kywikibooks",
        "url": "https://ky.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ky"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "kywikiquote",
        "url": "https://ky.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ky"
        }
    },
    {
        "name": "Vikipedeja",
        "identifier": "ltgwiki",
        "url": "https://ltg.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ltg"
        }
    },
    {
        "name": "विकिपिडिया",
        "identifier": "maiwiki",
        "url": "https://mai.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mai"
        }
    },
    {
        "name": "Βικιπαίδεια",
        "identifier": "pntwiki",
        "url": "https://pnt.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pnt"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "fjwiki",
        "url": "https://fj.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "fj"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "fjwiktionary",
        "url": "https://fj.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "fj"
        }
    },
    {
        "name": "ᐅᐃᑭᐱᑎᐊ",
        "identifier": "iuwiki",
        "url": "https://iu.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "iu"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "iuwiktionary",
        "url": "https://iu.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "iu"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "plwiki",
        "url": "https://pl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pl"
        }
    },
    {
        "name": "Wikisłownik",
        "identifier": "plwiktionary",
        "url": "https://pl.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "pl"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "plwikibooks",
        "url": "https://pl.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "pl"
        }
    },
    {
        "name": "Wikinews",
        "identifier": "plwikinews",
        "url": "https://pl.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "pl"
        }
    },
    {
        "name": "Wikicytaty",
        "identifier": "plwikiquote",
        "url": "https://pl.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "pl"
        }
    },
    {
        "name": "Wikiźródła",
        "identifier": "plwikisource",
        "url": "https://pl.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "pl"
        }
    },
    {
        "name": "Wikipodróże",
        "identifier": "plwikivoyage",
        "url": "https://pl.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "pl"
        }
    },
    {
        "name": "Википедие",
        "identifier": "adywiki",
        "url": "https://ady.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ady"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "crwiki",
        "url": "https://cr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "cr"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "crwiktionary",
        "url": "https://cr.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "cr"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "crwikiquote",
        "url": "https://cr.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "cr"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "nlwiki",
        "url": "https://nl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nl"
        }
    },
    {
        "name": "WikiWoordenboek",
        "identifier": "nlwiktionary",
        "url": "https://nl.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "nl"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "nlwikibooks",
        "url": "https://nl.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "nl"
        }
    },
    {
        "name": "Wikinieuws",
        "identifier": "nlwikinews",
        "url": "https://nl.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "nl"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "nlwikiquote",
        "url": "https://nl.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "nl"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "nlwikisource",
        "url": "https://nl.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "nl"
        }
    },
    {
        "name": "Wikivoyage",
        "identifier": "nlwikivoyage",
        "url": "https://nl.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "nl"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "quwiki",
        "url": "https://qu.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "qu"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "quwiktionary",
        "url": "https://qu.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "qu"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "quwikibooks",
        "url": "https://qu.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "qu"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "quwikiquote",
        "url": "https://qu.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "qu"
        }
    },
    {
        "name": "Wikipedija",
        "identifier": "slwiki",
        "url": "https://sl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sl"
        }
    },
    {
        "name": "Wikislovar",
        "identifier": "slwiktionary",
        "url": "https://sl.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sl"
        }
    },
    {
        "name": "Wikiknjige",
        "identifier": "slwikibooks",
        "url": "https://sl.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "sl"
        }
    },
    {
        "name": "Wikinavedek",
        "identifier": "slwikiquote",
        "url": "https://sl.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "sl"
        }
    },
    {
        "name": "Wikivir",
        "identifier": "slwikisource",
        "url": "https://sl.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "sl"
        }
    },
    {
        "name": "Wikiverza",
        "identifier": "slwikiversity",
        "url": "https://sl.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "sl"
        }
    },
    {
        "name": "উইকিপিডিয়া",
        "identifier": "bnwiki",
        "url": "https://bn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bn"
        }
    },
    {
        "name": "উইকিঅভিধান",
        "identifier": "bnwiktionary",
        "url": "https://bn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "bn"
        }
    },
    {
        "name": "উইকিবই",
        "identifier": "bnwikibooks",
        "url": "https://bn.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "bn"
        }
    },
    {
        "name": "উইকিউক্তি",
        "identifier": "bnwikiquote",
        "url": "https://bn.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "bn"
        }
    },
    {
        "name": "উইকিসংকলন",
        "identifier": "bnwikisource",
        "url": "https://bn.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "bn"
        }
    },
    {
        "name": "উইকিভ্রমণ",
        "identifier": "bnwikivoyage",
        "url": "https://bn.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "bn"
        }
    },
    {
        "name": "Dagbani Wikipedia",
        "identifier": "dagwiki",
        "url": "https://dag.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "dag"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "fowiki",
        "url": "https://fo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "fo"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "fowiktionary",
        "url": "https://fo.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "fo"
        }
    },
    {
        "name": "Wikiheimild",
        "identifier": "fowikisource",
        "url": "https://fo.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "fo"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "howiki",
        "url": "https://ho.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ho"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "kgwiki",
        "url": "https://kg.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kg"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "rmwiki",
        "url": "https://rm.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "rm"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "rmwiktionary",
        "url": "https://rm.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "rm"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "rmwikibooks",
        "url": "https://rm.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "rm"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "tpiwiki",
        "url": "https://tpi.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tpi"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "tpiwiktionary",
        "url": "https://tpi.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "tpi"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "nds_nlwiki",
        "url": "https://nds-nl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nds-nl"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "akwiki",
        "url": "https://ak.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ak"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "akwiktionary",
        "url": "https://ak.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ak"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "akwikibooks",
        "url": "https://ak.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ak"
        }
    },
    {
        "name": "Wikipédia",
        "identifier": "banwiki",
        "url": "https://ban.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ban"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "banwikisource",
        "url": "https://ban.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ban"
        }
    },
    {
        "name": "Վիքիպեդիա",
        "identifier": "hywiki",
        "url": "https://hy.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "hy"
        }
    },
    {
        "name": "Վիքիբառարան",
        "identifier": "hywiktionary",
        "url": "https://hy.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "hy"
        }
    },
    {
        "name": "Վիքիգրքեր",
        "identifier": "hywikibooks",
        "url": "https://hy.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "hy"
        }
    },
    {
        "name": "Վիքիքաղվածք",
        "identifier": "hywikiquote",
        "url": "https://hy.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "hy"
        }
    },
    {
        "name": "Վիքիդարան",
        "identifier": "hywikisource",
        "url": "https://hy.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "hy"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "jbowiki",
        "url": "https://jbo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "jbo"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "jbowiktionary",
        "url": "https://jbo.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "jbo"
        }
    },
    {
        "name": "វិគីភីឌា",
        "identifier": "kmwiki",
        "url": "https://km.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "km"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "kmwiktionary",
        "url": "https://km.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "km"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "kmwikibooks",
        "url": "https://km.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "km"
        }
    },
    {
        "name": "Википедия",
        "identifier": "lbewiki",
        "url": "https://lbe.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lbe"
        }
    },
    {
        "name": "Vicipedia",
        "identifier": "lfnwiki",
        "url": "https://lfn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lfn"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "bclwiki",
        "url": "https://bcl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bcl"
        }
    },
    {
        "name": "Wiksyunaryo",
        "identifier": "bclwiktionary",
        "url": "https://bcl.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "bcl"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "bclwikiquote",
        "url": "https://bcl.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "bcl"
        }
    },
    {
        "name": "Ուիքիփետիա",
        "identifier": "hywwiki",
        "url": "https://hyw.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "hyw"
        }
    },
    {
        "name": "Уикипедия",
        "identifier": "kkwiki",
        "url": "https://kk.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kk"
        }
    },
    {
        "name": "Уикисөздік",
        "identifier": "kkwiktionary",
        "url": "https://kk.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "kk"
        }
    },
    {
        "name": "Уикикітап",
        "identifier": "kkwikibooks",
        "url": "https://kk.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "kk"
        }
    },
    {
        "name": "Уикидәйек",
        "identifier": "kkwikiquote",
        "url": "https://kk.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "kk"
        }
    },
    {
        "name": "Wikipǣdia",
        "identifier": "angwiki",
        "url": "https://ang.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ang"
        }
    },
    {
        "name": "Wikiwordbōc",
        "identifier": "angwiktionary",
        "url": "https://ang.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ang"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "angwikibooks",
        "url": "https://ang.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ang"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "angwikiquote",
        "url": "https://ang.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ang"
        }
    },
    {
        "name": "Wicifruma",
        "identifier": "angwikisource",
        "url": "https://ang.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ang"
        }
    },
    {
        "name": "Wikipetcia",
        "identifier": "atjwiki",
        "url": "https://atj.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "atj"
        }
    },
    {
        "name": "Вікіпэдыя",
        "identifier": "be_x_oldwiki",
        "url": "https://be-tarask.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "be-x-old"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "brwiki",
        "url": "https://br.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "br"
        }
    },
    {
        "name": "Wikeriadur",
        "identifier": "brwiktionary",
        "url": "https://br.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "br"
        }
    },
    {
        "name": "Wikiarroud",
        "identifier": "brwikiquote",
        "url": "https://br.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "br"
        }
    },
    {
        "name": "Wikimammenn",
        "identifier": "brwikisource",
        "url": "https://br.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "br"
        }
    },
    {
        "name": "Wikipédja",
        "identifier": "gcrwiki",
        "url": "https://gcr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gcr"
        }
    },
    {
        "name": "विकिपीडिया",
        "identifier": "hiwiki",
        "url": "https://hi.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "hi"
        }
    },
    {
        "name": "विक्षनरी",
        "identifier": "hiwiktionary",
        "url": "https://hi.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "hi"
        }
    },
    {
        "name": "विकिपुस्तक",
        "identifier": "hiwikibooks",
        "url": "https://hi.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "hi"
        }
    },
    {
        "name": "विकिसूक्ति",
        "identifier": "hiwikiquote",
        "url": "https://hi.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "hi"
        }
    },
    {
        "name": "विकिस्रोत",
        "identifier": "hiwikisource",
        "url": "https://hi.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "hi"
        }
    },
    {
        "name": "विकिविश्वविद्यालय",
        "identifier": "hiwikiversity",
        "url": "https://hi.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "hi"
        }
    },
    {
        "name": "विकियात्रा",
        "identifier": "hiwikivoyage",
        "url": "https://hi.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "hi"
        }
    },
    {
        "name": "Авикипедиа",
        "identifier": "abwiki",
        "url": "https://ab.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ab"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "abwiktionary",
        "url": "https://ab.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ab"
        }
    },
    {
        "name": "Wikipidia",
        "identifier": "bjnwiki",
        "url": "https://bjn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bjn"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "bjnwiktionary",
        "url": "https://bjn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "bjn"
        }
    },
    {
        "name": "Wikipedija",
        "identifier": "hsbwiki",
        "url": "https://hsb.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "hsb"
        }
    },
    {
        "name": "Wikisłownik",
        "identifier": "hsbwiktionary",
        "url": "https://hsb.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "hsb"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "muswiki",
        "url": "https://mus.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mus"
        }
    },
    {
        "name": "Википедиясь",
        "identifier": "myvwiki",
        "url": "https://myv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "myv"
        }
    },
    {
        "name": "维基百科",
        "identifier": "wuuwiki",
        "url": "https://wuu.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "wuu"
        }
    },
    {
        "name": "Уикипедия",
        "identifier": "bgwiki",
        "url": "https://bg.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bg"
        }
    },
    {
        "name": "Уикиречник",
        "identifier": "bgwiktionary",
        "url": "https://bg.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "bg"
        }
    },
    {
        "name": "Уикикниги",
        "identifier": "bgwikibooks",
        "url": "https://bg.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "bg"
        }
    },
    {
        "name": "Уикиновини",
        "identifier": "bgwikinews",
        "url": "https://bg.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "bg"
        }
    },
    {
        "name": "Уикицитат",
        "identifier": "bgwikiquote",
        "url": "https://bg.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "bg"
        }
    },
    {
        "name": "Уикиизточник",
        "identifier": "bgwikisource",
        "url": "https://bg.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "bg"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "cowiki",
        "url": "https://co.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "co"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "cowiktionary",
        "url": "https://co.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "co"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "cowikibooks",
        "url": "https://co.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "co"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "cowikiquote",
        "url": "https://co.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "co"
        }
    },
    {
        "name": "Wikipedie",
        "identifier": "cswiki",
        "url": "https://cs.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "cs"
        }
    },
    {
        "name": "Wikislovník",
        "identifier": "cswiktionary",
        "url": "https://cs.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "cs"
        }
    },
    {
        "name": "Wikiknihy",
        "identifier": "cswikibooks",
        "url": "https://cs.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "cs"
        }
    },
    {
        "name": "Wikizprávy",
        "identifier": "cswikinews",
        "url": "https://cs.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "cs"
        }
    },
    {
        "name": "Wikicitáty",
        "identifier": "cswikiquote",
        "url": "https://cs.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "cs"
        }
    },
    {
        "name": "Wikizdroje",
        "identifier": "cswikisource",
        "url": "https://cs.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "cs"
        }
    },
    {
        "name": "Wikiverzita",
        "identifier": "cswikiversity",
        "url": "https://cs.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "cs"
        }
    },
    {
        "name": "Vichipedie",
        "identifier": "furwiki",
        "url": "https://fur.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "fur"
        }
    },
    {
        "name": "維基百科",
        "identifier": "ganwiki",
        "url": "https://gan.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gan"
        }
    },
    {
        "name": "Википедия",
        "identifier": "krcwiki",
        "url": "https://krc.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "krc"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "lgwiki",
        "url": "https://lg.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lg"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "scowiki",
        "url": "https://sco.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sco"
        }
    },
    {
        "name": "Википедий",
        "identifier": "mhrwiki",
        "url": "https://mhr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mhr"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "acewiki",
        "url": "https://ace.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ace"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "afwiki",
        "url": "https://af.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "af"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "afwiktionary",
        "url": "https://af.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "af"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "afwikibooks",
        "url": "https://af.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "af"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "afwikiquote",
        "url": "https://af.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "af"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "csbwiki",
        "url": "https://csb.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "csb"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "csbwiktionary",
        "url": "https://csb.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "csb"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "frrwiki",
        "url": "https://frr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "frr"
        }
    },
    {
        "name": "विकिपीडिया",
        "identifier": "gomwiki",
        "url": "https://gom.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gom"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "gomwiktionary",
        "url": "https://gom.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "gom"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "iawiki",
        "url": "https://ia.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ia"
        }
    },
    {
        "name": "Wiktionario",
        "identifier": "iawiktionary",
        "url": "https://ia.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ia"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "iawikibooks",
        "url": "https://ia.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ia"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "mgwiki",
        "url": "https://mg.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mg"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "mgwiktionary",
        "url": "https://mg.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "mg"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "mgwikibooks",
        "url": "https://mg.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "mg"
        }
    },
    {
        "name": "Wikipedija",
        "identifier": "mtwiki",
        "url": "https://mt.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mt"
        }
    },
    {
        "name": "Wikizzjunarju",
        "identifier": "mtwiktionary",
        "url": "https://mt.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "mt"
        }
    },
    {
        "name": "Wikipedija",
        "identifier": "dsbwiki",
        "url": "https://dsb.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "dsb"
        }
    },
    {
        "name": "Википедия",
        "identifier": "koiwiki",
        "url": "https://koi.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "koi"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "nsowiki",
        "url": "https://nso.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nso"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "stwiki",
        "url": "https://st.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "st"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "stwiktionary",
        "url": "https://st.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "st"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "tumwiki",
        "url": "https://tum.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tum"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "zuwiki",
        "url": "https://zu.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "zu"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "zuwiktionary",
        "url": "https://zu.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "zu"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "zuwikibooks",
        "url": "https://zu.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "zu"
        }
    },
    {
        "name": "Vikipeedia",
        "identifier": "etwiki",
        "url": "https://et.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "et"
        }
    },
    {
        "name": "Vikisõnastik",
        "identifier": "etwiktionary",
        "url": "https://et.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "et"
        }
    },
    {
        "name": "Vikiõpikud",
        "identifier": "etwikibooks",
        "url": "https://et.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "et"
        }
    },
    {
        "name": "Vikitsitaadid",
        "identifier": "etwikiquote",
        "url": "https://et.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "et"
        }
    },
    {
        "name": "Vikitekstid",
        "identifier": "etwikisource",
        "url": "https://et.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "et"
        }
    },
    {
        "name": "Vicipéid",
        "identifier": "gawiki",
        "url": "https://ga.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ga"
        }
    },
    {
        "name": "Vicífhoclóir",
        "identifier": "gawiktionary",
        "url": "https://ga.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ga"
        }
    },
    {
        "name": "Vicíleabhair",
        "identifier": "gawikibooks",
        "url": "https://ga.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ga"
        }
    },
    {
        "name": "Vicísliocht",
        "identifier": "gawikiquote",
        "url": "https://ga.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ga"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "glkwiki",
        "url": "https://glk.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "glk"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "snwiki",
        "url": "https://sn.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sn"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "snwiktionary",
        "url": "https://sn.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sn"
        }
    },
    {
        "name": "Wikipédia",
        "identifier": "jvwiki",
        "url": "https://jv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "jv"
        }
    },
    {
        "name": "Wikisastra",
        "identifier": "jvwiktionary",
        "url": "https://jv.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "jv"
        }
    },
    {
        "name": "Wikisumber",
        "identifier": "jvwikisource",
        "url": "https://jv.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "jv"
        }
    },
    {
        "name": "Википедия",
        "identifier": "lezwiki",
        "url": "https://lez.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lez"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "map_bmswiki",
        "url": "https://map-bms.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "map-bms"
        }
    },
    {
        "name": "ဝီကီပီးဒီးယား",
        "identifier": "mywiki",
        "url": "https://my.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "my"
        }
    },
    {
        "name": "ဝစ်ရှင်နရီ",
        "identifier": "mywiktionary",
        "url": "https://my.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "my"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "mywikibooks",
        "url": "https://my.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "my"
        }
    },
    {
        "name": "ਵਿਕੀਪੀਡੀਆ",
        "identifier": "pawiki",
        "url": "https://pa.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pa"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "pawiktionary",
        "url": "https://pa.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "pa"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "pawikibooks",
        "url": "https://pa.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "pa"
        }
    },
    {
        "name": "ਵਿਕੀਸਰੋਤ",
        "identifier": "pawikisource",
        "url": "https://pa.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "pa"
        }
    },
    {
        "name": "Wikipedija",
        "identifier": "shwiki",
        "url": "https://sh.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sh"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "shwiktionary",
        "url": "https://sh.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sh"
        }
    },
    {
        "name": "વિકિપીડિયા",
        "identifier": "guwiki",
        "url": "https://gu.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gu"
        }
    },
    {
        "name": "વિકિકોશ",
        "identifier": "guwiktionary",
        "url": "https://gu.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "gu"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "guwikibooks",
        "url": "https://gu.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "gu"
        }
    },
    {
        "name": "વિકિસૂક્તિ",
        "identifier": "guwikiquote",
        "url": "https://gu.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "gu"
        }
    },
    {
        "name": "વિકિસ્રોત",
        "identifier": "guwikisource",
        "url": "https://gu.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "gu"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "kjwiki",
        "url": "https://kj.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kj"
        }
    },
    {
        "name": "ວິກິພີເດຍ",
        "identifier": "lowiki",
        "url": "https://lo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "lo"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "lowiktionary",
        "url": "https://lo.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "lo"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "mhwiki",
        "url": "https://mh.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mh"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "mhwiktionary",
        "url": "https://mh.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "mh"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "ndswiki",
        "url": "https://nds.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "nds"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "ndswiktionary",
        "url": "https://nds.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "nds"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "ndswikibooks",
        "url": "https://nds.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "nds"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "ndswikiquote",
        "url": "https://nds.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "nds"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "yowiki",
        "url": "https://yo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "yo"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "yowiktionary",
        "url": "https://yo.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "yo"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "yowikibooks",
        "url": "https://yo.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "yo"
        }
    },
    {
        "name": "ვიკიპედია",
        "identifier": "xmfwiki",
        "url": "https://xmf.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "xmf"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "avkwiki",
        "url": "https://avk.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "avk"
        }
    },
    {
        "name": "Viquipèdia",
        "identifier": "cawiki",
        "url": "https://ca.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ca"
        }
    },
    {
        "name": "Viccionari",
        "identifier": "cawiktionary",
        "url": "https://ca.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ca"
        }
    },
    {
        "name": "Viquillibres",
        "identifier": "cawikibooks",
        "url": "https://ca.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ca"
        }
    },
    {
        "name": "Viquinotícies",
        "identifier": "cawikinews",
        "url": "https://ca.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "ca"
        }
    },
    {
        "name": "Viquidites",
        "identifier": "cawikiquote",
        "url": "https://ca.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ca"
        }
    },
    {
        "name": "Viquitexts",
        "identifier": "cawikisource",
        "url": "https://ca.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ca"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "iiwiki",
        "url": "https://ii.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ii"
        }
    },
    {
        "name": "Википедија",
        "identifier": "mkwiki",
        "url": "https://mk.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mk"
        }
    },
    {
        "name": "Викиречник",
        "identifier": "mkwiktionary",
        "url": "https://mk.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "mk"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "mkwikibooks",
        "url": "https://mk.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "mk"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "mkwikisource",
        "url": "https://mk.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "mk"
        }
    },
    {
        "name": "विकिपीडिया",
        "identifier": "mrwiki",
        "url": "https://mr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mr"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "mrwiktionary",
        "url": "https://mr.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "mr"
        }
    },
    {
        "name": "विकिबुक्स",
        "identifier": "mrwikibooks",
        "url": "https://mr.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "mr"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "mrwikiquote",
        "url": "https://mr.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "mr"
        }
    },
    {
        "name": "विकिस्रोत",
        "identifier": "mrwikisource",
        "url": "https://mr.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "mr"
        }
    },
    {
        "name": "వికీపీడియా",
        "identifier": "tewiki",
        "url": "https://te.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "te"
        }
    },
    {
        "name": "విక్షనరీ",
        "identifier": "tewiktionary",
        "url": "https://te.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "te"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "tewikibooks",
        "url": "https://te.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "te"
        }
    },
    {
        "name": "వికీవ్యాఖ్య",
        "identifier": "tewikiquote",
        "url": "https://te.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "te"
        }
    },
    {
        "name": "వికీసోర్స్",
        "identifier": "tewikisource",
        "url": "https://te.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "te"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "towiki",
        "url": "https://to.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "to"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "towiktionary",
        "url": "https://to.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "to"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "anwiki",
        "url": "https://an.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "an"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "anwiktionary",
        "url": "https://an.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "an"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "bxrwiki",
        "url": "https://bxr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bxr"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "ikwiki",
        "url": "https://ik.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ik"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "ikwiktionary",
        "url": "https://ik.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ik"
        }
    },
    {
        "name": "Уикипедиэ",
        "identifier": "kbdwiki",
        "url": "https://kbd.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kbd"
        }
    },
    {
        "name": "Википсалъалъэ",
        "identifier": "kbdwiktionary",
        "url": "https://kbd.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "kbd"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "smwiki",
        "url": "https://sm.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sm"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "smwiktionary",
        "url": "https://sm.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sm"
        }
    },
    {
        "name": "ܘܝܩܝܦܕܝܐ",
        "identifier": "arcwiki",
        "url": "https://arc.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "arc"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "ilowiki",
        "url": "https://ilo.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ilo"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "iswiki",
        "url": "https://is.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "is"
        }
    },
    {
        "name": "Wikiorðabók",
        "identifier": "iswiktionary",
        "url": "https://is.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "is"
        }
    },
    {
        "name": "Wikibækur",
        "identifier": "iswikibooks",
        "url": "https://is.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "is"
        }
    },
    {
        "name": "Wikivitnun",
        "identifier": "iswikiquote",
        "url": "https://is.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "is"
        }
    },
    {
        "name": "Wikiheimild",
        "identifier": "iswikisource",
        "url": "https://is.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "is"
        }
    },
    {
        "name": "위키백과",
        "identifier": "kowiki",
        "url": "https://ko.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ko"
        }
    },
    {
        "name": "위키낱말사전",
        "identifier": "kowiktionary",
        "url": "https://ko.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ko"
        }
    },
    {
        "name": "위키책",
        "identifier": "kowikibooks",
        "url": "https://ko.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ko"
        }
    },
    {
        "name": "위키뉴스",
        "identifier": "kowikinews",
        "url": "https://ko.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "ko"
        }
    },
    {
        "name": "위키인용집",
        "identifier": "kowikiquote",
        "url": "https://ko.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ko"
        }
    },
    {
        "name": "위키문헌",
        "identifier": "kowikisource",
        "url": "https://ko.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "ko"
        }
    },
    {
        "name": "위키배움터",
        "identifier": "kowikiversity",
        "url": "https://ko.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "ko"
        }
    },
    {
        "name": "Wîkîpediya",
        "identifier": "kuwiki",
        "url": "https://ku.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ku"
        }
    },
    {
        "name": "Wîkîferheng",
        "identifier": "kuwiktionary",
        "url": "https://ku.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ku"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "kuwikibooks",
        "url": "https://ku.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ku"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "kuwikiquote",
        "url": "https://ku.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ku"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "zawiki",
        "url": "https://za.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "za"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "zawiktionary",
        "url": "https://za.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "za"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "zawikibooks",
        "url": "https://za.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "za"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "zawikiquote",
        "url": "https://za.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "za"
        }
    },
    {
        "name": "ဝဳကဳပဳဒဳယာ",
        "identifier": "mnwwiki",
        "url": "https://mnw.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mnw"
        }
    },
    {
        "name": "ဝိက်ရှေန်နရဳ",
        "identifier": "mnwwiktionary",
        "url": "https://mnw.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "mnw"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "bat_smgwiki",
        "url": "https://bat-smg.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bat-smg"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "dawiki",
        "url": "https://da.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "da"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "dawiktionary",
        "url": "https://da.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "da"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "dawikibooks",
        "url": "https://da.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "da"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "dawikiquote",
        "url": "https://da.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "da"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "dawikisource",
        "url": "https://da.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "da"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "glwiki",
        "url": "https://gl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gl"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "glwiktionary",
        "url": "https://gl.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "gl"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "glwikibooks",
        "url": "https://gl.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "gl"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "glwikiquote",
        "url": "https://gl.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "gl"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "glwikisource",
        "url": "https://gl.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "gl"
        }
    },
    {
        "name": "Wikipiidiya",
        "identifier": "gurwiki",
        "url": "https://gur.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gur"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "hzwiki",
        "url": "https://hz.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "hz"
        }
    },
    {
        "name": "وِکیٖپیٖڈیا",
        "identifier": "kswiki",
        "url": "https://ks.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ks"
        }
    },
    {
        "name": "وِکیٖلۄغَتھ",
        "identifier": "kswiktionary",
        "url": "https://ks.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ks"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "kswikibooks",
        "url": "https://ks.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ks"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "kswikiquote",
        "url": "https://ks.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ks"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "miwiki",
        "url": "https://mi.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mi"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "miwiktionary",
        "url": "https://mi.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "mi"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "miwikibooks",
        "url": "https://mi.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "mi"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "pcdwiki",
        "url": "https://pcd.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pcd"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "pflwiki",
        "url": "https://pfl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pfl"
        }
    },
    {
        "name": "উইকিপিডিয়া",
        "identifier": "bpywiki",
        "url": "https://bpy.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "bpy"
        }
    },
    {
        "name": "Vikipediya",
        "identifier": "crhwiki",
        "url": "https://crh.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "crh"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "vecwiki",
        "url": "https://vec.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "vec"
        }
    },
    {
        "name": "Wikisionario",
        "identifier": "vecwiktionary",
        "url": "https://vec.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "vec"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "vecwikisource",
        "url": "https://vec.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "vec"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "avwiki",
        "url": "https://av.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "av"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "avwiktionary",
        "url": "https://av.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "av"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "chrwiki",
        "url": "https://chr.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "chr"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "chrwiktionary",
        "url": "https://chr.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "chr"
        }
    },
    {
        "name": "Вікіпедія",
        "identifier": "ruewiki",
        "url": "https://rue.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "rue"
        }
    },
    {
        "name": "ವಿಕಿಪೀಡಿಯ",
        "identifier": "tcywiki",
        "url": "https://tcy.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tcy"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "euwiki",
        "url": "https://eu.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "eu"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "euwiktionary",
        "url": "https://eu.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "eu"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "euwikibooks",
        "url": "https://eu.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "eu"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "euwikiquote",
        "url": "https://eu.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "eu"
        }
    },
    {
        "name": "Wikiteka",
        "identifier": "euwikisource",
        "url": "https://eu.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "eu"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "gorwiki",
        "url": "https://gor.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "gor"
        }
    },
    {
        "name": "Wikikamus",
        "identifier": "gorwiktionary",
        "url": "https://gor.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "gor"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "hifwiki",
        "url": "https://hif.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "hif"
        }
    },
    {
        "name": "Sabdkosh",
        "identifier": "hifwiktionary",
        "url": "https://hif.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "hif"
        }
    },
    {
        "name": "Vicipaedia",
        "identifier": "lawiki",
        "url": "https://la.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "la"
        }
    },
    {
        "name": "Victionarium",
        "identifier": "lawiktionary",
        "url": "https://la.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "la"
        }
    },
    {
        "name": "Vicilibri",
        "identifier": "lawikibooks",
        "url": "https://la.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "la"
        }
    },
    {
        "name": "Vicicitatio",
        "identifier": "lawikiquote",
        "url": "https://la.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "la"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "lawikisource",
        "url": "https://la.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "la"
        }
    },
    {
        "name": "Википедиесь",
        "identifier": "mdfwiki",
        "url": "https://mdf.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "mdf"
        }
    },
    {
        "name": "وکیپیڈیا",
        "identifier": "pnbwiki",
        "url": "https://pnb.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pnb"
        }
    },
    {
        "name": "وکشنری",
        "identifier": "pnbwiktionary",
        "url": "https://pnb.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "pnb"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "szlwiki",
        "url": "https://szl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "szl"
        }
    },
    {
        "name": "विकिपीडिया",
        "identifier": "anpwiki",
        "url": "https://anp.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "anp"
        }
    },
    {
        "name": "Википеди",
        "identifier": "cewiki",
        "url": "https://ce.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ce"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "enwiki",
        "url": "https://en.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "en"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "enwiktionary",
        "url": "https://en.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "en"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "enwikibooks",
        "url": "https://en.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "en"
        }
    },
    {
        "name": "Wikinews",
        "identifier": "enwikinews",
        "url": "https://en.wikinews.org",
        "code": "wikinews",
        "in_language": {
            "identifier": "en"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "enwikiquote",
        "url": "https://en.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "en"
        }
    },
    {
        "name": "Wikisource",
        "identifier": "enwikisource",
        "url": "https://en.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "en"
        }
    },
    {
        "name": "Wikiversity",
        "identifier": "enwikiversity",
        "url": "https://en.wikiversity.org",
        "code": "wikiversity",
        "in_language": {
            "identifier": "en"
        }
    },
    {
        "name": "Wikivoyage",
        "identifier": "enwikivoyage",
        "url": "https://en.wikivoyage.org",
        "code": "wikivoyage",
        "in_language": {
            "identifier": "en"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "kwwiki",
        "url": "https://kw.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kw"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "kwwiktionary",
        "url": "https://kw.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "kw"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "kwwikiquote",
        "url": "https://kw.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "kw"
        }
    },
    {
        "name": "Wikipédia",
        "identifier": "skwiki",
        "url": "https://sk.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "sk"
        }
    },
    {
        "name": "Wikislovník",
        "identifier": "skwiktionary",
        "url": "https://sk.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "sk"
        }
    },
    {
        "name": "Wikiknihy",
        "identifier": "skwikibooks",
        "url": "https://sk.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "sk"
        }
    },
    {
        "name": "Wikicitáty",
        "identifier": "skwikiquote",
        "url": "https://sk.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "sk"
        }
    },
    {
        "name": "Wikizdroje",
        "identifier": "skwikisource",
        "url": "https://sk.wikisource.org",
        "code": "wikisource",
        "in_language": {
            "identifier": "sk"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "sowiki",
        "url": "https://so.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "so"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "sowiktionary",
        "url": "https://so.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "so"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "sswiki",
        "url": "https://ss.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ss"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "sswiktionary",
        "url": "https://ss.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ss"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "tlwiki",
        "url": "https://tl.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tl"
        }
    },
    {
        "name": "Wiktionary",
        "identifier": "tlwiktionary",
        "url": "https://tl.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "tl"
        }
    },
    {
        "name": "Wikibooks",
        "identifier": "tlwikibooks",
        "url": "https://tl.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "tl"
        }
    },
    {
        "name": "Wikiquote",
        "identifier": "tlwikiquote",
        "url": "https://tl.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "tl"
        }
    },
    {
        "name": "Wikipidiya",
        "identifier": "trvwiki",
        "url": "https://trv.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "trv"
        }
    },
    {
        "name": "ვიკიპედია",
        "identifier": "kawiki",
        "url": "https://ka.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "ka"
        }
    },
    {
        "name": "ვიქსიკონი",
        "identifier": "kawiktionary",
        "url": "https://ka.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "ka"
        }
    },
    {
        "name": "ვიკიწიგნები",
        "identifier": "kawikibooks",
        "url": "https://ka.wikibooks.org",
        "code": "wikibooks",
        "in_language": {
            "identifier": "ka"
        }
    },
    {
        "name": "ვიკიციტატა",
        "identifier": "kawikiquote",
        "url": "https://ka.wikiquote.org",
        "code": "wikiquote",
        "in_language": {
            "identifier": "ka"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "kabwiki",
        "url": "https://kab.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "kab"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "pdcwiki",
        "url": "https://pdc.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "pdc"
        }
    },
    {
        "name": "Wikipedia",
        "identifier": "tetwiki",
        "url": "https://tet.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "tet"
        }
    },
    {
        "name": "維基辭典",
        "identifier": "yuewiktionary",
        "url": "https://yue.wiktionary.org",
        "code": "wiktionary",
        "in_language": {
            "identifier": "yue"
        }
    },
    {
        "name": "維基大典",
        "identifier": "zh_classicalwiki",
        "url": "https://zh-classical.wikipedia.org",
        "code": "wiki",
        "in_language": {
            "identifier": "zh-classical"
        }
    }
]
```
</details>


## Namespaces metadata
Get information on all the supported namespaces. Supports filtering and field selection. Allows to query single namespace.

```bash
GET https://api.enterprise.wikimedia.com/v2/namespaces
```

Response:
```json
[
    {
        "name": "Articles",
        "identifier": 0,
        "description": "The main namespace, article namespace, or mainspace is the namespace of Wikipedia that contains the encyclopedia proper—that is, where 'live' Wikipedia articles reside."
    },
    {
        "name": "File",
        "identifier": 6,
        "description": "The File namespace is a namespace consisting of administration pages in which all of Wikipedia's media content resides. On Wikipedia, all media filenames begin with the prefix File:, including data files for images, video clips, or audio clips, including document length clips; or MIDI files (a small file of computer music instructions)."
    },
    {
        "name": "Template",
        "identifier": 10,
        "description": "The Template namespace on Wikipedia is used to store templates, which contain Wiki markup intended for inclusion on multiple pages, usually via transclusion. Although the Template namespace is used for storing most templates, it is possible to transclude and substitute from other namespaces, and so some template pages are placed in other namespaces, such as the User namespace."
    },
    {
        "name": "Category",
        "identifier": 14,
        "description": "Categories are intended to group together pages on similar subjects. They are implemented by a MediaWiki feature that adds any page with a text like [[Category:XYZ]] in its wiki markup to the automated listing that is the category with name XYZ. Categories help readers to find, and navigate around, a subject area, to see pages sorted by title, and to thus find article relationships."
    }
]
```
## Expected Output

The script will log its progress as it steps through each example. A successful run will look similar to this:

```
INFO:__main__:Setting up authentication...
INFO:__main__:Succesfully authenticated!

INFO:__main__:Starting Metadata API examples...

INFO:__main__:--- Project Codes ---

INFO:__main__: --- Use Case 1: Get all codes ---

INFO:__main__:1) Get all project codes:
INFO:__main__:Found 15 project codes
INFO:__main__:First code details:
INFO:__main__:{
  "identifier": "commons",
  "name": "Wikimedia Commons",
  "url": "https://commons.wikimedia.org"
}

INFO:__main__:2) Get only the 'identifier' field for all codes:
INFO:__main__:Identifiers found:
INFO:__main__:[
  {
    "identifier": "commons"
  },
  {
    "identifier": "mediawiki"
  },
...
]

INFO:__main__:3) Filter for code 'wiki' and select 'identifier':
INFO:__main__:Filtered result:
INFO:__main__:[
  {
    "identifier": "wiki"
  }
]

INFO:__main__:4) Get details for specific code 'wiktionary':
INFO:__main__:Wiktionary details:
INFO:__main__:{
  "identifier": "wiktionary",
  "name": "Wiktionary",
  "url": "https://www.wiktionary.org"
}
...
INFO:__main__:--- Languages ---

INFO:__main__:1) Get all supported languages:
INFO:__main__:Found 321 languages.
INFO:__main__:Details for English ('en'):
INFO:__main__:{
  "identifier": "en",
  "name": "English",
  "direction": "ltr"
}
INFO:__main__:Details for Arabic ('ar'):
INFO:__main__:{
  "identifier": "ar",
  "name": "العربية",
  "direction": "rtl"
}
...
INFO:__main__:--- Projects ---

INFO:__main__:1) Get metadata for all supported projects:
INFO:__main__:Found 943 projects.
INFO:__main__:Details for English Wikipedia ('enwiki'):
INFO:__main__:{
  "identifier": "enwiki",
  "name": "Wikipedia",
  "url": "https://en.wikipedia.org",
...
}
...
INFO:__main__:--- Namespaces ---

INFO:__main__:1) Get metadata for all supported namespaces:
INFO:__main__:Found 28 namespaces.
INFO:__main__:Namespace details:
INFO:__main__:[
  {
    "identifier": 0,
    "name": "Article"
  },
  {
    "identifier": 1,
    "name": "Article talk"
  },
...
]

INFO:__main__:2) Get details for specific namespace ID 0 (Articles):
INFO:__main__:Namespace 0 details:
INFO:__main__:{
  "identifier": 0,
  "name": "Article"
}

INFO:__main__:--- Metadata API examples complete!
INFO:__main__:Shutting down helper and revoking tokens...
INFO:__main__:Exiting!
```
