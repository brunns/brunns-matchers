from bs4 import BeautifulSoup
from hamcrest import equal_to, has_item
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.matcher import Matcher


class HtmlWithTag(BaseMatcher):
    def __init__(self, name, matcher):
        self.name = name
        self.matcher = matcher if isinstance(matcher, Matcher) else equal_to(matcher)

    def _matches(self, html):
        soup = BeautifulSoup(html, "html.parser")
        found = soup.find_all(self.name)
        return has_item(self.matcher).matches(found)

    def describe_to(self, description):
        description.append_text("HTML with tag ").append_value(self.name).append_text(
            " matching "
        ).append_description_of(self.matcher)

    def describe_mismatch(self, html, mismatch_description):
        mismatch_description.append_text("got HTML with tag ").append_value(self.name)
        soup = BeautifulSoup(html, "html.parser")
        found = soup.find_all(self.name)
        has_item(self.matcher).describe_mismatch(found, mismatch_description)


class TagWithString(BaseMatcher):
    def _matches(self, tag):
        return self.matcher.matches(tag.string)

    def __init__(self, matcher):
        self.matcher = matcher if isinstance(matcher, Matcher) else equal_to(matcher)

    def describe_to(self, description):
        description.append_text("tag matching ").append_description_of(self.matcher)


def has_title(title):
    return HtmlWithTag("title", TagWithString(title))
