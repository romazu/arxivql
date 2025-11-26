"""
Unit tests for Query class error handling and validation.
Tests that invalid queries raise appropriate exceptions.
"""

import pytest
import warnings
from arxivql import Query as Q


class TestQueryValidationErrors:
    """Tests for validation errors in Query construction."""

    def test_double_quotes_in_value_raises(self):
        """Double quotes in field value should raise ValueError."""
        with pytest.raises(ValueError, match="Double quotes and parentheses.*forbidden"):
            Q.title('"quoted words"')

    def test_parentheses_in_value_raises(self):
        """Parentheses in field value should raise ValueError."""
        with pytest.raises(ValueError, match="Double quotes and parentheses.*forbidden"):
            Q.title("(parenthesized words)")

    def test_opening_paren_in_value_raises(self):
        """Opening parenthesis in value should raise."""
        with pytest.raises(ValueError, match="Double quotes and parentheses.*forbidden"):
            Q.abstract("test (value")

    def test_closing_paren_in_value_raises(self):
        """Closing parenthesis in value should raise."""
        with pytest.raises(ValueError, match="Double quotes and parentheses.*forbidden"):
            Q.abstract("test) value")

    def test_matched_paren_in_value_raises(self):
        """Closing parenthesis in value should raise."""
        with pytest.raises(ValueError, match="Double quotes and parentheses.*forbidden"):
            Q.abstract("(test) value")


class TestQueryNegationErrors:
    """Tests for negation operator errors."""

    def test_standalone_negation_raises_on_str(self):
        """Standalone NOT operator is not supported - error on str()."""
        negated = ~Q.author("Test")
        with pytest.raises(ValueError, match="no standalone negation operator"):
            str(negated)

    def test_standalone_negation_raises_on_to_string(self):
        """Standalone NOT operator is not supported - error on to_string()."""
        negated = ~Q.category("cs.AI")
        with pytest.raises(ValueError, match="no standalone negation operator"):
            negated.to_string()

    def test_ornot_raises(self):
        """ORNOT operator is not supported in arXiv API."""
        a1 = Q.author("Author1")
        a2 = Q.author("Author2")
        with pytest.raises(ValueError, match="no ORNOT operator"):
            a1 | ~a2

    def test_double_negation(self):
        """Double negation should toggle negated state."""
        q = Q.title("test")
        assert not q.negated
        negated = ~q
        assert negated.negated
        double_negated = ~negated
        assert not double_negated.negated
        # Double negated query should work fine
        assert str(double_negated) == "ti:test"

    def test_negated_query_in_and_works(self):
        """Negated query used with AND should work (becomes ANDNOT)."""
        a1 = Q.author("Author1")
        a2 = Q.author("Author2")
        result = str(a1 & ~a2)
        assert "ANDNOT" in result

    def test_standalone_negation_in_and_chain(self):
        """Negated first operand raises when trying to use & operator."""
        negated = ~Q.title("test")
        q2 = Q.author("author")
        with pytest.raises(ValueError, match="no standalone negation operator"):
            negated & q2


class TestQueryIdDeprecationWarning:
    """Tests for deprecation warning on id field."""

    def test_id_field_warns(self):
        """Query.id() should emit deprecation warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            Q.id("2303.08774")
            assert len(w) == 1
            assert "deprecation" in str(w[0].message).lower()
            assert "id_list" in str(w[0].message)

    def test_id_field_still_works(self):
        """Query.id() should still produce valid query despite warning."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = str(Q.id("2303.08774"))
            assert result == "id:2303.08774"


class TestQueryUnquotableErrors:
    """Tests for unquotable value errors in category field."""

    def test_category_multi_word_raises(self):
        """Category with space (multi-word) should raise since quote=False."""
        # Categories don't support quoting, so multi-word values are invalid
        with pytest.raises(ValueError, match="Unquotable multi-term value"):
            Q.category("cs.NE cs.CL")
