import re
import warnings
from typing import List, Protocol, Union, Tuple


# noinspection SpellCheckingInspection
class Stringable(Protocol):
    def __str__(self) -> str: ...


FieldValue = Union[Stringable, List[Stringable], Tuple[Stringable, ...]]


class Query:
    """
    https://info.arxiv.org/help/api/user-manual.html#query_details

    Available field prefixes with explanations:
    ti     Title
    au     Author
    abs    Abstract
    co     Comment
    jr     Journal Reference
    cat    Subject Category
    rn     Report Number
    id     Id (use id_list instead)
    all    All of the above

    Possible Boolean operators:
    AND
    OR
    ANDNOT

    Special symbol encodings:
    ( )            %28 %29    Used to group Boolean expressions for Boolean operator precedence.
    double quotes  %22 %22    Used to group multiple words into phrases to search a particular field.
    space          +          Used to extend a search_query to include multiple fields.

    """

    def __init__(self, content: str, negated=False):
        self.negated = negated
        self.content = content

    def __and__(self, other: Union[str, "Query"]):
        self._validate_negation()
        if isinstance(other, str):
            other = Query.all(other)
        if other.negated:
            operator = "ANDNOT"
        else:
            operator = "AND"
        return Query(f"({self.content} {operator} {other.content})")

    def __or__(self, other: Union[str, "Query"]):
        self._validate_negation()
        if isinstance(other, str):
            other = Query.all(other)
        if other.negated:
            raise ValueError("There is no ORNOT operator in the arXiv API")
        return Query(f"({self.content} OR {other.content})")

    def __rand__(self, other: Union[str, "Query"]):
        if isinstance(other, str):
            return Query.all(other) & self
        return NotImplemented

    def __ror__(self, other: Union[str, "Query"]):
        if isinstance(other, str):
            return Query.all(other) | self
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
            raise ValueError(
                "There is no standalone negation operator, only combined ANDNOT"
            )

    @staticmethod
    def _validate_term(term: Stringable, quote):
        value = str(term)
        if re.search('[")(]', value):
            raise ValueError(
                "Double quotes and parentheses cause problems and are forbidden"
            )
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
            content = f"{prefix}:({" ".join(terms)})"
            return cls(content)

        if isinstance(value, tuple):
            # Combine items inside the field, i.e., "field:(i1 AND i2 AND i3 ...)"
            terms = [cls._validate_term(term, quote) for term in value]
            content = f"{prefix}:({" AND ".join(terms)})"
            return cls(content)

        term = cls._validate_term(value, quote)
        content = f"{prefix}:{term}"
        return cls(content)

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
