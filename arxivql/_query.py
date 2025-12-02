import re
import warnings
from datetime import datetime, date, timezone
from typing import List, Protocol, Union, Tuple


# noinspection SpellCheckingInspection
class Stringable(Protocol):
    def __str__(self) -> str: ...


FieldValue = Union[Stringable, List[Stringable], Tuple[Stringable, ...]]


class Query:
    """
    https://info.arxiv.org/help/api/user-manual.html#query_details

    Available field prefixes with explanations:
    ti             Title
    au             Author
    abs            Abstract
    co             Comment
    jr             Journal Reference
    cat            Subject Category
    rn             Report Number
    id             Id (use id_list instead)
    all            All of the above
    submittedDate  Submission date range in format [YYYYMMDDTTTT TO YYYYMMDDTTTT]

    Possible Boolean operators:
    AND
    OR
    ANDNOT

    Special symbol encodings:
    ( )            %28 %29    Used to group Boolean expressions for Boolean operator precedence.
    double quotes  %22 %22    Used to group multiple words into phrases to search a particular field.
    space          +          Used to extend a search_query to include multiple fields.

    """

    def __init__(self, content: str, negated: bool = False):
        self.negated = negated
        self.content = content

    def __and__(self, other: Union[str, "Query"]):
        self._validate_negation()
        if isinstance(other, str):
            other = Query.from_raw_string(other)
        if other.negated:
            operator = "ANDNOT"
        else:
            operator = "AND"
        return Query(f"({self.content} {operator} {other.content})")

    def __or__(self, other: Union[str, "Query"]):
        self._validate_negation()
        if isinstance(other, str):
            other = Query.from_raw_string(other)
        if other.negated:
            raise ValueError("There is no ORNOT operator in the arXiv API")
        return Query(f"({self.content} OR {other.content})")

    def __rand__(self, other: Union[str]):
        if isinstance(other, str):
            return Query.from_raw_string(other) & self
        return NotImplemented

    def __ror__(self, other: Union[str]):
        if isinstance(other, str):
            return Query.from_raw_string(other) | self
        return NotImplemented

    def __invert__(self):
        return Query(self.content, not self.negated)

    def __str__(self):
        return self.to_string()

    def to_string(self) -> str:
        self._validate_negation()
        return self.content

    def _validate_negation(self):
        if self.negated:
            raise ValueError("There is no standalone negation operator in the arXiv API, only combined ANDNOT")

    @staticmethod
    def _validate_term(term: Stringable, quote):
        value = str(term)
        if re.search('[")(]', value):
            raise ValueError("Double quotes and parentheses cause problems and are forbidden")
        if len(value.split()) > 1:
            if quote:
                # Quote multi-term value.
                value = f'"{value}"'
            else:
                raise ValueError("Unquotable multi-term value")
        return value

    @classmethod
    def from_field(cls, value: FieldValue, prefix="all", quote=True) -> "Query":
        if isinstance(value, list):
            # Combine items inside the field, i.e., "field:(i1 i2 i3 ...)"
            terms = [cls._validate_term(term, quote) for term in value]
            joined = " ".join(terms)
            content = f"{prefix}:({joined})"
            return cls(content)

        if isinstance(value, tuple):
            # Combine items inside the field, i.e., "field:(i1 AND i2 AND i3 ...)"
            terms = [cls._validate_term(term, quote) for term in value]
            joined = " AND ".join(terms)
            content = f"{prefix}:({joined})"
            return cls(content)

        term = cls._validate_term(value, quote)
        content = f"{prefix}:{term}"
        return cls(content)

    @classmethod
    def from_raw_string(cls, raw: str) -> "Query":
        """Construct a Query from a raw string."""
        return cls(f"({raw})")

    @classmethod
    def category(cls, category: FieldValue):
        return cls.from_field(category, prefix="cat", quote=False)

    @classmethod
    def title(cls, value: FieldValue):
        return cls.from_field(value, prefix="ti")

    @classmethod
    def author(cls, value: FieldValue):
        return cls.from_field(value, prefix="au")

    @classmethod
    def abstract(cls, value: FieldValue):
        return cls.from_field(value, prefix="abs")

    @classmethod
    def comment(cls, value: FieldValue):
        return cls.from_field(value, prefix="co")

    @classmethod
    def journal(cls, value: FieldValue):
        return cls.from_field(value, prefix="jr")

    @classmethod
    def report(cls, value: FieldValue):
        return cls.from_field(value, prefix="rn")

    @classmethod
    def id(cls, value: FieldValue):
        warnings.warn("deprecation warning: use id_list in query instead")
        return cls.from_field(value, prefix="id")

    @classmethod
    def all(cls, value: FieldValue):
        return cls.from_field(value, prefix="all")

    @classmethod
    def submitted_date(
            cls,
            start: Union[datetime, date, str, None] = None,
            end: Union[datetime, date, str, None] = None,
    ) -> "Query":
        """
        Filter by submission date range (times in GMT).

        Args:
            start: Range start.
            end: Range end.

        Acceptable types:
          - datetime
          - date
          - timestamp string in arXiv format (see below)
          - None for open-ended ranges

        Timezone-aware datetimes are converted to UTC.

        The official arXiv datetime format for submittedDate filtering is YYYYMMDDHHMM.
        See https://info.arxiv.org/help/api/user-manual.html#query_details
        But in practice arXiv accepts shorter (partial) formats, and the ones that include seconds.

        Seconds are ignored by the search engine.
        """

        def format_date(d: Union[datetime, date, str]) -> str:
            if isinstance(d, datetime):
                if d.tzinfo is not None:
                    d = d.astimezone(timezone.utc)
                return d.strftime("%Y%m%d%H%M")
            elif isinstance(d, date):
                return d.strftime("%Y%m%d") + "0000"
            if isinstance(d, str):
                return _validate_arxiv_datetime_string(d)
            else:
                raise ValueError("submitted_date only accepts datetime, date, str, or None")

        start_str = format_date(start) if start is not None else "100001010000"
        end_str = format_date(end) if end is not None else "900001010000"
        return cls(f"submittedDate:[{start_str} TO {end_str}]")


def _validate_arxiv_datetime_string(d: str) -> str:
    if not re.fullmatch(r"[0-9]{4,14}", d):
        raise ValueError("submitted_date string must be a digit-only timestamp with 4 to 14 digits")

    length = len(d)
    # Choose appropriate format string based on length range and let
    # datetime.strptime handle the actual parsing. This validates that the
    # string represents a real date/time without changing its value.
    if length <= 4:  # YYYY or YYYY+
        fmt = "%Y"
    elif length <= 6:  # up to YYYYMM
        fmt = "%Y%m"
    elif length <= 8:  # up to YYYYMMDD
        fmt = "%Y%m%d"
    elif length <= 10:  # up to YYYYMMDDHH
        fmt = "%Y%m%d%H"
    elif length <= 12:  # up to YYYYMMDDHHMM
        fmt = "%Y%m%d%H%M"
    else:  # up to YYYYMMDDHHMMSS
        fmt = "%Y%m%d%H%M%S"

    try:
        datetime.strptime(d, fmt)
    except ValueError:
        raise ValueError("submitted_date string is not a valid datetime")
    return d
