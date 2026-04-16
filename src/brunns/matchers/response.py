from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, TypeVar, runtime_checkable

from deprecated import deprecated
from hamcrest import anything, described_as, has_entry
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.string_description import StringDescription

from brunns.matchers.object import between
from brunns.matchers.utils import (
    append_matcher_description,
    describe_field_match,
    describe_field_mismatch,
)

if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from datetime import timedelta

    from hamcrest.core.description import Description
    from hamcrest.core.matcher import Matcher

    from brunns.matchers.data import JsonValue
    from brunns.matchers.url import UrlProtocol


@runtime_checkable
class ResponseProtocol(Protocol):
    """Structural typing for HTTP Response objects."""

    @property
    def status_code(self) -> int: ...
    @property
    def text(self) -> str: ...
    @property
    def content(self) -> bytes: ...
    @property
    def headers(self) -> Mapping[str, str]: ...
    @property
    def cookies(self) -> Mapping[str, str]: ...
    @property
    def elapsed(self) -> timedelta: ...
    @property
    def history(self) -> Sequence[ResponseProtocol]: ...
    @property
    def url(self) -> Any: ...  ## Type differs between httpx and requests
    @property
    def encoding(self) -> str | None: ...

    def json(self) -> JsonValue | None: ...


R = TypeVar("R", bound=ResponseProtocol)


ANYTHING = anything()


def is_response() -> ResponseMatcher:
    """Matches an HTTP response object (requests, httpx, etc.).

    This function returns a :class:`ResponseMatcher` which can be refined using builder methods
    (e.g. ``.with_status_code(200)``).

    :return: A matcher for HTTP responses.
    """
    return ResponseMatcher()


