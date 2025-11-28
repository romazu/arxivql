"""
Unit tests for Taxonomy and Category classes.
Tests taxonomy structure and category information.
"""

import pytest
from arxivql import Taxonomy as T, Query as Q
from arxivql.taxonomy import Category


class TestCategoryDataclass:
    """Tests for Category dataclass."""

    def test_category_has_required_fields(self):
        """Category should have all expected fields."""
        cat = T.cs.AI
        assert hasattr(cat, "id")
        assert hasattr(cat, "name")
        assert hasattr(cat, "group_name")
        assert hasattr(cat, "archive_id")
        assert hasattr(cat, "archive_name")
        assert hasattr(cat, "description")

    def test_category_str(self):
        """Category __str__ returns the id."""
        cat = T.cs.AI
        assert str(cat) == "cs.AI"

    def test_category_to_string(self):
        """Category to_string() returns the id."""
        cat = T.cs.AI
        assert cat.to_string() == "cs.AI"

    def test_category_properties_cs_ai(self):
        """Test cs.AI category properties."""
        cat = T.cs.AI
        assert cat.id == "cs.AI"
        assert cat.name == "Artificial Intelligence"
        assert cat.group_name == "Computer Science"
        assert cat.archive_id == "cs"
        assert cat.archive_name == "Computer Science"
        assert len(cat.description) > 0

    def test_category_properties_astro_ph_he(self):
        """Test astro-ph.HE category properties - from README example."""
        cat = T.astro_ph.HE
        assert cat.id == "astro-ph.HE"
        assert cat.name == "High Energy Astrophysical Phenomena"
        assert cat.group_name == "Physics"
        assert cat.archive_id == "astro-ph"
        assert cat.archive_name == "Astrophysics"
        assert "Cosmic ray" in cat.description


class TestTaxonomyArchives:
    """Tests for Taxonomy archive-level access."""

    def test_cs_archive_str(self):
        """cs archive string representation uses wildcard."""
        assert str(T.cs) == "cs.*"

    def test_stat_archive_str(self):
        """stat archive string representation."""
        assert str(T.stat) == "stat.*"

    def test_math_archive_str(self):
        """math archive string representation."""
        assert str(T.math) == "math.*"

    def test_econ_archive_str(self):
        """econ archive string representation."""
        assert str(T.econ) == "econ.*"

    def test_eess_archive_str(self):
        """eess archive string representation."""
        assert str(T.eess) == "eess.*"

    def test_q_bio_archive_str(self):
        """q-bio archive string representation (note underscore in Python)."""
        assert str(T.q_bio) == "q-bio.*"

    def test_q_fin_archive_str(self):
        """q-fin archive string representation."""
        assert str(T.q_fin) == "q-fin.*"

    def test_astro_ph_archive_str(self):
        """astro-ph archive string representation (uses * not .*)."""
        assert str(T.astro_ph) == "astro-ph*"

    def test_cond_mat_archive_str(self):
        """cond-mat archive string representation."""
        assert str(T.cond_mat) == "cond-mat*"

    def test_physics_archive_str(self):
        """physics archive string representation."""
        assert str(T.physics) == "physics.*"

    def test_nlin_archive_str(self):
        """nlin archive string representation."""
        assert str(T.nlin) == "nlin.*"


