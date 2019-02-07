# encoding=utf-8
from bs4 import BeautifulSoup, Tag
from hamcrest import equal_to, has_item, anything, contains, all_of, has_entry
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.matcher import Matcher

ANYTHING = anything()


def has_title(title):
    return HtmlWithTag(TagWith(string=title), name="title")


def has_named_tag(name, matcher):
    return HtmlWithTag(matcher, name=name)


def has_id_tag(id_, matcher):
    return HtmlWithTag(matcher, id_=id_)


def tag_has_string(matcher):
    return TagWith(string=matcher)


def has_class(clazz):
    return TagWith(clazz=clazz)


def has_table(matcher, id_=ANYTHING):
    return HtmlHasTable(matcher, id_=id_)


def has_row(row_matches=ANYTHING, cells_match=ANYTHING, index_matches=ANYTHING, header_row=False):
    return TableHasRow(
        row_matcher=row_matches, cells_matcher=cells_match, index_matcher=index_matches, header_row=header_row
    )


def has_header_row(cells_matcher=ANYTHING, row_matcher=ANYTHING):
    return has_row(cells_match=cells_matcher, row_matches=row_matcher, header_row=True)


def has_id(id_):
    return TagWith(attributes=has_entry("id", id_))


def has_attributes(matcher):
    return TagWith(attributes=matcher)


def has_link(id_=ANYTHING, clazz=ANYTHING, href=ANYTHING):
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


class HtmlWithTag(BaseMatcher):
    def __init__(self, matcher, name=None, id_=None):
        self.name = name
        self.id_ = id_
        self.matcher = matcher if isinstance(matcher, Matcher) else tag_has_string(matcher)

    def _matches(self, actual):
        found = self.findall(actual)
        return has_item(self.matcher).matches(found)

    def findall(self, actual):
        soup = actual if isinstance(actual, Tag) else BeautifulSoup(actual, "html.parser")
        found = soup.find_all(self.name, id=self.id_) if self.id_ else soup.find_all(self.name)
        return found

    def describe_to(self, description):
        description.append_text("HTML with tag")
        if self.name:
            description.append_text(" name=").append_description_of(self.name)
        if self.id_:
            description.append_text(" id=").append_description_of(self.id_)
        description.append_text(" matching ").append_description_of(self.matcher)

    def describe_mismatch(self, actual, mismatch_description):
        mismatch_description.append_text("got HTML with tag")
        if self.name:
            mismatch_description.append_text(" name=").append_description_of(self.name)
        if self.id_:
            mismatch_description.append_text(" id=").append_description_of(self.id_)
        found = self.findall(actual)
        mismatch_description.append_list(" values [", ", ", "]", [repr(t) for t in found])


class TagWith(BaseMatcher):
    def __init__(self, name=ANYTHING, string=ANYTHING, clazz=ANYTHING, attributes=ANYTHING):
        self.name = name if isinstance(name, Matcher) else equal_to(name)
        self.string = string if isinstance(string, Matcher) else equal_to(string)
        self.clazz = clazz if isinstance(clazz, Matcher) else equal_to(clazz)
        self.attributes = attributes if isinstance(attributes, Matcher) else equal_to(attributes)

    def _matches(self, tag):
        return (
            self.name.matches(tag.name)
            and self.string.matches(tag.string)
            and (self.clazz == ANYTHING or has_item(self.clazz).matches(tag.get("class", None)))
            and self.attributes.matches(tag.attrs)
        )

    def describe_to(self, description):
        description.append_text("tag with")
        if self.name != ANYTHING:
            description.append_text(" name matching ").append_description_of(self.name)
        if self.string != ANYTHING:
            description.append_text(" string matching ").append_description_of(self.string)
        if self.clazz != ANYTHING:
            description.append_text(" class matching ").append_description_of(self.clazz)
        if self.attributes != ANYTHING:
            description.append_text(" attributes matching ").append_description_of(self.attributes)


class HtmlHasTable(BaseMatcher):
    def __init__(self, matcher, id_=ANYTHING):
        self.matcher = matcher
        self.id_ = id_

    def _matches(self, html):
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.find_all("table")
        return contains(all_of(self.id_, self.matcher)).matches(tables)

    def describe_to(self, description):
        description.append_text("row matching ")
        self.matcher.describe_to(description)


class TableHasRow(BaseMatcher):
    def __init__(self, row_matcher=ANYTHING, cells_matcher=ANYTHING, header_row=False, index_matcher=ANYTHING):
        self.row_matcher = row_matcher
        self.cells_matcher = cells_matcher
        self.header_row = header_row
        self.index_matcher = index_matcher if isinstance(index_matcher, Matcher) else equal_to(index_matcher)

    def _matches(self, table):
        rows = table.find_all("tr")
        rows_and_cells = ((row, self._row_cells(row)) for row in rows if self._row_cells(row))
        indexed_rows_and_cells = [(index, row, cells) for index, (row, cells) in enumerate(rows_and_cells)]
        indexed_row_matcher = contains(self.index_matcher, self.row_matcher, self.cells_matcher)
        return has_item(indexed_row_matcher).matches(indexed_rows_and_cells)

    def _row_cells(self, row):
        return row.find_all("th" if self.header_row else "td")

    def describe_to(self, description):
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

    def describe_mismatch(self, table, mismatch_description):
        super(TableHasRow, self).describe_mismatch(table, mismatch_description)
        mismatch_description.append_text("\n\nfound rows:\n").append_list("", "\n", "", table.find_all("tr"))