class ResponseMatcher(BaseMatcher[R]):
    def __init__(
        self,
        status_code: int | Matcher[int] = ANYTHING,
        body: str | Matcher[str] = ANYTHING,
        content: bytes | Matcher[bytes] = ANYTHING,
        json: JsonValue | Matcher[JsonValue] = ANYTHING,
        headers: Mapping[str, str | Matcher[str]] | Matcher[Mapping[str, str | Matcher[str]]] = ANYTHING,
        cookies: Mapping[str, str | Matcher[str]] | Matcher[Mapping[str, str | Matcher[str]]] = ANYTHING,
        elapsed: timedelta | Matcher[timedelta] = ANYTHING,
        history: Sequence[ResponseProtocol | Matcher[ResponseProtocol]]
        | Matcher[Sequence[ResponseProtocol | Matcher[ResponseProtocol]]] = ANYTHING,
        url: UrlProtocol | Matcher[UrlProtocol] = ANYTHING,
        encoding: str | None | Matcher[str | None] = ANYTHING,
    ) -> None:
        super().__init__()
        self.status_code = wrap_matcher(status_code)
        self.body = wrap_matcher(body)
        self.content = wrap_matcher(content)
        self.json = wrap_matcher(json)
        self.headers = wrap_matcher(headers)
        self.cookies = wrap_matcher(cookies)
        self.elapsed = wrap_matcher(elapsed)
        self.history = wrap_matcher(history)
        self.url = wrap_matcher(url)
        self.encoding = wrap_matcher(encoding)

    def _matches(self, response: R) -> bool:
        response_json = self._get_response_json(response)
        return (
            self.status_code.matches(response.status_code)
            and self.body.matches(response.text)
            and self.content.matches(response.content)
            and self.json.matches(response_json)
            and self.headers.matches(response.headers)
            and self.cookies.matches(response.cookies)
            and self.elapsed.matches(response.elapsed)
            and self.history.matches(response.history)
            and self.url.matches(response.url)
            and self.encoding.matches(response.encoding)
        )

    @staticmethod
    def _get_response_json(response: R) -> JsonValue:
        try:
            return response.json()
        except (ValueError, AttributeError, TypeError):
            return None

    def describe_to(self, description: Description) -> None:
        description.append_text("response with")
        append_matcher_description(self.status_code, "status code", description)
        append_matcher_description(self.body, "body", description)
        append_matcher_description(self.content, "content", description)
        append_matcher_description(self.json, "json", description)
        append_matcher_description(self.headers, "headers", description)
        append_matcher_description(self.cookies, "cookies", description)
        append_matcher_description(self.elapsed, "elapsed", description)
        append_matcher_description(self.history, "history", description)
        append_matcher_description(self.url, "url", description)
        append_matcher_description(self.encoding, "encoding", description)

    def describe_mismatch(self, response: R, mismatch_description: Description) -> None:
        mismatch_description.append_text("was response with")
        describe_field_mismatch(self.status_code, "status code", response.status_code, mismatch_description)
        describe_field_mismatch(self.body, "body", response.text, mismatch_description)
        describe_field_mismatch(self.content, "content", response.content, mismatch_description)
        describe_field_mismatch(self.json, "json", self._get_response_json(response), mismatch_description)
        describe_field_mismatch(self.headers, "headers", response.headers, mismatch_description)
        describe_field_mismatch(self.cookies, "cookies", response.cookies, mismatch_description)
        describe_field_mismatch(self.elapsed, "elapsed", response.elapsed, mismatch_description)
        describe_field_mismatch(self.history, "history", response.history, mismatch_description)
        describe_field_mismatch(self.url, "url", response.url, mismatch_description)
        describe_field_mismatch(self.encoding, "encoding", response.encoding, mismatch_description)

    def describe_match(self, response: R, match_description: Description) -> None:
        match_description.append_text("was response with")
        describe_field_match(self.status_code, "status code", response.status_code, match_description)
        describe_field_match(self.body, "body", response.text, match_description)
        describe_field_match(self.content, "content", response.content, match_description)
        describe_field_match(self.json, "json", self._get_response_json(response), match_description)
        describe_field_match(self.headers, "headers", response.headers, match_description)
        describe_field_match(self.cookies, "cookies", response.cookies, match_description)
        describe_field_match(self.elapsed, "elapsed", response.elapsed, match_description)
        describe_field_match(self.history, "history", response.history, match_description)
        describe_field_match(self.url, "url", response.url, match_description)
        describe_field_match(self.encoding, "encoding", response.encoding, match_description)

    def with_status_code(self, status_code: int | Matcher[int]) -> ResponseMatcher:
        """Matches if the response status code matches the given value or matcher.

        :param status_code: The expected status code (e.g. 200) or a matcher (e.g. ``between(200, 299)``).
        :return: ResponseMatcher, for chaining.
        """
        self.status_code = wrap_matcher(status_code)
        return self

    def and_status_code(self, status_code: int | Matcher[int]) -> ResponseMatcher:
        """Matches if the response status code matches the given value or matcher.

        A synonym for :meth:`with_status_code`.

        :param status_code: The expected status code.
        :return: ResponseMatcher, for chaining.
        """
        return self.with_status_code(status_code)

    def with_body(self, body: str | Matcher[str]) -> ResponseMatcher:
        """Matches if the response body text matches the given value or matcher.

        :param body: The expected body string or matcher.
        :return: ResponseMatcher, for chaining.
        """
        self.body = wrap_matcher(body)
        return self

    def and_body(self, body: str | Matcher[str]) -> ResponseMatcher:
        """Matches if the response body text matches the given value or matcher.

        A synonym for :meth:`with_body`.

        :param body: The expected body string or matcher.
        :return: ResponseMatcher, for chaining.
        """
        return self.with_body(body)

    def with_content(self, content: bytes | Matcher[bytes]) -> ResponseMatcher:
        """Matches if the response binary content matches the given value or matcher.

        :param content: The expected bytes or matcher.
        :return: ResponseMatcher, for chaining.
        """
        self.content = wrap_matcher(content)
        return self

    def and_content(self, content: bytes | Matcher[bytes]) -> ResponseMatcher:
        """Matches if the response binary content matches the given value or matcher.

        A synonym for :meth:`with_content`.

        :param content: The expected bytes or matcher.
        :return: ResponseMatcher, for chaining.
        """
        return self.with_content(content)

    def with_json(self, json: JsonValue | Matcher[JsonValue]) -> ResponseMatcher:
        """Matches if the response JSON body matches the given value or matcher.

        The response body is parsed as JSON before matching.

        :param json: The expected JSON structure (dict, list, etc.) or matcher.
        :return: ResponseMatcher, for chaining.
        """
        self.json = wrap_matcher(json)
        return self

    def and_json(self, json: JsonValue | Matcher[JsonValue]) -> ResponseMatcher:
        """Matches if the response JSON body matches the given value or matcher.

        A synonym for :meth:`with_json`.

        :param json: The expected JSON structure or matcher.
        :return: ResponseMatcher, for chaining.
        """
        return self.with_json(json)

    def with_headers(
        self,
        headers: Mapping[str, str | Matcher[str]] | Matcher[Mapping[str, str | Matcher[str]]],
    ) -> ResponseMatcher:
        """Matches if the response headers match the given value or matcher.

        :param headers: The expected headers dictionary or matcher.
        :return: ResponseMatcher, for chaining.
        """
        self.headers = wrap_matcher(headers)
        return self

    def and_headers(
        self,
        headers: Mapping[str, str | Matcher[str]] | Matcher[Mapping[str, str | Matcher[str]]],
    ) -> ResponseMatcher:
        """Matches if the response headers match the given value or matcher.

        A synonym for :meth:`with_headers`.

        :param headers: The expected headers dictionary or matcher.
        :return: ResponseMatcher, for chaining.
        """
        return self.with_headers(headers)

    def with_cookies(
        self,
        cookies: Mapping[str, str | Matcher[str]] | Matcher[Mapping[str, str | Matcher[str]]],
    ) -> ResponseMatcher:
        """Matches if the response cookies match the given value or matcher.

        :param cookies: The expected cookies dictionary or matcher.
        :return: ResponseMatcher, for chaining.
        """
        self.cookies = wrap_matcher(cookies)
        return self

    def and_cookies(
        self,
        cookies: Mapping[str, str | Matcher[str]] | Matcher[Mapping[str, str | Matcher[str]]],
    ) -> ResponseMatcher:
        """Matches if the response cookies match the given value or matcher.

        A synonym for :meth:`with_cookies`.

        :param cookies: The expected cookies dictionary or matcher.
        :return: ResponseMatcher, for chaining.
        """
        return self.with_cookies(cookies)

    def with_elapsed(self, elapsed: timedelta | Matcher[timedelta]) -> ResponseMatcher:
        """Matches if the response elapsed time matches the given value or matcher.

        :param elapsed: The expected timedelta or matcher.
        :return: ResponseMatcher, for chaining.
        """
        self.elapsed = wrap_matcher(elapsed)
        return self

    def and_elapsed(self, elapsed: timedelta | Matcher[timedelta]) -> ResponseMatcher:
        """Matches if the response elapsed time matches the given value or matcher.

        A synonym for :meth:`with_elapsed`.

        :param elapsed: The expected timedelta or matcher.
        :return: ResponseMatcher, for chaining.
        """
        return self.with_elapsed(elapsed)

    def with_history(
        self,
        history: Sequence[ResponseProtocol | Matcher[ResponseProtocol]]
        | Matcher[Sequence[ResponseProtocol | Matcher[ResponseProtocol]]],
    ) -> ResponseMatcher:
        """Matches if the response history (redirects) matches the given sequence or matcher.

        :param history: The expected sequence of responses/matchers or a sequence matcher.
        :return: ResponseMatcher, for chaining.
        """
        self.history = wrap_matcher(history)
        return self

    def and_history(
        self,
        history: Sequence[ResponseProtocol | Matcher[ResponseProtocol]]
        | Matcher[Sequence[ResponseProtocol | Matcher[ResponseProtocol]]],
    ) -> ResponseMatcher:
        """Matches if the response history (redirects) matches the given sequence or matcher.

        A synonym for :meth:`with_history`.

        :param history: The expected sequence or matcher.
        :return: ResponseMatcher, for chaining.
        """
        return self.with_history(history)

    def with_url(self, url: UrlProtocol | Matcher[UrlProtocol]) -> ResponseMatcher:
        """Matches if the response URL matches the given value or matcher.

        :param url: The expected URL string, object, or matcher.
        :return: ResponseMatcher, for chaining.
        """
        self.url = wrap_matcher(url)
        return self

    def and_url(self, url: UrlProtocol | Matcher[UrlProtocol]) -> ResponseMatcher:
        """Matches if the response URL matches the given value or matcher.

        A synonym for :meth:`with_url`.

        :param url: The expected URL string, object, or matcher.
        :return: ResponseMatcher, for chaining.
        """
        return self.with_url(url)

    def with_encoding(self, encoding: str | None | Matcher[str | None]) -> ResponseMatcher:
        """Matches if the response encoding matches the given value or matcher.

        :param encoding: The expected encoding string or matcher.
        :return: ResponseMatcher, for chaining.
        """
        self.encoding = wrap_matcher(encoding)
        return self

    def and_encoding(self, encoding: str | None | Matcher[str | None]) -> ResponseMatcher:
        """Matches if the response encoding matches the given value or matcher.

        A synonym for :meth:`with_encoding`.

        :param encoding: The expected encoding string or matcher.
        :return: ResponseMatcher, for chaining.
        """
        return self.with_encoding(encoding)


