# encoding=utf-8
import logging
from typing import Any, Mapping, Union

from deprecated import deprecated
from furl import furl
from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.core.isanything import IsAnything
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

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
        self._append_matcher_description(description, self.host, "host")
        self._append_matcher_description(description, self.path, "path")
        self._append_matcher_description(description, self.query, "query")
        self._append_matcher_description(description, self.fragment, "fragment")

    @staticmethod
    def _append_matcher_description(description: Description, matcher: Matcher, text: str) -> None:
        if not isinstance(matcher, IsAnything):
            description.append_text(" {0}: ".format(text)).append_description_of(matcher)

    def describe_mismatch(self, url: Union[furl, str], mismatch_description: Description) -> None:
        url = url if isinstance(url, furl) else furl(url)
        mismatch_description.append_text("was URL with")
        self._describe_field_mismatch(self.host, "host", url.host, mismatch_description)
        self._describe_field_mismatch(self.path, "path", url.path, mismatch_description)
        self._describe_field_mismatch(self.query, "query", url.query.params, mismatch_description)
        self._describe_field_mismatch(self.fragment, "fragment", url.fragment, mismatch_description)

    @staticmethod
    def _describe_field_mismatch(
        field_matcher: Matcher[Any],
        field_name: str,
        actual_value: Any,
        mismatch_description: Description,
    ) -> None:
        if field_matcher is not ANYTHING and not field_matcher.matches(actual_value):
            mismatch_description.append_text(" {0}: ".format(field_name))
            field_matcher.describe_mismatch(actual_value, mismatch_description)

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
