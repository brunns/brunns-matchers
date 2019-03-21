# encoding=utf-8
import logging
from typing import Mapping, Union

from brunns.matchers.base import GenericMatcher
from furl import furl
from hamcrest import anything
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

logger = logging.getLogger(__name__)
ANYTHING = anything()


def to_host(matcher: Union[str, Matcher]):
    """TODO"""
    return UrlWith(host=matcher)


def with_path(matcher: Union[str, Matcher]):
    """TODO"""
    return UrlWith(path=matcher)


def with_query(matcher: Union[Mapping[str, str], Matcher]):
    """TODO"""
    return UrlWith(query=matcher)


def with_fragment(matcher: Union[str, Matcher]):
    """TODO"""
    return UrlWith(fragment=matcher)


class UrlWith(GenericMatcher[Union[furl, str]]):
    def __init__(
        self,
        host: Union[str, Matcher] = ANYTHING,
        path: Union[str, Matcher] = ANYTHING,
        query: Union[Mapping[str, str], Matcher] = ANYTHING,
        fragment: Union[str, Matcher] = ANYTHING,
    ) -> None:
        super(UrlWith, self).__init__()
        self.host = wrap_matcher(host)
        self.path = wrap_matcher(path)
        self.query = wrap_matcher(query)
        self.fragment = wrap_matcher(fragment)

    def _matches(self, url: Union[furl, str]) -> bool:
        url = url if isinstance(url, furl) else furl(url)
        return (
            self.host.matches(url.host)
            and self.path.matches(url.path)
            and self.query.matches(url.query.params)
            and self.fragment.matches(url.fragment)
        )

    def describe_to(self, description: Description) -> None:
        description.append_text("URL with")
        if self.host != ANYTHING:
            description.append_text(" host ").append_description_of(self.host)
        if self.path != ANYTHING:
            description.append_text(" path ").append_description_of(self.path)
        if self.query != ANYTHING:
            description.append_text(" query ").append_description_of(self.query)
        if self.fragment != ANYTHING:
            description.append_text(" fragment ").append_description_of(self.fragment)

    def describe_mismatch(self, url: Union[furl, str], mismatch_description: Description) -> None:
        url = url if isinstance(url, furl) else furl(url)
        if self.host != ANYTHING and not self.host.matches(url.host):
            mismatch_description.append_text("host ")
            self.host.describe_mismatch(url.host, mismatch_description)
        if self.path != ANYTHING and not self.path.matches(url.path):
            mismatch_description.append_text("path ")
            self.host.describe_mismatch(url.path, mismatch_description)
        if self.query != ANYTHING and not self.query.matches(url.query.params):
            mismatch_description.append_text("query ")
            self.query.describe_mismatch(url.query.params, mismatch_description)
        if self.fragment != ANYTHING and not self.fragment.matches(url.fragment):
            mismatch_description.append_text("fragment ")
            self.host.describe_mismatch(url.fragment, mismatch_description)