def redirects_to(url_matcher: UrlProtocol | Matcher[UrlProtocol]) -> Matcher[R]:
    """Is a response a redirect to a URL matching the supplied matcher?

    Matches if the status code is between 300 and 399 and the ``Location`` header matches
    the provided URL matcher.

    :param url_matcher: The expected URL (string or matcher) found in the Location header.
    :return: A matcher for redirect responses.
    """
    return described_as(
        str(StringDescription().append_text("redirects to ").append_description_of(url_matcher)),
        is_response()
        .with_status_code(between(300, 399))
        .and_headers(
            has_entry("Location", url_matcher)  # type: ignore[arg-type]
        ),
    )


@deprecated(version="2.3.0", reason="Use builder style is_response()")
def response_with(
    status_code: int | Matcher[int] = ANYTHING,
    body: str | Matcher[str] = ANYTHING,
    content: bytes | Matcher[bytes] = ANYTHING,
    json: JsonValue | Matcher[JsonValue] = ANYTHING,
    headers: Mapping[str, str | Matcher[str]] | Matcher[Mapping[str, str | Matcher[str]]] = ANYTHING,
) -> ResponseMatcher:  # pragma: no cover
    """Matches a response with specific attributes.

    .. deprecated:: 2.3.0
       Use :func:`is_response` and its builder methods instead.
    """
    return ResponseMatcher(status_code=status_code, body=body, content=content, json=json, headers=headers)
