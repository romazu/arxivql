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
    """Run a query and print results."""
    print(f"\n{'=' * 60}")
    print(f"Query: {query}")
    if description:
        print(f"Description: {description}")
    print("-" * 60)

    search = arxiv.Search(query=str(query), max_results=max_results)
    client = arxiv.Client()

    try:
        results = list(client.results(search))
        print(f"Results: {len(results)}")
        for result in results:
            authors_str = ', '.join(a.name for a in result.authors)
            print(f"  {result.get_short_id()}: {result.title}")
            print(f"    Categories: {result.categories}")
            print(f"    Authors: {authors_str}")
    except Exception as e:
        print(f"Error: {e}")


def test_basic_title_query():
    """Test basic title search."""
    query = Q.title("transformer")
    run_query(query, description="Single word title search")


def test_phrase_query():
    """Test phrase search with auto-quoting."""
    query = Q.title("large language model")
    run_query(query, description="Multi-word phrase (auto-quoted)")


def test_author_query():
    """Test author search."""
    query = Q.author("Ilya Sutskever")
    run_query(query, description="Author name search")


def test_category_query():
    """Test category filter."""
    query = Q.category(T.cs.CL) & Q.title("GPT")
    run_query(query, description="Category + title combination")


def test_tuple_all_matching():
    """Test tuple for ALL matching."""
    query = Q.title(("neural", "network", "training"))
    run_query(query, description="Tuple creates AND matching")


def test_list_any_matching():
    """Test list for ANY matching."""
    query = Q.title(["transformer", "attention", "BERT"])
    run_query(query, description="List creates OR matching")


def test_andnot_query():
    """Test ANDNOT exclusion."""
    query = Q.title("transformer") & ~Q.category(T.cs.CL)
    run_query(query, description="Title search excluding cs.CL category")


def test_or_categories():
    """Test OR between categories."""
    query = Q.category([T.cs.LG, T.stat.ML]) & Q.title("reinforcement")
    run_query(query, description="Multiple categories (OR) with title")


def test_archive_wildcard():
    """Test archive-level wildcard query."""
    query = Q.category(T.cs) & Q.title("quantum")
    run_query(query, description="All CS categories (cs.*) with title")


def test_complex_query():
    """Test complex combined query from README."""
    query = Q.author("Ilya Sutskever") & Q.title("autoencoders") & ~Q.category(T.cs.AI)
    run_query(query, description="Complex query from README example")


def test_wildcard_in_title():
    """Test wildcard character in title."""
    query = Q.title("trans*") & Q.category(T.cs.CL)
    run_query(query, description="Wildcard in title")


def test_abstract_search():
    """Test abstract field search."""
    query = Q.abstract("self-attention mechanism") & Q.category(T.cs.LG)
    run_query(query, description="Abstract phrase search")


def test_catalog_search():
    """Test search using catalog."""
    query = Q.category(catalog.hep) & Q.author("Hawking") & ~ Q.title("black holes")
    run_query(query, description="Search using catalog categories")


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
