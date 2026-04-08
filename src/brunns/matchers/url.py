from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Protocol, TypeVar, runtime_checkable

from deprecated import deprecated
from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from yarl import URL

from brunns.matchers.utils import (
    append_matcher_description,
    describe_field_match,
    describe_field_mismatch,
)

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence

    from hamcrest.core.description import Description
    from hamcrest.core.matcher import Matcher


@runtime_checkable
class UrlProtocol(Protocol):
    """Structural typing for URL objects."""

    @property
    def scheme(self) -> str: ...
    @property
    def password(self) -> str | None: ...
    @property
    def host(self) -> str | None: ...
    @property
    def port(self) -> int | None: ...
    @property
    def path(self) -> str: ...
    @property
    def query(self) -> Mapping[str, str]: ...


U = TypeVar("U", bound=UrlProtocol)

ANYTHING = anything()

logger = logging.getLogger(__name__)


def is_url() -> UrlWith:
    """Matches a string (or ``furl`` / ``yarl.URL`` object) as a URL.

    This function returns a :class:`UrlWith` matcher which can be refined using builder methods
    to match specific parts of the URL (e.g. ``.with_host(...)``, ``.with_query(...)``).

    Requires brunns-matchers to have been installed with the `url` extra.

    :return: A matcher for URL components.
    """
    return UrlWith()


