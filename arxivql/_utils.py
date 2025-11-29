import dataclasses
import re
from typing import Optional


@dataclasses.dataclass
class ArticleId:
    base_id: str
    version: Optional[int]
    year: int
    month: int
    number: int
    prefix: Optional[str]  # "arXiv" prefix if present

    # Legacy format:
    archive: Optional[str]

    # "Subject Class" is an old name for "Category".
    # Currently, it's always empty for all articles in full arXiv metadata snapshot, even for old articles.
    # E.g., "math.GT/0309136" is now referred as "math/0309136".
    subject: Optional[str] = None

    @property
    def id(self):
        prefix = f"{self.prefix}:" if self.prefix is not None else ""
        version = f"v{self.version}" if self.version is not None else ""
        return f"{prefix}{self.base_id}{version}"

    @classmethod
    def from_id(cls, article_id: str) -> 'ArticleId':
        """Parse arxiv identifier into detailed ArticleId.

        Args:
            article_id: String containing arxiv identifier (with or without version)

        Returns:
            ArticleId with parsed components for both new- and legacy-style identifiers.

        The format variants are documented in the official docs:
        https://info.arxiv.org/help/arxiv_identifier.html
        """
        s = article_id.strip()

        prefix = None
        if ":" in s:
            prefix, rest = s.split(":", 1)
            s = rest.strip()

        # Split optional version suffix from base identifier.
        # Examples:
        #   "1806.10215v4"        -> id="1806.10215", version="v4"
        #   "math.GT/0309136"     -> id="math.GT/0309136", version=None
        # The lazy quantifier (.+?) ensures that when a trailing "v<digits>" is present
        # it is captured by the version group rather than folded into the id.
        version_match = re.match(
            r"""
            ^                      # start of string
            (?P<id>.+?)            # base identifier, as short as possible
            (?P<version>           # optional version group
                v[0-9]+            # literal 'v' followed by one or more digits
            )?                     # version is optional
            $                      # end of string
            """,
            s,
            re.VERBOSE,
        )
        if not version_match:
            raise ValueError(f"Invalid arxiv identifier format: {article_id}")

        base_id = version_match.group("id")
        version_str = version_match.group("version")  # e.g. "v4" or None
        version = int(version_str[1:]) if version_str is not None else None

        if "/" in base_id:
            year, month, number, archive, subject = _parse_pre0704_identifier(base_id)
        else:
            year, month, number = _parse_post0704_identifier(base_id)
            archive = None
            subject = None

        return ArticleId(
            base_id=base_id,
            version=version,
            year=year,
            month=month,
            number=number,
            prefix=prefix,
            archive=archive,
            subject=subject,
        )

    def _reconstruct_id(self) -> str:
        """Rebuild full identifier from internal fields.
        This method is used mostly for testing.
        """
        if self.archive is None:
            base_id = self._reconstruct_post0704_base_id()
        else:
            base_id = self._reconstruct_pre0704_base_id()

        prefix = f"{self.prefix}:" if self.prefix is not None else ""
        version = f"v{self.version}" if self.version is not None else ""
        return f"{prefix}{base_id}{version}"

    def _reconstruct_post0704_base_id(self) -> str:
        """Rebuild YYMM.number for post-0704 identifiers.

        The number part is 4 digits up to 2014-12 inclusive (1412.NNNN), and
        5 digits from 2015-01 (1501.NNNNN) onward.
        """
        yy = self.year % 100
        mm = self.month

        # 4-digit sequence up to 2014-12 (1412), 5-digit afterwards.
        number_width = 4 if self.year < 2015 else 5
        number = f"{self.number:0{number_width}d}"
        return f"{yy:02d}{mm:02d}.{number}"

    def _reconstruct_pre0704_base_id(self) -> str:
        """Rebuild archive[.subject]/YYMMNNN for pre-0704 identifiers."""
        yy = self.year % 100
        mm = self.month
        number = f"{self.number:03d}"
        numeric = f"{yy:02d}{mm:02d}{number}"

        if self.subject is not None:
            category = f"{self.archive}.{self.subject}"
        else:
            category = self.archive

        return f"{category}/{numeric}"


def _parse_post0704_identifier(identifier: str):
    match = re.fullmatch(
        r"""
        ^                # start of string
        ([0-9]{4})       # YYMM: two-digit year + two-digit month
        \.               # literal dot between date part and sequence
        ([0-9]{4,5})     # sequence number within the month (4 or 5 digits)
        $                # end of string
        """,
        identifier,
        re.VERBOSE,
    )
    if not match:
        raise ValueError(f"Invalid new-style arxiv identifier: {identifier}")

    yymm, seq = match.groups()
    yy = int(yymm[:2])
    mm = int(yymm[2:4])
    if not 1 <= mm <= 12:
        raise ValueError(f"Invalid month in arxiv identifier: {identifier}")

    year = 2000 + yy
    number = int(seq)
    return year, mm, number


def _parse_pre0704_identifier(identifier: str):
    match = re.fullmatch(
        r"""
        ^                # start of string
        ([\w.-]+)        # archive or archive.subject (letters, digits, '_', '.', '-')
        /                # slash separating category from numeric part
        ([0-9]{7})       # YYMMNNN: year, month, and 3-digit sequence
        $                # end of string
        """,
        identifier,
        re.VERBOSE,
    )
    if not match:
        raise ValueError(f"Invalid legacy arxiv identifier: {identifier}")

    category, numeric = match.groups()
    yy = int(numeric[:2])
    mm = int(numeric[2:4])
    if not 1 <= mm <= 12:
        raise ValueError(f"Invalid month in arxiv identifier: {identifier}")

    if yy >= 90:
        year = 1900 + yy
    else:
        year = 2000 + yy

    number = int(numeric[4:])

    if "." in category:
        archive, subject = category.split(".", 1)
    else:
        archive = category
        subject = None

    return year, mm, number, archive, subject
