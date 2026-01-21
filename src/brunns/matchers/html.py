from collections.abc import Mapping, Sequence
from typing import Any, Optional, Union, cast

from bs4 import BeautifulSoup, Tag  # type: ignore[attr-defined]
from hamcrest import all_of, anything, contains_exactly, has_entry, has_item
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

ANYTHING = anything()
ATTR_MATCHER = Union[Matcher[Mapping[str, Union[str, Matcher[str]]]], Mapping[str, Union[str, Matcher[str]]]]


class HtmlWithTag(BaseMatcher[str]):
    def __init__(
        self,
        tag_matcher: Union[str, Matcher[Tag]],
        name: Optional[str] = None,
        id_: Optional[str] = None,
    ) -> None:
        self.name = name
        self.id_ = id_
        self.tag_matcher: Matcher[Tag] = (
            tag_matcher if isinstance(tag_matcher, Matcher) else tag_has_string(cast("str", tag_matcher))
        )

    def _matches(self, actual: str) -> bool:
        found_tags: Sequence[Tag] = self.findall(actual)
        return cast("Matcher[Sequence[Tag]]", has_item(self.tag_matcher)).matches(found_tags)

    def findall(self, actual: str) -> Sequence[Tag]:
        soup = actual if isinstance(actual, Tag) else BeautifulSoup(actual, "html.parser")
        return soup.find_all(self.name, id=self.id_) if self.id_ else soup.find_all(self.name)

    def describe_to(self, description: Description) -> None:
        description.append_text("HTML with tag")
        if self.name:
            description.append_text(" name=").append_description_of(self.name)
        if self.id_:
            description.append_text(" id=").append_description_of(self.id_)
        description.append_text(" matching ").append_description_of(self.tag_matcher)

    def describe_mismatch(self, actual, mismatch_description: Description) -> None:
        mismatch_description.append_text("got HTML with tag")
        if self.name:
            mismatch_description.append_text(" name=").append_description_of(self.name)
        if self.id_:
            mismatch_description.append_text(" id=").append_description_of(self.id_)
        found = self.findall(actual)
        mismatch_description.append_list(" values [", ", ", "]", [repr(t) for t in found])


class TagWith(BaseMatcher[Tag]):
    def __init__(
        self,
        name: Union[str, Matcher[str]] = ANYTHING,
        string: Union[str, Matcher[str]] = ANYTHING,
        clazz: Union[str, Matcher[str]] = ANYTHING,
        attributes: Union[
            Mapping[str, Union[str, Matcher[str]]],
            Matcher[Mapping[str, Union[str, Matcher[str]]]],
        ] = ANYTHING,
    ) -> None:
        self.name: Matcher[str] = wrap_matcher(name)
        self.string: Matcher[str] = wrap_matcher(string)
        self.clazz: Matcher[str] = wrap_matcher(clazz)
        self.attributes: Matcher[Mapping[str, Union[str, Matcher[str]]]] = wrap_matcher(attributes)

    def _matches(self, tag: Tag) -> bool:
        # TODO - remove type ignore when https://github.com/python/mypy/issues/3283 is resolved.
        return (
            self.name.matches(tag.name)
            and self.string.matches(tag.string or "")
            and (self.clazz == ANYTHING or has_item(self.clazz).matches(tag.get("class", [])))  # type: ignore[arg-type]
            and self.attributes.matches(cast("Mapping[str, Any]", tag.attrs))
        )

    def describe_to(self, description: Description) -> None:
        description.append_text("tag with")
        if self.name != ANYTHING:
            description.append_text(" name matching ").append_description_of(self.name)
        if self.string != ANYTHING:
            description.append_text(" string matching ").append_description_of(self.string)
        if self.clazz != ANYTHING:
            description.append_text(" class matching ").append_description_of(self.clazz)
        if self.attributes != ANYTHING:
            description.append_text(" attributes matching ").append_description_of(self.attributes)


class HtmlHasTable(BaseMatcher[str]):
    def __init__(self, table_matcher: Matcher[Tag], id_: Union[str, Matcher[str]] = ANYTHING) -> None:
        self.table_matcher = table_matcher
        self.id_: Matcher[str] = wrap_matcher(id_)

    def _matches(self, html: str) -> bool:
        # TODO - remove type ignore when https://github.com/python/mypy/issues/3283 is resolved.
        tables = BeautifulSoup(html, "html.parser").find_all("table")
        return contains_exactly(all_of(self.id_, self.table_matcher)).matches(tables)  # type: ignore[arg-type]

    def describe_to(self, description: Description) -> None:
        description.append_text("row matching ")
        self.table_matcher.describe_to(description)


