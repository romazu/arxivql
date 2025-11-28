"""
Live arXiv API query tests.

These tests make actual requests to the arXiv API to verify query behavior.
They are NOT run during regular test runs (file doesn't start with "test_").

Run manually with:
    python tests/live_arxiv_queries.py

Requires: pip install arxiv
"""

import sys
import time

try:
    import arxiv
except ImportError:
    print("This script requires the 'arxiv' package.")
    print("Install with: pip install arxiv")
    sys.exit(1)

from arxivql import Query as Q, Taxonomy as T
from arxivql.taxonomy import catalog


def run_query(query, max_results=3, description=""):
    """Run a query and print results.

    Any errors from the arxiv client are allowed to propagate to callers.
    """
    print(f"\n{'=' * 60}")
    print(f"Query: {query}")
    if description:
        print(f"Description: {description}")
    print("-" * 60)

    search = arxiv.Search(query=str(query), max_results=max_results)
    client = arxiv.Client()

    results = list(client.results(search))
    print(f"Results: {len(results)}")
    for result in results:
        authors_str = ', '.join(a.name for a in result.authors)
        categories_str = ', '.join(result.categories)
        print(f"  {result.get_short_id()}:")
        print(f"    Title:      {result.title}")
        print(f"    Authors:    {authors_str}")
        print(f"    Categories: {categories_str}")

    return results


def test_basic_title_query():
    """Test basic title search."""
    query = Q.title("transformer")
    results = run_query(query, description="Single word title search")
    for result in results:
        # exact word match
        assert "transformer" in result.title.lower()


def test_phrase_query():
    """Test phrase search with auto-quoting."""
    query = Q.title("large language model")
    results = run_query(query, description="Multi-word phrase (auto-quoted)")
    for result in results:
        # exact phrase match
        assert "large language model" in result.title.lower()


def test_author_query():
    """Test author search."""
    query = Q.author("Ilya Sutskever")
    results = run_query(query, description="Author name search")
    for result in results:
        # match at least one author
        assert any("Ilya Sutskever".lower() in author.name.lower() for author in result.authors)


def test_category_query():
    """Test category filter."""
    query = Q.category(T.cs.CL) & Q.title("GPT")
    results = run_query(query, description="Category + title combination")
    for result in results:
        # match at least one category
        assert T.cs.CL.id in result.categories


def test_tuple_all_matching():
    """Test tuple for ALL matching."""
    query = Q.title(("neural", "network", "training"))
    results = run_query(query, description="Tuple creates AND matching")
    for result in results:
        # match all words
        assert all(word.lower() in result.title.lower() for word in ("neural", "network", "training"))


def test_list_any_matching():
    """Test list for ANY matching."""
    query = Q.title(["topology", "crocodile", "BERT"])
    results = run_query(query, description="List creates OR matching")
    for result in results:
        # match any word
        assert any(word.lower() in result.title.lower() for word in ["topology", "crocodile", "BERT"])


def test_andnot_query():
    """Test ANDNOT exclusion."""
    query = Q.title("transformer") & ~Q.category(T.cs.CL)
    results = run_query(query, description="Title search excluding cs.CL category")
    for result in results:
        # category is excluded
        assert T.cs.CL.id not in result.categories


def test_or_categories():
    """Test OR between categories."""
    query = Q.category([T.physics.hist_ph, T.physics.bio_ph]) & Q.title("energy")
    results = run_query(query, description="Multiple categories (OR) with title")
    for result in results:
        # match any category
        assert any(category.id in result.categories for category in [T.physics.hist_ph, T.physics.bio_ph])


def test_archive_wildcard():
    """Test archive-level wildcard query."""
    query = Q.category(T.econ) & Q.title("quantum")
    results = run_query(query, description="Any of econ.* categories with title")
    for result in results:
        # TODO: Make category archive an iterable.
        # assert any(category.id in result.categories for category in T.econ)
        categories = [field for name, field in T.econ.__dict__.items() if not name.startswith("_")]
        assert any(category.id in result.categories for category in categories)


def test_complex_query():
    """Test complex combined query from README."""
    query = Q.author("Ilya Sutskever") & Q.title("autoencoder") & ~Q.category(T.cs.AI)
    results = run_query(query, description="Complex query from README example")
    for result in results:
        assert any("Ilya Sutskever".lower() in author.name.lower() for author in result.authors)
        assert "autoencoder" in result.title.lower()
        assert T.cs.AI.id not in result.categories


def test_wildcard_in_title():
    """Test wildcard character in title."""
    query = Q.title("trans*") & Q.category(T.cs.CL)
    results = run_query(query, description="Wildcard in title")
    for result in results:
        assert "trans" in result.title.lower()


def test_abstract_search():
    """Test abstract field search."""
    query = Q.abstract("attention mechanism") & Q.category(T.cs.LG)
    results = run_query(query, description="Abstract phrase search")
    for result in results:
        assert "attention mechanism" in result.summary.lower()


def test_catalog_search():
    """Test search using catalog."""
    query = Q.category(catalog.hep) & Q.author("Hawking") & ~ Q.title("black holes")
    results = run_query(query, description="Search using catalog categories")
    for result in results:
        assert any(category.id in result.categories for category in catalog.hep)


def test_submitted_date():
    """Test submitted date filter."""
    import datetime
    # end = date(2024, 9, 2)  # still includes article 2409.01343 submitted 2024-09-02
    end = datetime.datetime(2024, 9, 3)  # excludes 2409.01343
    query = Q.author("Terence Tao") & ~ Q.submitted_date(start=None, end=end)
    results = run_query(query, description="Author with excluded date range filter")
    for result in results:
        assert result.published.astimezone(datetime.UTC).replace(tzinfo=None) > end


def main():
    """Run all live query tests."""
    print("Live arxiv api query tests")

    tests = [
        test_basic_title_query,
        test_phrase_query,
        test_author_query,
        test_category_query,
        test_tuple_all_matching,
        test_list_any_matching,
        test_andnot_query,
        test_or_categories,
        test_archive_wildcard,
        test_complex_query,
        test_wildcard_in_title,
        test_abstract_search,
        test_catalog_search,
        test_submitted_date,
    ]

    for test_func in tests:
        try:
            test_func()
            time.sleep(0.2)
        except Exception as e:
            print(f"\nFAILED: {test_func.__name__}")
            print(f"Error: {e}")

    print("\n" + "=" * 60)
    print("Live tests complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
