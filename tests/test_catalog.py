"""
Unit tests for catalog and categories_by_id.
Tests the category catalog and lookup functionality.
"""

from arxivql import Taxonomy as T, Query as Q
from arxivql.taxonomy import Category, catalog, categories_by_id


class TestCategoriesById:
    """Tests for categories_by_id dictionary."""

    def test_categories_by_id_count(self):
        """Should have 157 categories - from README."""
        assert len(categories_by_id) == 157

    def test_lookup_by_id(self):
        """Can lookup category by id string."""
        cat = categories_by_id["cs.AI"]
        assert isinstance(cat, Category)
        assert cat.id == "cs.AI"
        assert cat.name == "Artificial Intelligence"

    def test_lookup_hep_th(self):
        """Can lookup hep-th (single-category archive)."""
        cat = categories_by_id["hep-th"]
        assert cat.id == "hep-th"
        assert cat.name == "High Energy Physics - Theory"

    def test_all_ids_are_strings(self):
        """All keys are strings."""
        for key in categories_by_id.keys():
            assert isinstance(key, str)

    def test_all_values_are_categories(self):
        """All values are Category instances."""
        for value in categories_by_id.values():
            assert isinstance(value, Category)

    def test_id_matches_key(self):
        """Category.id matches its key in the dictionary."""
        for key, cat in categories_by_id.items():
            assert key == cat.id


class TestCatalogAllCategories:
    """Tests for catalog.all_categories."""

    def test_all_categories_count(self):
        """Should have 157 categories - from README."""
        assert len(catalog.all_categories) == 157

    def test_all_categories_are_category_instances(self):
        """All items are Category instances."""
        for cat in catalog.all_categories:
            assert isinstance(cat, Category)

    def test_all_categories_contains_cs_ai(self):
        """Should contain cs.AI."""
        ids = [cat.id for cat in catalog.all_categories]
        assert "cs.AI" in ids

    def test_all_categories_contains_hep_th(self):
        """Should contain hep-th."""
        ids = [cat.id for cat in catalog.all_categories]
        assert "hep-th" in ids


class TestCatalogAllArchives:
    """Tests for catalog.all_archives."""

    def test_all_archives_count(self):
        """Should have 20 archives - from README."""
        assert len(catalog.all_archives) == 20

    def test_all_archives_query(self):
        """Query with all archives - from README example."""
        result = str(Q.category(catalog.all_archives))
        # Check it contains some of expected archive patterns
        assert "cs.*" in result
        assert "stat.*" in result
        assert "math.*" in result
        assert "astro-ph*" in result
        assert "hep-th" in result
        assert "quant-ph" in result

    def test_all_archives_in_parentheses(self):
        """All archives query should be in parentheses for OR."""
        result = str(Q.category(catalog.all_archives))
        assert result.startswith("cat:(")
        assert result.endswith(")")

    def test_archive_iteration_matches_catalog_filter(self):
        """Archive iteration matches filtering by archive_id in catalog.all_categories."""
        cs_from_iter = {cat.id for cat in T.cs}
        cs_from_catalog = {cat.id for cat in catalog.all_categories if cat.archive_id == "cs"}
        assert cs_from_iter == cs_from_catalog

    def test_all_archives_iteration_covers_all_categories(self):
        """Iterating over all_archives yields exactly all_categories."""
        ids_from_archives = {
            cat.id
            for archive in catalog.all_archives
            for cat in archive
        }
        ids_from_all_categories = {cat.id for cat in catalog.all_categories}
        assert ids_from_archives == ids_from_all_categories


class TestCatalogVariants:
    """Tests for catalog.ml_broad - broad Machine Learning categories."""

    def test_ml_broad_count(self):
        """Should have 16 categories - from README."""
        assert len(catalog.ml_broad) == 16

    def test_ml_karpathy_count(self):
        """Should have 6 categories - from README."""
        assert len(catalog.ml_karpathy) == 6

    def test_hep_count(self):
        """Should have 4 HEP categories."""
        assert len(catalog.hep) == 4

    def test_catalog_as_tuple_creates_and(self):
        """Converting ml_broad to tuple creates AND query."""
        result = str(Q.category(tuple(catalog.ml_broad)))
        assert " AND " in result

    def test_catalog_combined_with_field(self):
        """Combine ml_broad with author search."""
        q = Q.category(catalog.ml_broad) & Q.author("Hinton")
        result = str(q)
        assert "cat:(" in result
        assert "cs.AI" in result
        assert "AND" in result
        assert "au:Hinton" in result
