"""
Unit tests for the Query class.
Tests query building functionality without making actual arXiv API calls.
"""

from arxivql import Query as Q


class TestQueryFieldConstructors:
    """Tests for Query field constructor methods - single word conversion."""

    def test_title(self):
        assert str(Q.title("word")) == "ti:word"

    def test_author(self):
        assert str(Q.author("Sutskever")) == "au:Sutskever"

    def test_abstract(self):
        assert str(Q.abstract("neural")) == "abs:neural"

    def test_category(self):
        assert str(Q.category("cs.AI")) == "cat:cs.AI"

    def test_comment(self):
        assert str(Q.comment("ICLR")) == "co:ICLR"

    def test_journal(self):
        assert str(Q.journal("Nature")) == "jr:Nature"

    def test_report(self):
        assert str(Q.report("TR-123")) == "rn:TR-123"

    def test_all(self):
        assert str(Q.all("transformers")) == "all:transformers"


class TestQueryValueFormats:
    """Tests for quoting, list (ANY), and tuple (ALL) value formats.
    
    Uses abstract field to demonstrate all formatting behaviors.
    Other fields use the same underlying logic.
    """

    def test_multi_word_auto_quotes(self):
        """Multi-word values are automatically quoted for phrase matching."""
        assert str(Q.abstract("some words")) == 'abs:"some words"'

    def test_list_any_matching(self):
        """List input creates OR (ANY) matching with parentheses."""
        result = str(Q.abstract(["word1", "word2", "word3"]))
        assert result == "abs:(word1 word2 word3)"

    def test_list_with_phrases(self):
        """List with multi-word items quotes the phrases."""
        result = str(Q.abstract(["single", "multi word phrase"]))
        assert result == 'abs:(single "multi word phrase")'

    def test_tuple_all_matching(self):
        """Tuple input creates AND (ALL) matching."""
        result = str(Q.abstract(("word1", "word2", "word3")))
        assert result == "abs:(word1 AND word2 AND word3)"

    def test_tuple_with_phrases(self):
        """Tuple with multi-word items quotes the phrases - from README."""
        result = str(Q.abstract(("Syntactic", "natural language processing", "synthetic corpus")))
        assert result == 'abs:(Syntactic AND "natural language processing" AND "synthetic corpus")'

    def test_list_readme_example(self):
        """List example from README."""
        result = str(Q.abstract(["Syntactic", "natural language processing", "synthetic corpus"]))
        assert result == 'abs:(Syntactic "natural language processing" "synthetic corpus")'


class TestCategoryValueFormats:
    """Tests for category field value formats.
    
    Category field uses quote=False, so multi-word strings raise errors
    instead of being quoted. Use list/tuple for multiple categories.
    Compare with TestQueryValueFormats which tests quoting behavior.
    """

    def test_single_category(self):
        """Single category - no special formatting."""
        assert str(Q.category("cs.AI")) == "cat:cs.AI"

    def test_multi_word_raises_error(self):
        """Multi-word string raises error (use list instead)."""
        import pytest
        # Category doesn't quote, so multi-word strings are invalid
        with pytest.raises(ValueError, match="Unquotable multi-term"):
            Q.category("cs.AI cs.LG")
        # Compare: abstract would quote this successfully
        assert str(Q.abstract("some words")) == 'abs:"some words"'

    def test_list_any_matching(self):
        """List input creates OR (ANY) matching."""
        result = str(Q.category(["cs.AI", "cs.LG", "stat.ML"]))
        assert result == "cat:(cs.AI cs.LG stat.ML)"

    def test_tuple_all_matching(self):
        """Tuple input creates AND (ALL) matching."""
        result = str(Q.category(("cs.LG", "stat.ML")))
        assert result == "cat:(cs.LG AND stat.ML)"

    def test_tuple_readme_example(self):
        """Tuple example from README."""
        from arxivql import Taxonomy as T
        result = str(Q.category((T.cs.LG, T.stat.ML)))
        assert result == "cat:(cs.LG AND stat.ML)"

    def test_list_with_taxonomy(self):
        """List with Taxonomy objects."""
        from arxivql import Taxonomy as T
        result = str(Q.category([T.cs.CV, T.cs.AI, T.cs.CL]))
        assert result == "cat:(cs.CV cs.AI cs.CL)"

    def test_archive_wildcard(self):
        """Archive-level category produces wildcard."""
        from arxivql import Taxonomy as T
        assert str(Q.category(T.cs)) == "cat:cs.*"
        assert str(Q.category(T.stat)) == "cat:stat.*"

    def test_single_category_archive(self):
        """Single-category archives have no dot in ID."""
        from arxivql import Taxonomy as T
        assert str(Q.category(T.hep_th)) == "cat:hep-th"
        assert str(Q.category(T.quant_ph)) == "cat:quant-ph"


