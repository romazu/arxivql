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
import signal
import warnings
from contextlib import contextmanager
from typing import Optional

try:
    import arxiv
except ImportError:
    print("This script requires the 'arxiv' package.")
    print("Install with: pip install arxiv")
    sys.exit(1)

from arxivql import Query as Q, Taxonomy as T
from arxivql.taxonomy import catalog


@contextmanager
def _query_timeout(seconds: Optional[int]):
    """Timeout helper for blocking arxiv queries.

    Uses ``SIGALRM`` on Unix. On platforms without ``SIGALRM`` (e.g. Windows)
    or when ``seconds`` is ``None``, it is a no-op.
    """

    # No timeout requested
    if seconds is None or seconds <= 0:
        yield
        return

    # SIGALRM is not available on Windows; fall back to no-op with warning.
    if not hasattr(signal, "SIGALRM"):
        warnings.warn(
            "SIGALRM is not available on this platform; timeout_seconds has no effect.",
            RuntimeWarning,
        )
        yield
        return

    def _handle_timeout(signum, frame):
        raise TimeoutError(f"arxiv query exceeded {seconds} seconds")

    previous = signal.signal(signal.SIGALRM, _handle_timeout)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        # Restore the previous handler.
        signal.signal(signal.SIGALRM, previous)


def is_match_normaliized(normalized_query: str, raw: str, exact: bool = True) -> bool:
    """Return True if all normalized words appear in normalized raw text."""

    words = [w for w in normalized_query.split() if w]
    if not words:
        return False

    normalized_raw = raw.lower().replace("-", " ")
    if exact:
        return all(word in normalized_raw for word in words)
    else:
        return any(word in normalized_raw for word in words)


def run_query(query, max_results=None, description="", timeout_seconds: Optional[int] = None):
    """Run a query and print results.

    Any errors from the arxiv client are allowed to propagate to callers.
    Pass ``timeout_seconds=None`` to disable timeout.
    """
    if max_results is None:
        max_results = 3

    print(f"\n{'=' * 60}")
    print(f"Query: {query}")
    if description:
        print(f"Description: {description}")
    print("-" * 60)

    search = arxiv.Search(query=str(query), max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)
    client = arxiv.Client()

    with _query_timeout(timeout_seconds):
        results = list(client.results(search))

    print(f"Results: {len(results)}")
    for result in results:
        authors_str = ', '.join(a.name for a in result.authors)
        categories_str = ', '.join(result.categories)
        print(f"  {result.get_short_id()}:")
        print(f"    Title:      {result.title}")
        print(f"    Authors:    {authors_str}")
        print(f"    Categories: {categories_str}")
        # print(f"    Abstract:   {result.summary}")

    return results


