# encoding=utf-8
from typing import Mapping, Optional, Sequence, Tuple, Union, cast

from bs4 import BeautifulSoup, Tag  # type: ignore
from hamcrest import all_of, anything, contains_exactly, has_entry, has_item
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

ANYTHING = anything()


class HtmlWithTag(BaseMatcher[str]):
    def __init__(
        self,
        tag_matcher: Union[str, Matcher[Tag]],
        name: Optional[str] = None,
        id_: Optional[str] = None,
    ) -> None:
        self.name = name
        self.id_ = id_
        self.tag_matcher = (
            tag_matcher
            if isinstance(tag_matcher, Matcher)
            else tag_has_string(cast(str, tag_matcher))
        )  # type: Matcher[Tag]

    def _matches(self, actual: str) -> bool:
        found_tags = self.findall(actual)  # type: Sequence[Tag]
        return has_item(self.tag_matcher).matches(found_tags)

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
            Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
        ] = ANYTHING,
    ) -> None:
        self.name = wrap_matcher(name)  # type: Matcher[str]
        self.string = wrap_matcher(string)  # type: Matcher[str]
        self.clazz = wrap_matcher(clazz)  # type: Matcher[str]
        self.attributes = wrap_matcher(
            attributes
        )  # type: Matcher[Mapping[str, Union[str, Matcher[str]]]]

    def _matches(self, tag: Tag) -> bool:
        # TODO - remove type ignore when https://github.com/python/mypy/issues/3283 is resolved.
        return (
            self.name.matches(tag.name)
            and self.string.matches(tag.string)
            and (self.clazz == ANYTHING or has_item(self.clazz).matches(tag.get("class", [])))  # type: ignore
            and self.attributes.matches(tag.attrs)
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
    def __init__(
        self, table_matcher: Matcher[Tag], id_: Union[str, Matcher[str]] = ANYTHING
    ) -> None:
        self.table_matcher = table_matcher
        self.id_ = wrap_matcher(id_)  # type: Matcher[str]

    def _matches(self, html: str) -> bool:
        # TODO - remove type ignore when https://github.com/python/mypy/issues/3283 is resolved.
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        return contains_exactly(all_of(self.id_, self.table_matcher)).matches(tables)  # type: ignore

    def describe_to(self, description: Description) -> None:
        description.append_text("row matching ")
        self.table_matcher.describe_to(description)


class TableHasRow(BaseMatcher[Tag]):
    def __init__(
        self,
        row_matcher: Matcher[Tag] = ANYTHING,
        cells_matcher: Matcher[Sequence[Tag]] = ANYTHING,
        header_row: bool = False,
        index_matcher: Union[int, Matcher[int]] = ANYTHING,
    ) -> None:
        self.row_matcher = row_matcher
        self.cells_matcher = cells_matcher
        self.header_row = header_row
        self.index_matcher = wrap_matcher(index_matcher)  # type: Matcher[int]

    def _matches(self, table: Tag) -> bool:
        # TODO - remove type ignore when https://github.com/python/mypy/issues/3283 is resolved.
        rows = table.find_all("tr")  # type: Sequence[Tag]
        rows_and_cells = [(row, self._row_cells(row)) for row in rows if self._row_cells(row)]
        indexed_rows_and_cells = [
            (index, row, cells) for index, (row, cells) in enumerate(rows_and_cells)
        ]
        indexed_row_matcher = cast(
            Matcher[Tuple[int, Tag, Sequence[Tag]]],
            contains_exactly(self.index_matcher, self.row_matcher, self.cells_matcher),
        )
        return has_item(indexed_row_matcher).matches(indexed_rows_and_cells)  # type: ignore

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
        super(TableHasRow, self).describe_mismatch(table, mismatch_description)
        mismatch_description.append_text("\n\nfound rows:\n").append_list(
            "", "\n", "", table.find_all("tr")
        )


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


def has_row(
    row_matches=ANYTHING, cells_match=ANYTHING, index_matches=ANYTHING, header_row=False
) -> TableHasRow:
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
    matcher: Union[
        Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
    ]
) -> TagWith:
    return TagWith(attributes=matcher)


def has_link(
    id_: Union[str, Matcher[str]] = ANYTHING,
    clazz: Union[str, Matcher[str]] = ANYTHING,
    href: Union[str, Matcher[str]] = ANYTHING,
) -> HtmlWithTag:
    href_matcher = has_entry("href", href) if href != ANYTHING else ANYTHING
    id_matcher = has_entry("id", id_) if id_ != ANYTHING else ANYTHING
    return HtmlWithTag(TagWith(name="a", clazz=clazz, attributes=all_of(href_matcher, id_matcher)))