class TestQueryLogicalOperations:
    """Tests for Query logical operators (AND, OR, ANDNOT)."""

    def test_and_operator(self):
        """AND operator between two queries."""
        a1 = Q.author("Ilya Sutskever")
        a2 = Q.author(("Geoffrey", "Hinton"))
        result = str(a1 & a2)
        assert result == '(au:"Ilya Sutskever" AND au:(Geoffrey AND Hinton))'

    def test_and_chain(self):
        """Chain of AND operators - from README example."""
        a1 = Q.author("Ilya Sutskever")
        a2 = Q.author(("Geoffrey", "Hinton"))
        c1 = Q.category("cs.NE")
        result = str(a1 & a2 & c1)
        assert result == '((au:"Ilya Sutskever" AND au:(Geoffrey AND Hinton)) AND cat:cs.NE)'

    def test_or_operator(self):
        """OR operator between two queries."""
        c1 = Q.category("cs.NE")
        c2 = Q.category("cs.CL")
        result = str(c1 | c2)
        assert result == "(cat:cs.NE OR cat:cs.CL)"

    def test_mixed_and_or(self):
        """Mixed AND and OR operators - from README example."""
        a1 = Q.author("Ilya Sutskever")
        a2 = Q.author(("Geoffrey", "Hinton"))
        c1 = Q.category("cs.NE")
        c2 = Q.category("cs.CL")
        result = str((a1 | a2) & (c1 | c2))
        assert result == '((au:"Ilya Sutskever" OR au:(Geoffrey AND Hinton)) AND (cat:cs.NE OR cat:cs.CL))'

    def test_andnot_operator(self):
        """ANDNOT operator using ~ (invert)."""
        a1 = Q.author("Ilya Sutskever")
        a2 = Q.author(("Geoffrey", "Hinton"))
        result = str(a1 & ~a2)
        assert result == '(au:"Ilya Sutskever" ANDNOT au:(Geoffrey AND Hinton))'

    def test_complex_query_with_andnot(self):
        """Complex query with ANDNOT - from README usage example."""
        from arxivql import Taxonomy as T
        query = Q.author("Ilya Sutskever") & Q.title("autoencoders") & ~Q.category(T.cs.AI)
        result = str(query)
        assert result == '((au:"Ilya Sutskever" AND ti:autoencoders) ANDNOT cat:cs.AI)'

    def test_and_with_string(self):
        """AND operator with string auto-wraps in Query.all()."""
        q = Q.category("cs.AI") & "machine learning"
        result = str(q)
        assert result == '(cat:cs.AI AND all:"machine learning")'

    def test_rand_with_string(self):
        """Right-side AND with string."""
        q = "neural networks" & Q.category("cs.NE")
        result = str(q)
        assert result == '(all:"neural networks" AND cat:cs.NE)'

    def test_or_with_string(self):
        """OR operator with string."""
        q = Q.category("cs.AI") | "transformers"
        result = str(q)
        assert result == "(cat:cs.AI OR all:transformers)"

    def test_ror_with_string(self):
        """Right-side OR with string."""
        q = "transformers" | Q.category("cs.AI")
        result = str(q)
        assert result == "(all:transformers OR cat:cs.AI)"


