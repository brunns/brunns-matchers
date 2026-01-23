import logging
from collections.abc import Mapping, Sequence
from typing import Union

from deprecated import deprecated
from furl import furl
from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher
from yarl import URL

from brunns.matchers.utils import (
    append_matcher_description,
    describe_field_match,
    describe_field_mismatch,
)

logger = logging.getLogger(__name__)
ANYTHING = anything()


def is_url() -> "UrlWith":
    """Matches a string (or ``furl`` / ``yarl.URL`` object) as a URL.

    This function returns a :class:`UrlWith` matcher which can be refined using builder methods
    to match specific parts of the URL (e.g. ``.with_host(...)``, ``.with_query(...)``).

    :return: A matcher for URL components.
    """
    return UrlWith()


class UrlWith(BaseMatcher[Union[str, URL, furl]]):
    """Matches specific components of a URL.

    The matcher parses the actual value using the ``furl`` library.

    :param host: Expected hostname (e.g., "google.com").
    :param path: Expected path string (e.g., "/search").
    :param query: Expected query parameters dictionary.
    :param fragment: Expected URL fragment (hash).
    """

    def __init__(
        self,
        host: Union[str, Matcher[str]] = ANYTHING,
        path: Union[str, Matcher[str]] = ANYTHING,
        query: Union[
            Mapping[str, Union[str, Matcher[str]]],
            Matcher[Mapping[str, Union[str, Matcher[str]]]],
        ] = ANYTHING,
        fragment: Union[str, Matcher[str]] = ANYTHING,
    ) -> None:
        super().__init__()
        self.scheme: Matcher[str] = ANYTHING
        self.username: Matcher[str] = ANYTHING
        self.password: Matcher[str] = ANYTHING
        self.host = wrap_matcher(host)
        self.port: Matcher[int] = ANYTHING
        self.path = wrap_matcher(path)
        self.path_segments: Matcher[Sequence[str]] = ANYTHING
        self.query = wrap_matcher(query)
        self.fragment = wrap_matcher(fragment)

    def _matches(self, url: Union[str, URL, furl]) -> bool:
        url = furl(url)
        return (
            self.scheme.matches(url.scheme)
            and self.username.matches(url.username)
            and self.password.matches(url.password)
            and self.host.matches(url.host)
            and self.port.matches(url.port)
            and self.path.matches(url.path)
            and self.path_segments.matches(url.path.segments)
            and self.query.matches(url.query.params)
            and self.fragment.matches(url.fragment)
        )

    def describe_to(self, description: Description) -> None:
        description.append_text("URL with")
        append_matcher_description(self.scheme, "scheme", description)
        append_matcher_description(self.username, "username", description)
        append_matcher_description(self.password, "password", description)
        append_matcher_description(self.host, "host", description)
        append_matcher_description(self.port, "port", description)
        append_matcher_description(self.path, "path", description)
        append_matcher_description(self.path_segments, "path segments", description)
        append_matcher_description(self.query, "query", description)
        append_matcher_description(self.fragment, "fragment", description)

    def describe_mismatch(self, url: Union[str, URL, furl], mismatch_description: Description) -> None:
        url = furl(url)
        mismatch_description.append_text("was URL with")
        describe_field_mismatch(self.scheme, "scheme", url.scheme, mismatch_description)
        describe_field_mismatch(self.username, "username", url.username, mismatch_description)
        describe_field_mismatch(self.password, "password", url.password, mismatch_description)
        describe_field_mismatch(self.host, "host", url.host, mismatch_description)
        describe_field_mismatch(self.port, "port", url.port, mismatch_description)
        describe_field_mismatch(self.path, "path", url.path, mismatch_description)
        describe_field_mismatch(self.path_segments, "path segments", url.path.segments, mismatch_description)
        describe_field_mismatch(self.query, "query", url.query.params, mismatch_description)
        describe_field_mismatch(self.fragment, "fragment", url.fragment, mismatch_description)

    def describe_match(self, url: Union[str, URL, furl], match_description: Description) -> None:
        url = furl(url)
        match_description.append_text("was URL with")
        describe_field_match(self.scheme, "scheme", url.scheme, match_description)
        describe_field_match(self.username, "username", url.username, match_description)
        describe_field_match(self.password, "password", url.password, match_description)
        describe_field_match(self.host, "host", url.host, match_description)
        describe_field_match(self.port, "port", url.port, match_description)
        describe_field_match(self.path, "path", url.path, match_description)
        describe_field_match(self.path_segments, "path segments", url.path.segments, match_description)
        describe_field_match(self.query, "query", url.query.params, match_description)
        describe_field_match(self.fragment, "fragment", url.fragment, match_description)

    def with_scheme(self, scheme: Union[str, Matcher[str]]):
        self.scheme = wrap_matcher(scheme)
        return self

    def and_scheme(self, scheme: Union[str, Matcher[str]]):
        return self.with_scheme(scheme)

    def with_username(self, username: Union[str, Matcher[str]]):
        self.username = wrap_matcher(username)
        return self

    def and_username(self, username: Union[str, Matcher[str]]):
        return self.with_username(username)

    def with_password(self, password: Union[str, Matcher[str]]):
        self.password = wrap_matcher(password)
        return self

    def and_password(self, password: Union[str, Matcher[str]]):
        return self.with_password(password)

    def with_host(self, host: Union[str, Matcher[str]]):
        self.host = wrap_matcher(host)
        return self

    def and_host(self, host: Union[str, Matcher[str]]):
        return self.with_host(host)

    def with_port(self, port: Union[int, Matcher[int]]):
        self.port = wrap_matcher(port)
        return self

    def and_port(self, port: Union[int, Matcher[int]]):
        return self.with_port(port)

    def with_path(self, path: Union[str, Matcher[str]]):
        self.path = wrap_matcher(path)
        return self

    def and_path(self, path: Union[str, Matcher[str]]):
        return self.with_path(path)

    def with_path_segments(self, path_segments: Union[Sequence[str], Matcher[Sequence[str]]]):
        self.path_segments = wrap_matcher(path_segments)
        return self

    def and_path_segments(self, path_segments: Union[Sequence[str], Matcher[Sequence[str]]]):
        return self.with_path_segments(path_segments)

    def with_query(
        self,
        query: Union[Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]],
    ):
        self.query = wrap_matcher(query)
        return self

    def and_query(
        self,
        query: Union[Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]],
    ):
        return self.with_query(query)

    def with_fragment(self, fragment: Union[str, Matcher[str]]):
        self.fragment = wrap_matcher(fragment)
        return self

    def and_fragment(self, fragment: Union[str, Matcher[str]]):
        return self.with_fragment(fragment)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_host(matcher: Union[str, Matcher]):  # pragma: no cover
    """Matches URL with specific host.

    .. deprecated:: 2.3.0
       Use ``is_url().with_host(...)`` instead.
    """
    return UrlWith(host=matcher)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_path(matcher: Union[str, Matcher]):  # pragma: no cover
    """Matches URL with specific path.

    .. deprecated:: 2.3.0
       Use ``is_url().with_path(...)`` instead.
    """
    return UrlWith(path=matcher)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_query(matcher: Union[Mapping[str, str], Matcher]):  # pragma: no cover
    """Matches URL with specific query parameters.

    .. deprecated:: 2.3.0
       Use ``is_url().with_query(...)`` instead.
    """
    return UrlWith(query=matcher)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_fragment(matcher: Union[str, Matcher]):  # pragma: no cover
    """Matches URL with specific fragment.

    .. deprecated:: 2.3.0
       Use ``is_url().with_fragment(...)`` instead.
    """
    return UrlWith(fragment=matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def to_host(matcher: Union[str, Matcher]):  # pragma: no cover
    """Matches URL with specific host.

    .. deprecated:: 2.2.0
       Use ``is_url().with_host(...)`` instead.
    """
    return url_with_host(matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def with_path(matcher: Union[str, Matcher]):  # pragma: no cover
    """Matches URL with specific path.

    .. deprecated:: 2.2.0
       Use ``is_url().with_path(...)`` instead.
    """
    return url_with_path(matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def with_query(matcher: Union[Mapping[str, str], Matcher]):  # pragma: no cover
    """Matches URL with specific query parameters.

    .. deprecated:: 2.2.0
       Use ``is_url().with_query(...)`` instead.
    """
    return url_with_query(matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def with_fragment(matcher: Union[str, Matcher]):  # pragma: no cover
    """Matches URL with specific fragment.

    .. deprecated:: 2.2.0
       Use ``is_url().with_fragment(...)`` instead.
    """
    return url_with_fragment(matcher)
