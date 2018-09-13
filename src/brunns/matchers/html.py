# encoding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import warnings

from bs4 import BeautifulSoup
from hamcrest import equal_to, has_item, anything, contains, all_of
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.matcher import Matcher

ANYTHING = anything()


def has_title(title):
    return HtmlWithTag(TagWithString(title), name="title")


def has_tag(name, matcher):
    """Ultimately replace this with a signature something like:
    has_tag(name=None, id_=None, matcher=anything())
    """
    warnings.warn("deprecated - use has_named_tag()", DeprecationWarning)
    return HtmlWithTag(matcher, name=name)


def has_named_tag(name, matcher):
    return HtmlWithTag(matcher, name=name)


def has_id_tag(id_, matcher):
    return HtmlWithTag(matcher, id_=id_)


def tag_has_string(matcher):
    return TagWithString(matcher)


def has_class(clazz):
    return TagWithClass(clazz)


def has_table(matcher, id_=ANYTHING):
    return HtmlHasTable(matcher, id_=id_)


def has_rows(cells_matcher):
    warnings.warn("deprecated - use has_row()", DeprecationWarning)
    return has_row(cells_match=cells_matcher)


def has_row(row_matches=ANYTHING, cells_match=ANYTHING, index_matches=ANYTHING, header_row=False):
    return TableHasRow(
        row_matcher=row_matches, cells_matcher=cells_match, index_matcher=index_matches, header_row=header_row
    )


def has_nth_row(index, cells_matcher=ANYTHING, row_matcher=ANYTHING):
    warnings.warn("deprecated - use has_row(index_matches=index)", DeprecationWarning)
    return has_row(row_matches=row_matcher, cells_match=cells_matcher, index_matches=index)


def has_header_row(cells_matcher=ANYTHING, row_matcher=ANYTHING):
    return has_row(cells_match=cells_matcher, row_matches=row_matcher, header_row=True)


class HtmlWithTag(BaseMatcher):
    def __init__(self, matcher, name=None, id_=None):
        self.name = name
        self.id_ = id_
        self.matcher = matcher if isinstance(matcher, Matcher) else tag_has_string(matcher)

    def _matches(self, actual):
        soup = BeautifulSoup(actual, "html.parser")
        found = soup.find_all(self.name, id=self.id_)
        return has_item(self.matcher).matches(found)

    def describe_to(self, description):
        description.append_text("HTML with tag")
        if self.name:
            description.append_text(" name=").append_value(self.name)
        if self.id_:
            description.append_text(" id=").append_value(self.id_)
        description.append_text(" matching ").append_description_of(self.matcher)

    def describe_mismatch(self, actual, mismatch_description):
        mismatch_description.append_text("got HTML with tag")
        if self.name:
            mismatch_description.append_text(" name=").append_value(self.name)
        if self.id_:
            mismatch_description.append_text(" id=").append_value(self.id_)
        soup = BeautifulSoup(actual, "html.parser")
        found = soup.find_all(self.name, id=self.id_)
        mismatch_description.append_list(" values [", ", ", "]", [repr(t) for t in found])


class TagWithString(BaseMatcher):
    def __init__(self, matcher):
        self.matcher = matcher if isinstance(matcher, Matcher) else equal_to(matcher)

    def _matches(self, tag):
        return self.matcher.matches(tag.string)

    def describe_to(self, description):
        description.append_text("tag with string matching ").append_description_of(self.matcher)


class TagWithClass(BaseMatcher):
    def __init__(self, matcher):
        self.matcher = matcher if isinstance(matcher, Matcher) else equal_to(matcher)

    def _matches(self, tag):
        return has_item(self.matcher).matches(tag.get("class", None))

    def describe_to(self, description):
        description.append_text("tag with class matching ").append_description_of(self.matcher)


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
        indexed_rows_and_cells = ((index, row, cells) for index, (row, cells) in enumerate(rows_and_cells))
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