class TestQueryStringConversion:
    """Tests for Query string conversion and to_string method."""

    def test_str_method(self):
        """__str__ returns same as to_string()."""
        q = Q.title("test")
        assert str(q) == q.to_string()


class TestQueryWithWildcards:
    """Tests for queries with wildcard characters."""

    def test_wildcard_asterisk(self):
        """Asterisk wildcard in query."""
        result = str(Q.title("transform*"))
        assert result == "ti:transform*"

    def test_wildcard_question_mark(self):
        """Question mark wildcard in query."""
        result = str(Q.author("Suts???er"))
        assert result == "au:Suts???er"

    def test_wildcard_question_mark_at_first_character(self):
        """Question mark wildcard in query at first character of a string."""
        result = str(Q.author("??tskever"))
        assert result == "au:??tskever"

    def test_category_wildcard(self):
        """Category with wildcard."""
        result = str(Q.category("cs.*"))
        assert result == "cat:cs.*"

    def test_mixed_wildcards(self):
        """Mixed wildcards."""
        result = str(Q.category("q-?i*"))
        assert result == "cat:q-?i*"


class TestQuerySubmittedDate:
    """Tests for submitted_date filter."""

    def test_with_date_objects(self):
        """Date objects default to midnight (0000)."""
        from datetime import date
        result = str(Q.submitted_date(date(2023, 1, 1), date(2024, 1, 1)))
        assert result == "submittedDate:[202301010000 TO 202401010000]"

    def test_with_datetime_objects(self):
        """Datetime objects preserve hour and minute."""
        from datetime import datetime
        result = str(Q.submitted_date(
            datetime(2023, 1, 1, 6, 0),
            datetime(2024, 1, 1, 6, 0)
        ))
        assert result == "submittedDate:[202301010600 TO 202401010600]"

    def test_with_mixed_date_datetime(self):
        """Can mix date and datetime."""
        from datetime import date, datetime
        result = str(Q.submitted_date(date(2023, 1, 1), datetime(2024, 1, 1, 12, 30)))
        assert result == "submittedDate:[202301010000 TO 202401011230]"

    def test_combined_with_author(self):
        """Combine with other query fields."""
        from datetime import date
        query = Q.author("Terence Tao") & Q.submitted_date(date(2023, 1, 1), date(2024, 1, 1))
        result = str(query)
        assert result == '(au:"Terence Tao" AND submittedDate:[202301010000 TO 202401010000])'

    def test_open_ended_start(self):
        """None start creates open-ended range."""
        from datetime import date
        result = str(Q.submitted_date(None, date(2024, 1, 1)))
        assert result == "submittedDate:[100001010000 TO 202401010000]"

    def test_open_ended_end(self):
        """None end creates open-ended range."""
        from datetime import date
        result = str(Q.submitted_date(date(2023, 1, 1), None))
        assert result == "submittedDate:[202301010000 TO 900001010000]"

    def test_open_ended_with_negation(self):
        """Open-ended range with ANDNOT for exclusion."""
        from datetime import date
        query = Q.author("Tao") & ~Q.submitted_date()
        result = str(query)
        assert "ANDNOT submittedDate:[100001010000 TO 900001010000]" in result

    def test_timezone_aware_datetime_converted_to_utc(self):
        """Timezone-aware datetimes are auto-converted to UTC."""
        from datetime import datetime, timezone, timedelta
        tz = timezone(timedelta(hours=9))
        dt_local = datetime(2023, 1, 1, 5, 0, tzinfo=tz)  # 05:00 UTC+9 = 20:00 UTC the day before
        result = str(Q.submitted_date(dt_local, None))
        assert "202212312000" in result  # 20:00 UTC
