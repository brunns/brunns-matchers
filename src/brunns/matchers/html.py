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


def has_rows(matcher):
    return TableHasRows(matcher)


def has_header_row(matcher):
    return TableHasRows(matcher, header_row=True)


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
        mismatch_description.append_list(" values [", ", ", "]", [t for t in found])


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


class TableHasRows(BaseMatcher):
    def __init__(self, matcher, header_row=False):
        self.matcher = matcher
        self.header_row = header_row

    def _matches(self, table):
        rows = table.find_all("tr")
        return has_item(self.matcher).matches(row.find_all("th" if self.header_row else "td") for row in rows)

    def describe_to(self, description):
        description.append_text("table with {0}row matching ".format("header " if self.header_row else ""))
        self.matcher.describe_to(description)