class TestTaxonomySingleCategoryArchives:
    """Tests for archives that are also single categories."""

    def test_hep_th_is_category(self):
        """hep-th is both archive and category."""
        cat = T.hep_th
        assert isinstance(cat, Category)
        assert cat.id == "hep-th"
        assert str(cat) == "hep-th"

    def test_hep_ph_is_category(self):
        """hep-ph is both archive and category."""
        cat = T.hep_ph
        assert isinstance(cat, Category)
        assert cat.id == "hep-ph"

    def test_hep_ex_is_category(self):
        """hep-ex is both archive and category."""
        cat = T.hep_ex
        assert isinstance(cat, Category)
        assert cat.id == "hep-ex"

    def test_hep_lat_is_category(self):
        """hep-lat is both archive and category."""
        cat = T.hep_lat
        assert isinstance(cat, Category)
        assert cat.id == "hep-lat"

    def test_gr_qc_is_category(self):
        """gr-qc is both archive and category."""
        cat = T.gr_qc
        assert isinstance(cat, Category)
        assert cat.id == "gr-qc"

    def test_quant_ph_is_category(self):
        """quant-ph is both archive and category."""
        cat = T.quant_ph
        assert isinstance(cat, Category)
        assert cat.id == "quant-ph"

    def test_math_ph_is_category(self):
        """math-ph is both archive and category."""
        cat = T.math_ph
        assert isinstance(cat, Category)
        assert cat.id == "math-ph"

    def test_nucl_th_is_category(self):
        """nucl-th is both archive and category."""
        cat = T.nucl_th
        assert isinstance(cat, Category)
        assert cat.id == "nucl-th"

    def test_nucl_ex_is_category(self):
        """nucl-ex is both archive and category."""
        cat = T.nucl_ex
        assert isinstance(cat, Category)
        assert cat.id == "nucl-ex"


class TestCategoryIteration:
    """Tests for iterability of Category instances used as archives."""

    def test_single_category_archive_iterates_over_itself(self):
        """Single-category archives (e.g., hep-th) yield themselves when iterated."""
        cat = T.hep_th
        assert list(cat) == [cat]

    def test_non_archive_category_not_iterable(self):
        """Regular categories should not be iterable and raise TypeError."""
        cat = T.cs.AI
        with pytest.raises(TypeError):
            list(cat)


class TestArchiveLength:
    """Tests for __len__ behavior on archives and archive-like categories."""

    def test_archive_len_matches_iteration(self):
        """len(T.cs) equals the number of categories yielded by iterating over T.cs."""
        assert len(T.cs) == len(list(T.cs))

    def test_single_category_archive_len_is_one(self):
        """Single-category archives report length 1."""
        assert len(T.hep_th) == 1

    def test_regular_category_len_raises_type_error(self):
        """Regular categories do not define a length and raise TypeError on len()."""
        with pytest.raises(TypeError):
            len(T.cs.AI)


class TestTaxonomyWithQuery:
    """Tests for using Taxonomy with Query class."""

    def test_category_query(self):
        """Basic category query with Taxonomy - from README."""
        result = str(Q.category(T.cs.AI))
        assert result == "cat:cs.AI"

    def test_archive_query_with_wildcard(self):
        """Archive-level query produces wildcard - from README."""
        result = str(Q.category(T.cs))
        assert result == "cat:cs.*"

    def test_tuple_of_categories(self):
        """Tuple of categories creates AND query - from README."""
        result = str(Q.category((T.cs.LG, T.stat.ML)))
        assert result == "cat:(cs.LG AND stat.ML)"

    def test_list_of_categories(self):
        """List of categories creates OR query."""
        result = str(Q.category([T.cs.LG, T.stat.ML]))
        assert result == "cat:(cs.LG stat.ML)"

    def test_combined_category_and_title(self):
        """Combined category and title query - from README."""
        result = str(Q.category((T.cs.LG, T.stat.ML)) & Q.title("LLM"))
        assert result == "(cat:(cs.LG AND stat.ML) AND ti:LLM)"

    def test_category_with_andnot(self):
        """Category exclusion with ANDNOT."""
        result = str(Q.author("Test") & ~Q.category(T.cs.AI))
        assert result == "(au:Test ANDNOT cat:cs.AI)"


class TestLegacyCategories:
    """Tests for legacy/general categories."""

    def test_astro_ph_general(self):
        """astro-ph has a general legacy category."""
        assert T.astro_ph.general.id == "astro-ph"
        assert "legacy" in T.astro_ph.general.description.lower()

    def test_cond_mat_general(self):
        """cond-mat has a general legacy category."""
        assert T.cond_mat.general.id == "cond-mat"
        assert "legacy" in T.cond_mat.general.description.lower()