class TableHasRow(BaseMatcher[Tag]):
    def __init__(
        self,
        row_matcher: Matcher[Tag] = ANYTHING,
        cells_matcher: Matcher[Sequence[Tag]] = ANYTHING,
        index_matcher: Union[int, Matcher[int]] = ANYTHING,
        *,
        header_row: bool = False,
    ) -> None:
        self.row_matcher = row_matcher
        self.cells_matcher = cells_matcher
        self.header_row = header_row
        self.index_matcher: Matcher[int] = wrap_matcher(index_matcher)

    def _matches(self, table: Tag) -> bool:
        # TODO - remove type ignore when https://github.com/python/mypy/issues/3283 is resolved.
        rows: Sequence[Tag] = table.find_all("tr")
        rows_and_cells = [(row, self._row_cells(row)) for row in rows if self._row_cells(row)]
        indexed_rows_and_cells = [(index, row, cells) for index, (row, cells) in enumerate(rows_and_cells)]
        indexed_row_matcher = cast(
            "Matcher[tuple[int, Tag, Sequence[Tag]]]",
            contains_exactly(self.index_matcher, self.row_matcher, self.cells_matcher),
        )
        return has_item(indexed_row_matcher).matches(indexed_rows_and_cells)  # type: ignore[arg-type]

    def _row_cells(self, row: Tag) -> Sequence[Tag]:
        return row.find_all("th" if self.header_row else "td")

    def describe_to(self, description: Description) -> None:
        description.append_text(f"table with {'header ' if self.header_row else ''}row")
        if self.cells_matcher != ANYTHING:
            description.append_text(" cells matching ")
            self.cells_matcher.describe_to(description)
        if self.row_matcher != ANYTHING:
            description.append_text(" row matching ")
            self.row_matcher.describe_to(description)
        if self.index_matcher != ANYTHING:
            description.append_text(" index matching ")
            self.index_matcher.describe_to(description)

    def describe_mismatch(self, table: Tag, mismatch_description: Description) -> None:
        super().describe_mismatch(table, mismatch_description)
        mismatch_description.append_text("\n\nfound rows:\n").append_list("", "\n", "", table.find_all("tr"))


def has_title(title: Union[str, Matcher[str]]) -> HtmlWithTag:
    """TODO"""
    return HtmlWithTag(TagWith(string=title), name="title")


def has_named_tag(name, matcher) -> HtmlWithTag:
    """TODO"""
    return HtmlWithTag(matcher, name=name)


def has_id_tag(id_, matcher) -> HtmlWithTag:
    """TODO"""
    return HtmlWithTag(matcher, id_=id_)


def tag_has_string(matcher: Union[str, Matcher[str]]) -> TagWith:
    """TODO"""
    return TagWith(string=matcher)


def has_class(clazz: Union[str, Matcher[str]]) -> TagWith:
    """TODO"""
    return TagWith(clazz=clazz)


def has_table(matcher, id_=ANYTHING) -> HtmlHasTable:
    """TODO"""
    return HtmlHasTable(matcher, id_=id_)


def has_row(row_matches=ANYTHING, cells_match=ANYTHING, index_matches=ANYTHING, *, header_row=False) -> TableHasRow:
    return TableHasRow(
        row_matcher=row_matches,
        cells_matcher=cells_match,
        index_matcher=index_matches,
        header_row=header_row,
    )


def has_header_row(cells_matcher=ANYTHING, row_matcher=ANYTHING) -> TableHasRow:
    return has_row(cells_match=cells_matcher, row_matches=row_matcher, header_row=True)


def has_id(id_: Union[str, Matcher[str]]) -> TagWith:
    return TagWith(attributes=has_entry("id", id_))


def has_attributes(
    matcher: Union[Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]],
) -> TagWith:
    return TagWith(attributes=matcher)


def has_link(
    id_: Union[str, Matcher[str]] = ANYTHING,
    clazz: Union[str, Matcher[str]] = ANYTHING,
    href: Union[str, Matcher[str]] = ANYTHING,
) -> HtmlWithTag:
    href_matcher: ATTR_MATCHER = has_entry("href", href) if href != ANYTHING else ANYTHING
    id_matcher: ATTR_MATCHER = has_entry("id", id_) if id_ != ANYTHING else ANYTHING
    return HtmlWithTag(TagWith(name="a", clazz=clazz, attributes=all_of(href_matcher, id_matcher)))


def has_image(
    id_: Union[str, Matcher[str]] = ANYTHING,
    clazz: Union[str, Matcher[str]] = ANYTHING,
    src: Union[str, Matcher[str]] = ANYTHING,
) -> HtmlWithTag:
    src_matcher: ATTR_MATCHER = has_entry("src", src) if src != ANYTHING else ANYTHING
    id_matcher: ATTR_MATCHER = has_entry("id", id_) if id_ != ANYTHING else ANYTHING
    return HtmlWithTag(TagWith(name="img", clazz=clazz, attributes=all_of(src_matcher, id_matcher)))