class UrlWith(BaseMatcher[U]):
    """Matches specific components of a URL.

    The matcher parses the actual value using the ``furl`` library.

    :param host: Expected hostname (e.g., "google.com").
    :param path: Expected path string (e.g., "/search").
    :param query: Expected query parameters dictionary.
    :param fragment: Expected URL fragment (hash).
    """

    def __init__(
        self,
        host: str | None | Matcher[str | None] = ANYTHING,
        path: str | Matcher[str] = ANYTHING,
        query: Mapping[str, str | Matcher[str]] | Matcher[Mapping[str, str | Matcher[str]]] = ANYTHING,
        fragment: str | Matcher[str] = ANYTHING,
    ) -> None:
        super().__init__()

        self.scheme: Matcher[str] = ANYTHING
        self.username: Matcher[str | None] = ANYTHING
        self.password: Matcher[str | None] = ANYTHING
        self.host: Matcher[str | None] = wrap_matcher(host)
        self.port: Matcher[int | None] = ANYTHING
        self.path = wrap_matcher(path)
        self.path_segments: Matcher[Sequence[str]] = ANYTHING
        self.query = wrap_matcher(query)
        self.fragment = wrap_matcher(fragment)

    def _matches(self, url: U) -> bool:
        parsed_url = URL(str(url))
        return (
            self.scheme.matches(parsed_url.scheme)
            and self.username.matches(parsed_url.user)
            and self.password.matches(parsed_url.password)
            and self.host.matches(parsed_url.host)
            and self.port.matches(parsed_url.port)
            and self.path.matches(parsed_url.path)
            and self.path_segments.matches(parsed_url.parts[1:])
            and self.query.matches(parsed_url.query)
            and self.fragment.matches(parsed_url.fragment)
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

    def describe_mismatch(self, url: U, mismatch_description: Description) -> None:
        parsed_url = URL(str(url))
        mismatch_description.append_text("was URL with")
        describe_field_mismatch(self.scheme, "scheme", parsed_url.scheme, mismatch_description)
        describe_field_mismatch(self.username, "username", parsed_url.user, mismatch_description)
        describe_field_mismatch(self.password, "password", parsed_url.password, mismatch_description)
        describe_field_mismatch(self.host, "host", parsed_url.host, mismatch_description)
        describe_field_mismatch(self.port, "port", parsed_url.port, mismatch_description)
        describe_field_mismatch(self.path, "path", parsed_url.path, mismatch_description)
        describe_field_mismatch(self.path_segments, "path segments", parsed_url.parts[1:], mismatch_description)
        describe_field_mismatch(self.query, "query", parsed_url.query, mismatch_description)
        describe_field_mismatch(self.fragment, "fragment", parsed_url.fragment, mismatch_description)

    def describe_match(self, url: U, match_description: Description) -> None:
        parsed_url = URL(str(url))
        match_description.append_text("was URL with")
        describe_field_match(self.scheme, "scheme", parsed_url.scheme, match_description)
        describe_field_match(self.username, "username", parsed_url.user, match_description)
        describe_field_match(self.password, "password", parsed_url.password, match_description)
        describe_field_match(self.host, "host", parsed_url.host, match_description)
        describe_field_match(self.port, "port", parsed_url.port, match_description)
        describe_field_match(self.path, "path", parsed_url.path, match_description)
        describe_field_match(self.path_segments, "path segments", parsed_url.parts[1:], match_description)
        describe_field_match(self.query, "query", parsed_url.query, match_description)
        describe_field_match(self.fragment, "fragment", parsed_url.fragment, match_description)

    def with_scheme(self, scheme: str | Matcher[str]) -> UrlWith:
        """Matches if the URL scheme matches the given value or matcher.

        :param scheme: The expected scheme (e.g. "https") or matcher.
        :return: UrlWith, for chaining.
        """
        self.scheme = wrap_matcher(scheme)
        return self

    def and_scheme(self, scheme: str | Matcher[str]) -> UrlWith:
        """Matches if the URL scheme matches the given value or matcher.

        A synonym for :meth:`with_scheme`.

        :param scheme: The expected scheme or matcher.
        :return: UrlWith, for chaining.
        """
        return self.with_scheme(scheme)

    def with_username(self, username: str | None | Matcher[str | None]) -> UrlWith:
        """Matches if the URL username matches the given value or matcher.

        :param username: The expected username or matcher.
        :return: UrlWith, for chaining.
        """
        self.username = wrap_matcher(username)
        return self

    def and_username(self, username: str | None | Matcher[str | None]) -> UrlWith:
        """Matches if the URL username matches the given value or matcher.

        A synonym for :meth:`with_username`.

        :param username: The expected username or matcher.
        :return: UrlWith, for chaining.
        """
        return self.with_username(username)

    def with_password(self, password: str | None | Matcher[str | None]) -> UrlWith:
        """Matches if the URL password matches the given value or matcher.

        :param password: The expected password or matcher.
        :return: UrlWith, for chaining.
        """
        self.password = wrap_matcher(password)
        return self

    def and_password(self, password: str | None | Matcher[str | None]) -> UrlWith:
        """Matches if the URL password matches the given value or matcher.

        A synonym for :meth:`with_password`.

        :param password: The expected password or matcher.
        :return: UrlWith, for chaining.
        """
        return self.with_password(password)

    def with_host(self, host: str | None | Matcher[str | None]) -> UrlWith:
        """Matches if the URL host matches the given value or matcher.

        :param host: The expected hostname or matcher.
        :return: UrlWith, for chaining.
        """
        self.host = wrap_matcher(host)
        return self

    def and_host(self, host: str | None | Matcher[str | None]) -> UrlWith:
        """Matches if the URL host matches the given value or matcher.

        A synonym for :meth:`with_host`.

        :param host: The expected hostname or matcher.
        :return: UrlWith, for chaining.
        """
        return self.with_host(host)

    def with_port(self, port: int | None | Matcher[int | None]) -> UrlWith:
        """Matches if the URL port matches the given value or matcher.

        :param port: The expected port integer or matcher.
        :return: UrlWith, for chaining.
        """
        self.port = wrap_matcher(port)
        return self

    def and_port(self, port: int | None | Matcher[int | None]) -> UrlWith:
        """Matches if the URL port matches the given value or matcher.

        A synonym for :meth:`with_port`.

        :param port: The expected port integer or matcher.
        :return: UrlWith, for chaining.
        """
        return self.with_port(port)

    def with_path(self, path: str | Matcher[str]) -> UrlWith:
        """Matches if the URL path matches the given value or matcher.

        :param path: The expected path string (e.g. "/foo/bar") or matcher.
        :return: UrlWith, for chaining.
        """
        self.path = wrap_matcher(path)
        return self

    def and_path(self, path: str | Matcher[str]) -> UrlWith:
        """Matches if the URL path matches the given value or matcher.

        A synonym for :meth:`with_path`.

        :param path: The expected path string or matcher.
        :return: UrlWith, for chaining.
        """
        return self.with_path(path)

    def with_path_segments(self, path_segments: Sequence[str] | Matcher[Sequence[str]]) -> UrlWith:
        """Matches if the URL path segments match the given sequence or matcher.

        :param path_segments: The expected sequence of path segments (e.g. ["foo", "bar"]) or matcher.
        :return: UrlWith, for chaining.
        """
        self.path_segments = wrap_matcher(path_segments)
        return self

    def and_path_segments(self, path_segments: Sequence[str] | Matcher[Sequence[str]]) -> UrlWith:
        """Matches if the URL path segments match the given sequence or matcher.

        A synonym for :meth:`with_path_segments`.

        :param path_segments: The expected sequence of path segments or matcher.
        :return: UrlWith, for chaining.
        """
        return self.with_path_segments(path_segments)

    def with_query(
        self,
        query: Mapping[str, str | Matcher[str]] | Matcher[Mapping[str, str | Matcher[str]]],
    ) -> UrlWith:
        """Matches if the URL query parameters match the given dictionary or matcher.

        :param query: The expected query parameters dictionary or matcher.
        :return: UrlWith, for chaining.
        """
        self.query = wrap_matcher(query)
        return self

    def and_query(
        self,
        query: Mapping[str, str | Matcher[str]] | Matcher[Mapping[str, str | Matcher[str]]],
    ) -> UrlWith:
        """Matches if the URL query parameters match the given dictionary or matcher.

        A synonym for :meth:`with_query`.

        :param query: The expected query parameters dictionary or matcher.
        :return: UrlWith, for chaining.
        """
        return self.with_query(query)

    def with_fragment(self, fragment: str | Matcher[str]) -> UrlWith:
        """Matches if the URL fragment (hash) matches the given value or matcher.

        :param fragment: The expected fragment string or matcher.
        :return: UrlWith, for chaining.
        """
        self.fragment = wrap_matcher(fragment)
        return self

    def and_fragment(self, fragment: str | Matcher[str]) -> UrlWith:
        """Matches if the URL fragment (hash) matches the given value or matcher.

        A synonym for :meth:`with_fragment`.

        :param fragment: The expected fragment string or matcher.
        :return: UrlWith, for chaining.
        """
        return self.with_fragment(fragment)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_host(matcher: str | Matcher):  # pragma: no cover
    """Matches URL with specific host.

    .. deprecated:: 2.3.0
       Use ``is_url().with_host(...)`` instead.
    """
    return UrlWith(host=matcher)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_path(matcher: str | Matcher):  # pragma: no cover
    """Matches URL with specific path.

    .. deprecated:: 2.3.0
       Use ``is_url().with_path(...)`` instead.
    """
    return UrlWith(path=matcher)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_query(matcher: Mapping[str, str] | Matcher):  # pragma: no cover
    """Matches URL with specific query parameters.

    .. deprecated:: 2.3.0
       Use ``is_url().with_query(...)`` instead.
    """
    return UrlWith(query=matcher)


@deprecated(version="2.3.0", reason="Use builder style is_url()")
def url_with_fragment(matcher: str | Matcher):  # pragma: no cover
    """Matches URL with specific fragment.

    .. deprecated:: 2.3.0
       Use ``is_url().with_fragment(...)`` instead.
    """
    return UrlWith(fragment=matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def to_host(matcher: str | Matcher):  # pragma: no cover
    """Matches URL with specific host.

    .. deprecated:: 2.2.0
       Use ``is_url().with_host(...)`` instead.
    """
    return url_with_host(matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def with_path(matcher: str | Matcher):  # pragma: no cover
    """Matches URL with specific path.

    .. deprecated:: 2.2.0
       Use ``is_url().with_path(...)`` instead.
    """
    return url_with_path(matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def with_query(matcher: Mapping[str, str] | Matcher):  # pragma: no cover
    """Matches URL with specific query parameters.

    .. deprecated:: 2.2.0
       Use ``is_url().with_query(...)`` instead.
    """
    return url_with_query(matcher)


@deprecated(version="2.2.0", reason="Use builder style is_url()")
def with_fragment(matcher: str | Matcher):  # pragma: no cover
    """Matches URL with specific fragment.

    .. deprecated:: 2.2.0
       Use ``is_url().with_fragment(...)`` instead.
    """
    return url_with_fragment(matcher)