def test_basic_title_query(max_results=None, timeout_seconds=None):
    """Test basic title search."""
    query = Q.title("transformer")
    results = run_query(
        query,
        max_results=max_results,
        description="Single word title search",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        # exact word match
        assert is_match_normaliized("transform", result.title)


def test_phrase_query(max_results=None, timeout_seconds=None):
    """Test phrase search with auto-quoting."""
    query = Q.title("large language model")
    results = run_query(
        query,
        max_results=max_results,
        description="Multi-word phrase (auto-quoted)",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        # exact phrase match
        assert is_match_normaliized("larg languag model", result.title)


def test_author_query(max_results=None, timeout_seconds=None):
    """Test author search."""
    query = Q.author("Ilya Sutskever")
    results = run_query(
        query,
        max_results=max_results,
        description="Author name search",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        # match at least one author
        assert any(is_match_normaliized("ilya sutskever", author.name) for author in result.authors)


def test_category_query(max_results=None, timeout_seconds=None):
    """Test category filter."""
    query = Q.category(T.cs.CL) & Q.title("GPT")
    results = run_query(
        query,
        max_results=max_results,
        description="Category + title combination",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        # match at least one category
        assert T.cs.CL.id in result.categories


def test_tuple_all_matching(max_results=None, timeout_seconds=None):
    """Test tuple for ALL matching."""
    query = Q.title(("neural", "network", "training"))
    results = run_query(
        query,
        max_results=max_results,
        description="Tuple creates AND matching",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        # match all words
        assert is_match_normaliized("neural network train", result.title)


def test_list_any_matching(max_results=None, timeout_seconds=None):
    """Test list for ANY matching."""
    query = Q.title(["topology", "crocodile", "BERT"])
    results = run_query(
        query,
        max_results=max_results,
        description="List creates OR matching",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        # match any word
        assert is_match_normaliized("topolog crocodil bert", result.title, exact=False)


def test_andnot_query(max_results=None, timeout_seconds=None):
    """Test ANDNOT exclusion."""
    query = Q.title("transformer") & ~Q.category(T.cs.CL)
    results = run_query(
        query,
        max_results=max_results,
        description="Title search excluding cs.CL category",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        # category is excluded
        assert T.cs.CL.id not in result.categories


def test_or_categories(max_results=None, timeout_seconds=None):
    """Test OR between categories."""
    query = Q.category([T.physics.hist_ph, T.physics.bio_ph]) & Q.title("energy")
    results = run_query(
        query,
        max_results=max_results,
        description="Multiple categories (OR) with title",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        # match any category
        assert any(category.id in result.categories for category in [T.physics.hist_ph, T.physics.bio_ph])


def test_archive_wildcard(max_results=None, timeout_seconds=None):
    """Test archive-level wildcard query."""
    query = Q.category(T.econ) & Q.title("quantum")
    results = run_query(
        query,
        max_results=max_results,
        description="Any of econ.* categories with title",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        # TODO: Make category archive an iterable.
        # assert any(category.id in result.categories for category in T.econ)
        categories = [field for name, field in T.econ.__dict__.items() if not name.startswith("_")]
        assert any(category.id in result.categories for category in categories)


def test_complex_query(max_results=None, timeout_seconds=None):
    """Test complex combined query from README."""
    query = Q.author("Ilya Sutskever") & Q.title("autoencoder") & ~Q.category(T.cs.AI)
    results = run_query(
        query,
        max_results=max_results,
        description="Complex query from README example",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        assert any(is_match_normaliized("ilya sutskever", author.name) for author in result.authors)
        assert is_match_normaliized("autoencod", result.title)
        assert T.cs.AI.id not in result.categories


def test_wildcard_in_title(max_results=None, timeout_seconds=None):
    """Test wildcard character in title. In general wildcards in title are brittle and not recommended."""
    query = Q.title("trans*") & Q.category(T.cs.CL)
    results = run_query(
        query,
        max_results=max_results,
        description="Wildcard in title",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        assert is_match_normaliized("tran", result.title)


def test_abstract_search(max_results=None, timeout_seconds=None):
    """Test abstract field search."""
    query = Q.abstract("self-attention mechanisms") & Q.category(T.cs.LG)
    results = run_query(
        query,
        max_results=max_results,
        description="Abstract phrase search",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        assert is_match_normaliized("self attent mechan", result.summary)


def test_catalog_search(max_results=None, timeout_seconds=None):
    """Test search using catalog."""
    query = Q.category(catalog.hep) & Q.author("Hawking") & ~ Q.title("black holes")
    results = run_query(
        query,
        max_results=max_results,
        description="Search using catalog categories",
        timeout_seconds=timeout_seconds,
    )
    for result in results:
        assert any(category.id in result.categories for category in catalog.hep)


def test_submitted_date(max_results=None, timeout_seconds=None):
    """Test submitted date filter."""
    import datetime
    # end = date(2024, 9, 2)  # still includes article 2409.01343 submitted 2024-09-02
    end = datetime.datetime(2024, 9, 3)  # excludes 2409.01343
    query = Q.author("Terence Tao") & ~ Q.submitted_date(start=None, end=end)
    # query = '(au:"Terence Tao" ANDNOT submittedDate:[100001010000 TO])'
    results = run_query(
        query,
        max_results=max_results,
        description="Author with excluded date range filter",
        timeout_seconds=timeout_seconds,
    )
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

    # Override these values for more comprehensive manual testing.
    max_results = 3
    timeout_seconds = 10
    for test_func in tests:
        try:
            test_func(max_results=max_results, timeout_seconds=timeout_seconds)
            time.sleep(0.5)
        except Exception as e:
            print(f"\nFAILED: {test_func.__name__}")
            print(f"Error: {e}")

    print("\n" + "=" * 60)
    print("Live tests complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
