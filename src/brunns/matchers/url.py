# encoding=utf-8
import logging
from typing import Mapping, Union

from deprecated import deprecated
from furl import furl
from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

from brunns.matchers.utils import append_matcher_description, describe_field_mismatch

logger = logging.getLogger(__name__)
ANYTHING = anything()


def is_url() -> "UrlWith":
    """TODO"""
    return UrlWith()


class UrlWith(BaseMatcher[Union[furl, str]]):
    def __init__(
        self,
        host: Union[str, Matcher[str]] = ANYTHING,
        path: Union[str, Matcher[str]] = ANYTHING,
        query: Union[
            Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
        ] = ANYTHING,
        fragment: Union[str, Matcher[str]] = ANYTHING,
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
        append_matcher_description(self.host, "host", description)
        append_matcher_description(self.path, "path", description)
        append_matcher_description(self.query, "query", description)
        append_matcher_description(self.fragment, "fragment", description)

    def describe_mismatch(self, url: Union[furl, str], mismatch_description: Description) -> None:
        url = url if isinstance(url, furl) else furl(url)
        mismatch_description.append_text("was URL with")
        describe_field_mismatch(self.host, "host", url.host, mismatch_description)
        describe_field_mismatch(self.path, "path", url.path, mismatch_description)
        describe_field_mismatch(self.query, "query", url.query.params, mismatch_description)
        describe_field_mismatch(self.fragment, "fragment", url.fragment, mismatch_description)

    def with_host(self, host: Union[str, Matcher[str]]):
        self.host = wrap_matcher(host)
        return self

    def and_host(self, host: Union[str, Matcher[str]]):
        return self.with_host(host)

    def with_path(self, path: Union[str, Matcher[str]]):
        self.path = wrap_matcher(path)
        return self

    def and_path(self, path: Union[str, Matcher[str]]):
        return self.with_path(path)

    def with_query(
        self,
        query: Union[
            Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
        ],
    ):
        self.query = wrap_matcher(query)
        return self

    def and_query(
        self,
        query: Union[
            Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
        ],
    ):
        return self.with_query(query)

    def with_fragment(self, fragment: Union[str, Matcher[str]]):
        self.fragment = wrap_matcher(fragment)
        return self

    def and_fragment(self, fragment: Union[str, Matcher[str]]):
        return self.with_fragment(fragment)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_host(matcher: Union[str, Matcher]):  # pragma: no cover
    return UrlWith(host=matcher)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_path(matcher: Union[str, Matcher]):  # pragma: no cover
    return UrlWith(path=matcher)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_query(matcher: Union[Mapping[str, str], Matcher]):  # pragma: no cover
    return UrlWith(query=matcher)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_fragment(matcher: Union[str, Matcher]):  # pragma: no cover
    return UrlWith(fragment=matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def to_host(matcher: Union[str, Matcher]):  # pragma: no cover
    return url_with_host(matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def with_path(matcher: Union[str, Matcher]):  # pragma: no cover
    return url_with_path(matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def with_query(matcher: Union[Mapping[str, str], Matcher]):  # pragma: no cover
    return url_with_query(matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def with_fragment(matcher: Union[str, Matcher]):  # pragma: no cover
    return url_with_fragment(matcher)
