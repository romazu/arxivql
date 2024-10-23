# arXiv Query Language
The arXiv search API enables filtering articles based on various **fields** such as "title", "author", "category", etc.
Queries follow the format `{field_prefix}:{value}`, e.g., `ti:AlexNet`.
The query language supports combining field filters using logical operators AND, OR, ANDNOT.
Constructing these queries manually presents two challenges:
1. Writing syntactically correct query strings with abbreviated field prefixes.
2. Navigating numerous arXiv category identifiers.

This repository provides a pythonic query builder to address both challenges.
See the [official documentation](https://info.arxiv.org/help/api/user-manual.html#query_details) for API details.

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

The library also provides useful category collections:

```python
from arxivql.taxonomy import Collections, categories_by_id

print(len(categories_by_id.keys()))
# Output:
# 155

print(len(Collections.all_categories))
# Output:
# 155

print(len(Collections.all_archives))
print(Q.category(Collections.all_archives))
# Output:
# 20
# cat:(cs.* econ.* eess.* math.* q-bio.* q-fin.* stat.* astro-ph.* cond-mat.* nlin.* physics.* gr-qc hep-ex hep-lat hep-ph hep-th math-ph nucl-ex nucl-th quant-ph)

# Broad machine learcning categories, see
# https://blog.arxiv.org/2019/12/05/arxiv-machine-learning-classification-guide/
print(len(Collections.machine_learning_broad))
print(Q.category(Collections.machine_learning_broad))
# Output:
# 16
# cat:(cs.LG stat.ML math.OC cs.CV cs.CL eess.AS cs.IR cs.HC cs.SI cs.CY cs.GR cs.SY cs.AI cs.MM cs.ET cs.NE)
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

- Quoted items imply exact sequence matching:
  - For text fields, this means standard phrase matching
  - For categories, order matters: `cat:"hep-th cs.AI"` differs from `cat:"cs.AI hep-th"`. Article categories are ordered in arXiv API.
  - Queries like `cat:"cs.* hep-th"` or `cat:"cs.*"` return no results as they search for literal category names, and, e.g., literal `cs.*` category does not exist.
  - Double quotes are special characters and should be carefully handled. E.g., `"""` finds nothing, and `""2"""` is equivalent to `"2"` and `2`.
  - This library raises exceptions for most such problematic queries. 

- Spaces between terms or fields imply OR operations:
  `cat:hep-th cat:cs.AI` equals `cat:hep-th OR cat:cs.AI`

- Parentheses serve two purposes:
  1. Grouping logical operations
  2. Defining field scope, e.g., `ti:(some words)` treats spaces as OR operations.
  Examples:
  - `cat:(cs.AI hep-th)` matches articles with either category
  - `cat:(cs.* hep-th)` functions as expected with wildcards

- Explicit operators in field scopes are supported:
  `ti:(some OR words)` and `ti:(some AND words)` are valid

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