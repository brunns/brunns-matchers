from bs4 import BeautifulSoup
from hamcrest import equal_to, has_item, anything, contains, all_of
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.matcher import Matcher

ANYTHING = anything()


def has_title(title):
    return HtmlWithTag("title", TagWithString(title))


def has_tag(name, matcher):
    return HtmlWithTag(name, matcher)


def tag_has_string(matcher):
    return TagWithString(matcher)


def has_class(clazz):
    return TagWithClass(clazz)


def has_table(matcher, id_=ANYTHING):
    return HtmlHasTable(matcher, id_=id_)


def has_rows(matcher):
    return TableHasRows(matcher)


class HtmlWithTag(BaseMatcher):
    def __init__(self, name, matcher):
        self.name = name
        self.matcher = matcher if isinstance(matcher, Matcher) else tag_has_string(matcher)

    def _matches(self, actual):
        soup = BeautifulSoup(actual, "html.parser")
        found = soup.find_all(self.name)
        return has_item(self.matcher).matches(found)

    def describe_to(self, description):
        description.append_text("HTML with tag ").append_value(self.name).append_text(
            " matching "
        ).append_description_of(self.matcher)

    def describe_mismatch(self, actual, mismatch_description):
        mismatch_description.append_text("got HTML with tag ").append_value(self.name).append_text(" values ")
        soup = BeautifulSoup(actual, "html.parser")
        found = soup.find_all(self.name)
        mismatch_description.append_list("[", ", ", "]", [t for t in found])


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
        return has_item(self.matcher).matches(tag["class"])

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
        pass


class TableHasRows(BaseMatcher):
    def __init__(self, matcher):
        self.matcher = matcher

    def _matches(self, table):
        rows = table.find_all("tr")
        return has_item(self.matcher).matches(row.find_all("td") for row in rows)

    def describe_to(self, description):
        pass
