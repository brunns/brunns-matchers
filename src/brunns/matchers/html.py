# encoding=utf-8
from typing import Iterable, Union

from brunns.matchers.base import GenericMatcher
from bs4 import BeautifulSoup, Tag
from hamcrest import all_of, anything, contains, has_entry, has_item
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

ANYTHING = anything()


class HtmlWithTag(GenericMatcher[str]):
    def __init__(self, matcher: Union[str, Matcher], name: str = None, id_: str = None) -> None:
        self.name = name
        self.id_ = id_
        self.matcher = matcher if isinstance(matcher, Matcher) else tag_has_string(matcher)

    def _matches(self, actual: str) -> bool:
        found = self.findall(actual)
        return has_item(self.matcher).matches(found)

    def findall(self, actual: str) -> Iterable[Tag]:
        soup = actual if isinstance(actual, Tag) else BeautifulSoup(actual, "html.parser")
        return soup.find_all(self.name, id=self.id_) if self.id_ else soup.find_all(self.name)

    def describe_to(self, description: Description) -> None:
        description.append_text("HTML with tag")
        if self.name:
            description.append_text(" name=").append_description_of(self.name)
        if self.id_:
            description.append_text(" id=").append_description_of(self.id_)
        description.append_text(" matching ").append_description_of(self.matcher)

    def describe_mismatch(self, actual, mismatch_description: Description) -> None:
        mismatch_description.append_text("got HTML with tag")
        if self.name:
            mismatch_description.append_text(" name=").append_description_of(self.name)
        if self.id_:
            mismatch_description.append_text(" id=").append_description_of(self.id_)
        found = self.findall(actual)
        mismatch_description.append_list(" values [", ", ", "]", [repr(t) for t in found])


class TagWith(GenericMatcher[Tag]):
    def __init__(
        self,
        name: Union[str, Matcher] = ANYTHING,
        string: Union[str, Matcher] = ANYTHING,
        clazz: Union[str, Matcher] = ANYTHING,
        attributes: Union[str, Matcher] = ANYTHING,
    ) -> None:
        self.name = wrap_matcher(name)
        self.string = wrap_matcher(string)
        self.clazz = wrap_matcher(clazz)
        self.attributes = wrap_matcher(attributes)

    def _matches(self, tag: Tag) -> bool:
        return (
            self.name.matches(tag.name)
            and self.string.matches(tag.string)
            and (self.clazz == ANYTHING or has_item(self.clazz).matches(tag.get("class", None)))
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


class HtmlHasTable(GenericMatcher[str]):
    def __init__(self, matcher: Matcher, id_: Union[str, Matcher] = ANYTHING) -> None:
        self.matcher = matcher
        self.id_ = id_

    def _matches(self, html: str) -> bool:
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        return contains(all_of(self.id_, self.matcher)).matches(tables)

    def describe_to(self, description: Description) -> None:
        description.append_text("row matching ")
        self.matcher.describe_to(description)


class TableHasRow(GenericMatcher[Tag]):
    def __init__(
        self,
        row_matcher: Matcher = ANYTHING,
        cells_matcher: Matcher = ANYTHING,
        header_row: bool = False,
        index_matcher: Union[int, Matcher] = ANYTHING,
    ) -> None:
        self.row_matcher = row_matcher
        self.cells_matcher = cells_matcher
        self.header_row = header_row
        self.index_matcher = wrap_matcher(index_matcher)

    def _matches(self, table: Tag) -> bool:
        rows = table.find_all("tr")
        rows_and_cells = ((row, self._row_cells(row)) for row in rows if self._row_cells(row))
        indexed_rows_and_cells = [
            (index, row, cells) for index, (row, cells) in enumerate(rows_and_cells)
        ]
        indexed_row_matcher = contains(self.index_matcher, self.row_matcher, self.cells_matcher)
        return has_item(indexed_row_matcher).matches(indexed_rows_and_cells)

    def _row_cells(self, row: Tag) -> Iterable[Tag]:
        return row.find_all("th" if self.header_row else "td")

    def describe_to(self, description: Description) -> None:
        description.append_text("table with {0}row".format("header " if self.header_row else ""))
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


def has_title(title: str) -> HtmlWithTag:
    """TODO"""
    return HtmlWithTag(TagWith(string=title), name="title")


def has_named_tag(name, matcher) -> HtmlWithTag:
    """TODO"""
    return HtmlWithTag(matcher, name=name)


def has_id_tag(id_, matcher) -> HtmlWithTag:
    """TODO"""
    return HtmlWithTag(matcher, id_=id_)


def tag_has_string(matcher) -> TagWith:
    """TODO"""
    return TagWith(string=matcher)


def has_class(clazz) -> TagWith:
    """TODO"""
    return TagWith(clazz=clazz)


def has_table(matcher, id_=ANYTHING) -> HtmlHasTable:
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


def has_id(id_) -> TagWith:
    return TagWith(attributes=has_entry("id", id_))


def has_attributes(matcher) -> TagWith:
    return TagWith(attributes=matcher)


def has_link(id_=ANYTHING, clazz=ANYTHING, href=ANYTHING) -> HtmlWithTag:
    return HtmlWithTag(
        TagWith(
            name="a",
            clazz=clazz,
            attributes=all_of(
                has_entry("href", href) if href != ANYTHING else ANYTHING,
                has_entry("id", id_) if id_ != ANYTHING else ANYTHING,
            ),
        )
    )
