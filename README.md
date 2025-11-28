# arXiv Query Language

[![PyPI](https://img.shields.io/pypi/v/arxivql)](https://pypi.org/project/arxivql/)
[![Tests](https://img.shields.io/github/actions/workflow/status/romazu/arxivql/tests.yml?branch=main)](https://github.com/romazu/arxivql/actions?query=branch%3Amain)

The arXiv search API enables filtering articles based on various **fields** such as "title", "author", "category", etc.
Queries follow the format `{field_prefix}:{value}`, e.g., `ti:AlexNet`.
The query language supports combining field filters using logical operators AND, OR, ANDNOT.
Constructing these queries manually presents two challenges:
1. Writing syntactically correct query strings with abbreviated field prefixes
2. Navigating numerous arXiv category identifiers

This repository provides a pythonic query builder to address both challenges.
See the [arxiv documentation](https://info.arxiv.org/help/api/user-manual.html#query_details) for the official Search API details.
See the [arXiv Search API behavior](#important-arxiv-search-api-behavior) section for API behavior details and caveats.

## Installation
```shell
pip install arxivql
```

## Query
The `Query` class provides constructors for all supported arXiv fields and methods to combine them.

### Field Constructors

```python
from arxivql import Query as Q

# Single word search
print(Q.title('word'))
# Output:
# ti:word

# Exact phrase and author name searches
print(Q.abstract('some words'))
print(Q.author("Ilya Sutskever"))
# Output:
# abs:"some words"
# au:"Ilya Sutskever"
```
Multi-word field values are automatically double-quoted for exact phrase matching.
For ANY word matching, pass a **list** to the constructor:
```python
Q.abstract(["Syntactic", "natural language processing", "synthetic corpus"])
# Output:
# abs:(Syntactic "natural language processing" "synthetic corpus")
```
For ALL words matching, pass a **tuple** to the constructor:
```python
Q.abstract(("Syntactic", "natural language processing", "synthetic corpus"))
# Output:
# abs:(Syntactic AND "natural language processing" AND "synthetic corpus")
```
Note: All searches are case-insensitive.

### Date Filtering
Filter by submission date range using `datetime` or `date` objects.
For convenience, `None` (the default) arguments make the date range open-ended.
Timezone-aware datetimes are converted to UTC.

```python
from datetime import date, datetime
from arxivql import Query as Q

# Date range (times default to 00:00 GMT)
Q.submitted_date(date(2023, 1, 1), date(2024, 1, 1))
# Output: submittedDate:[202301010000 TO 202401010000]

# With specific times
Q.submitted_date(datetime(2023, 1, 1, 6, 0), datetime(2024, 1, 1, 6, 0))
# Output: submittedDate:[202301010600 TO 202401010600]

# Open-ended ranges (None for no bound)
Q.author("Terence Tao") & Q.submitted_date(date(2020, 1, 1), None)  # From 2020 onwards
# Output: (au:"Terence Tao" AND submittedDate:[202001010000 TO 900001010000])

Q.title("GPT") & ~Q.submitted_date(None, date(2023, 1, 1))  # Exclude before 2023
# Output: (ti:GPT ANDNOT submittedDate:[100001010000 TO 202301010000])
```

### Logical Operations
Complex queries can be constructed by combining field filters using regular python logic operators:
```python
a1 = Q.author("Ilya Sutskever")
a2 = Q.author(("Geoffrey", "Hinton"))
c1 = Q.category("cs.NE")  # See taxonomy section for preferred category construction
c2 = Q.category("cs.CL")

# AND operator
q1 = a1 & a2 & c1
# Output:
# ((au:"Ilya Sutskever" AND au:(Geoffrey AND Hinton)) AND cat:cs.NE)

# OR operator
q2 = (a1 | a2) & (c1 | c2)
# Output:
# ((au:"Ilya Sutskever" OR au:(Geoffrey AND Hinton)) AND (cat:cs.NE OR cat:cs.CL))

# ANDNOT operator
q3 = a1 & ~a2
# Output:
# (au:"Ilya Sutskever" ANDNOT au:(Geoffrey AND Hinton))
```
The following operations raise exceptions due to arXiv API limitations:
```python
~a1       # Error: standalone NOT operator not supported
a1 | ~a2  # Error: ORNOT operator not supported
```

### Wildcards
Wildcards (`?` and `*`) can be used in queries as usual. See the [arXiv Search API behavior](#important-arxiv-search-api-behavior) section for more details.

### Category Taxonomy
The `Taxonomy` class provides a structured interface for managing arXiv categories.
Basic usage:

```python
from arxivql import Taxonomy as T

print(T.cs.AI)
print(Q.category(T.cs.AI))
print(Q.category(T.cs))
print(Q.category((T.cs.LG, T.stat.ML)) & Q.title("LLM"))
# Output:
# cs.AI
# cat:cs.AI
# cat:cs.*
# (cat:(cs.LG AND stat.ML) AND ti:LLM)
```
Note the wildcard syntax in archive-level queries (e.g., `T.cs`).

The Taxonomy class provides comprehensive category information:
```python
category = T.astro_ph.HE
print("id:          ", category.id)
print("name:        ", category.name)
print("group_name:  ", category.group_name)
print("archive_id:  ", category.archive_id)
print("archive_name:", category.archive_name)
print("description: ", category.description)
# Output:
# id:           astro-ph.HE
# name:         High Energy Astrophysical Phenomena
# group_name:   Physics
# archive_id:   astro-ph
# archive_name: Astrophysics
# description:  Cosmic ray production, acceleration, propagation, detection. Gamma ray astronomy and bursts, X-rays, charged particles, supernovae and other explosive phenomena, stellar remnants and accretion systems, jets, microquasars, neutron stars, pulsars, black holes
```

The library also provides useful category catalog:

```python
from arxivql.taxonomy import catalog, categories_by_id

print(len(categories_by_id.keys()))
# Output:
# 157

print(len(catalog.all_categories))
# Output:
# 157

print(len(catalog.all_archives))
print(Q.category(catalog.all_archives))
# Output:
# 20
# cat:(cs.* econ.* eess.* math.* q-bio.* q-fin.* stat.* astro-ph* cond-mat* nlin.* physics.* gr-qc hep-ex hep-lat hep-ph hep-th math-ph nucl-ex nucl-th quant-ph)

# Broad Machine Learning categories, see official classification guide
# https://blog.arxiv.org/2019/12/05/arxiv-machine-learning-classification-guide
print(len(catalog.ml_broad))
print(Q.category(catalog.ml_broad))
# Output:
# 16
# cat:(cs.LG stat.ML math.OC cs.CV cs.CL eess.AS cs.IR cs.HC cs.SI cs.CY cs.GR cs.SY cs.AI cs.MM cs.ET cs.NE)

# Core Machine Learning categories according to Andrej Karpathy's `arxiv sanity preserver` project:
# https://github.com/karpathy/arxiv-sanity-preserver
print(len(catalog.ml_karpathy))
print(Q.category(catalog.ml_karpathy))
# Output:
# 6
# cat:(cs.CV cs.AI cs.CL cs.LG cs.NE stat.ML)
```

### Usage with Python arXiv Client
Constructed queries can be directly used in [python arXiv API wrapper](https://pypi.org/project/arxiv):

```python
# pip install arxiv

import arxiv
from arxivql import Query as Q, Taxonomy as T

query = Q.author("Ilya Sutskever") & Q.title("autoencoders") & ~Q.category(T.cs.AI)
search = arxiv.Search(query=query)
client = arxiv.Client()
results = list(client.results(search))

print(f"query = {query}")
for result in results:
    print(result.get_short_id(), result.title)

# Output:
# query = ((au:"Ilya Sutskever" AND ti:autoencoders) ANDNOT cat:cs.AI)
# 1611.02731v2 Variational Lossy Autoencoder
```

## Important arXiv Search API Behavior
- Category searches consider all listed categories, not only primary ones.

- arXiv supports two wildcard characters: `?` and `*`.
  - `?` replaces one character in a word
  - `*` replaces zero or more characters in a word
  - They don't match the first character of the term, i.e., `au:??tskever` fails, but `au:Sutske???` is okay
  - Categories can also be "wildcarded", i.e., `cat:cs.?I` is a valid filter
  - `?` and `*` can be combined, e.g., `cat:q-?i*` is valid and matches both `q-bio` and `q-fin`
  - Text fields other than `author` and `category` are stemmed (see the notes on normalization and API quirks below), which means that wildcards often do not work as expected on them.

- arXiv search engine internally normalizes input terms before matching (based on observed behavior -- this is not documented in the official API):
  - Terms are lowercased, hyphens are replaced with spaces, text is tokenized into words, and each token is stemmed with a Porter-like stemmer before being reassembled into a query string.
  - Example normalizations:
    - `transformers` → `transform`
    - `self-attention mechanisms` → `self attent mechan`
  - This normalization also applies to quoted searches. For example, `ti:"mechanics"` can match both "mechanic" and "mechanism", because `mechanics` is normalized to `mechan`. More on quoted-query behavior below.
  - The `author` field is not stemmed, so `au:john` and `au:johns` are different queries.
  - Because of this normalization, the following queries are equivalent:

    ```text
    abs:("self-attention mechanisms")
    abs:("Mechanisms Attention Self")
    abs:"self-attention mechanisms"
    abs:"selfs attentive mechanics"
    abs:"-- selfs -- --- attentive----mechanics --"
    abs:("-- -- mechaniC --- ATTENTIVE----seLfs --")
    ```

  - You can approximate this normalization locally using NLTK:

    ```python
    import nltk

    nltk.download("punkt_tab")
    stemmer = nltk.PorterStemmer()


    def normalize_text(text: str) -> str:
        text_clean = text.lower()
        text_clean = text_clean.replace("-", " ")
        tokens = nltk.word_tokenize(text_clean)
        stemmed = [stemmer.stem(token) for token in tokens]
        return " ".join(stemmed)


    print(normalize_text("transformers"))
    print(normalize_text("self-attention mechanisms"))
    # Output:
    # transform
    # self attent mechan
    ```

- Quoted items imply exact matching, but:
  - For regular text fields (i.e., all except categories), this behaves like an AND operator over all normalized words in the quoted phrase in any order (see normalization note above), rather than strict character-by-character phrase matching.
  - For categories, quoted multi-category queries don't work at all. For example, `cat:"hep-th cs.AI"` and `cat:"cs.* hep-th"` don't match anything and give zero results. The `Q.category` constructor in this library raises an exception for this case.
  - Single categories can be quoted (`cat:"cs.*"`), but this is redundant.
  - Beyond the usages above, double quotes are special characters and should be carefully handled. They often give unintuitive results: for example, `ti:"` returns an error, while `ti:""`, `ti:""""`, and `ti:"""""` return identical matches without a `"` character in them, and `""2"""` is equivalent to `""2""` but not to `"2"`.
  - This library raises exceptions for most such problematic queries.

- Spaces between terms or fields imply OR operations:
  `cat:hep-th cat:cs.AI` equals `cat:hep-th OR cat:cs.AI`

- Parentheses serve two purposes:
  1. Grouping logical operations
  2. Defining field scope, e.g., `ti:(some words)` treats spaces as OR operations.
  Examples:
     - `cat:(cs.AI hep-th)` matches articles with either category
     - `cat:(cs.* hep-th)` functions as expected with wildcards
  3. Note that several categories inside `cat` parentheses are okay.

- Explicit operators in field scopes are supported:
  `ti:(some OR words)` and `ti:(some AND words)` are valid.

- The `id_list` parameter (and legacy `id:` field filter) in the arXiv Search API is used internally to filter over the "major" article IDs (`2410.21276`), not the "version" IDs (`2410.21276v1`).
  - When used with a non-empty query:
    ```python
    # pip install arxiv
    
    arxiv.Search(query="au:Sutskever", id_list=["2303.08774v6"])  # zero results
    arxiv.Search(query="au:Sutskever", id_list=["2303.08774"])    # -> 2303.08774v6 (latest)
    ```
  - BUT if the query is left empty, `id_list` and `id:` can be used to search for the exact article version:
    ```python
    arxiv.Search(id_list=["2303.08774"])     # -> 2303.08774v6 (latest)
    arxiv.Search(id_list=["2303.08774v4"])   # -> 2303.08774v4
    arxiv.Search(id_list=["2303.08774v5"])   # -> 2303.08774v5
    arxiv.Search(id_list=["2303.08774v99"])  # -> obscure error
    ```

- Empty query matches all article, i.e., no filtering is applied.

- There are some other unintuitive API quirks:
  - Query `all:-` (or just `-`) matches actual "-" character across different article fields. But `ti:-` and `abs:-` match nothing.
  - Query `all:atte?tion` works as expected, but `abs:atte?tion` returns only 5 matches and `ti:atte?tion` returns zero matches.
  - Queries `ti:atten?` and `ti:atten*` return identical results, as if "attention" was searched for. But `ti:attent?` returns nothing. This is probably because the stem of "attention" is "attent", which matches `atten?` but not `attent?`.
  - And likely more.

# arXiv Categories Taxonomy
The arXiv taxonomy consists of three hierarchical levels: group → archive → category.
For complete details, consult the [arXiv Category Taxonomy](https://arxiv.org/category_taxonomy) and [arXiv Catchup Interface](https://arxiv.org/catchup).

## Category
Categories represent the finest granularity of classification.
Category identifiers typically follow the pattern `{archive}.{category}`, with some exceptions noted below.
Example: In `astro-ph.HE`, the hierarchy is:
- Group: `Physics`
- Archive: `Astrophysics`
- Category: `High Energy Astrophysical Phenomena`
- Queryable ID: `astro-ph.HE`

<img src="https://raw.githubusercontent.com/romazu/arxivql/main/assets/images/taxonomy_astro-ph.HE-fs8.png" width="35%">

## Group
Groups constitute the top level of taxonomy, currently including:
- Computer Science
- Economics
- Electrical Engineering and Systems Science
- Mathematics
- Physics
- Quantitative Biology
- Quantitative Finance
- Statistics

## Archive
Archives form the intermediate level, with each belonging to exactly one group.

Special cases:
1. Single-archive groups:
   - When a group contains only one archive, they share the same name
   - Example: `q-fin.CP` category has `Quantitative Finance` → `Quantitative Finance` → `Computational Finance`

   <img src="https://raw.githubusercontent.com/romazu/arxivql/main/assets/images/taxonomy_q-fin.CP-fs8.png" width="35%">

2. Single-category archives:
   - When an archive contains only one category, the archive name is omitted from the identifier
   - Example: `hep-th` category has `Physics` → `High Energy Physics - Theory` → `High Energy Physics - Theory`

   <img src="https://raw.githubusercontent.com/romazu/arxivql/main/assets/images/taxonomy_hep-th-fs8.png" width="35%">

Note: The `Physics` group contains a `Physics` archive alongside other archives, which may cause confusion.

# Testing
The library includes a comprehensive test suite.

## Unit Tests
Unit tests verify query construction without making arXiv API calls:
```shell
pip install pytest
pytest tests/
```

## Manual Live arXiv API Tests
Live tests make actual requests to the arXiv API to verify query behavior:
```shell
pip install arxiv
python tests/live_arxiv_queries.py
```
or
```shell
pytest tests/live_arxiv_queries.py
```
Note: Live tests are not run by pytest (the file is intentionally not prefixed with `test_`).
