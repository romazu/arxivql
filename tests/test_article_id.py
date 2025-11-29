from arxivql import ArticleId


def check_reconstruction(article_id: str) -> None:
    aid = ArticleId.from_id(article_id)
    assert aid.id == article_id
    assert aid._reconstruct_id() == article_id


class TestParseArticleId:
    def test_full_fields_for_arxiv_1805_12345v2(self):
        aid = ArticleId.from_id("   arXiv:1805.12345v2 ")
        assert aid.base_id == "1805.12345"
        assert aid.version == 2
        assert aid.year == 2018
        assert aid.month == 5
        assert aid.number == 12345
        assert aid.prefix == "arXiv"
        assert aid.archive is None
        assert aid.subject is None
        assert aid.id == "arXiv:1805.12345v2"

    def test_full_fields_for_1805_12345(self):
        aid = ArticleId.from_id("1805.12345")
        assert aid.base_id == "1805.12345"
        assert aid.version is None
        assert aid.year == 2018
        assert aid.month == 5
        assert aid.number == 12345
        assert aid.prefix is None
        assert aid.archive is None
        assert aid.subject is None
        assert aid.id == "1805.12345"

    def test_full_fields_for_arxiv_quant_ph_0201082v1(self):
        aid = ArticleId.from_id("arXiv:quant-ph/0201082v1")
        assert aid.base_id == "quant-ph/0201082"
        assert aid.version == 1
        assert aid.year == 2002
        assert aid.month == 1
        assert aid.number == 82
        assert aid.prefix == "arXiv"
        assert aid.archive == "quant-ph"
        assert aid.subject is None
        assert aid.id == "arXiv:quant-ph/0201082v1"

    def test_full_fields_for_quant_ph_0201082(self):
        aid = ArticleId.from_id("quant-ph/0201082")
        assert aid.base_id == "quant-ph/0201082"
        assert aid.version is None
        assert aid.year == 2002
        assert aid.month == 1
        assert aid.number == 82
        assert aid.prefix is None
        assert aid.archive == "quant-ph"
        assert aid.subject is None
        assert aid.id == "quant-ph/0201082"

    def test_reconstruct_new_format_5digits(self):
        # new format with 5-digit number
        check_reconstruction("1805.12345")
        check_reconstruction("1805.12345v1")
        check_reconstruction("1805.12345v2")
        check_reconstruction("arXiv:1805.12345")
        check_reconstruction("arXiv:1805.12345v2")

    def test_reconstruct_new_format_4digits(self):
        # last 4-digit number in new format
        check_reconstruction("1412.8770")
        check_reconstruction("1412.8770v1")
        check_reconstruction("arXiv:1412.8770")
        check_reconstruction("arXiv:1412.8770v1")

    def test_reconstruct_legacy_format_with_subject(self):
        # legacy format with a subject class
        check_reconstruction("math.GT/0309136")
        check_reconstruction("math.GT/0309136v1")
        check_reconstruction("arXiv:math.GT/0309136")
        check_reconstruction("arXiv:math.GT/0309136v1")

    def test_reconstruct_legacy_formats(self):
        # assorted legacy archives
        check_reconstruction("cmp-lg/9404001")
        check_reconstruction("cs/0411052")
        check_reconstruction("q-bio/0703067")
        check_reconstruction("quant-ph/0201082v1")
        check_reconstruction("physics/9403001v1")
