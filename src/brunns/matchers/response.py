from collections.abc import Mapping, Sequence
from datetime import timedelta
from typing import Optional, Union

import httpx
import requests
from deprecated import deprecated
from furl import furl
from hamcrest import anything, described_as, has_entry
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription
from yarl import URL

from brunns.matchers.data import JsonStructure
from brunns.matchers.object import between
from brunns.matchers.utils import (
    append_matcher_description,
    describe_field_match,
    describe_field_mismatch,
)

ANYTHING = anything()


def is_response() -> "ResponseMatcher":
    """Matches :requests.models.Response: or :httpx.Response:.

    Todo:

    """
    return ResponseMatcher()


ResponseType = Union[requests.Response, httpx.Response]


class ResponseMatcher(BaseMatcher[ResponseType]):
    """Matches :requests.models.Response: or :httpx.Response:.
    :param status_code: Expected status code
    :param body: Expected body
    :param content: Expected content
    :param json: Expected json
    :param headers: Expected headers
    :param cookies: Expected cookies
    :param elapsed: Expected elapsed time
    :param history: Expected history
    :param url: Expected url
    :param encoding: Expected encoding
    """

    def __init__(
        self,
        status_code: Union[int, Matcher[int]] = ANYTHING,
        body: Union[str, Matcher[str]] = ANYTHING,
        content: Union[bytes, Matcher[bytes]] = ANYTHING,
        json: Union[JsonStructure, Matcher[JsonStructure]] = ANYTHING,
        headers: Union[
            Mapping[str, Union[str, Matcher[str]]],
            Matcher[Mapping[str, Union[str, Matcher[str]]]],
        ] = ANYTHING,
        cookies: Union[
            Mapping[str, Union[str, Matcher[str]]],
            Matcher[Mapping[str, Union[str, Matcher[str]]]],
        ] = ANYTHING,
        elapsed: Union[timedelta, Matcher[timedelta]] = ANYTHING,
        history: Union[
            Sequence[
                Union[
                    ResponseType,
                    Matcher[ResponseType],
                ]
            ],
            Matcher[
                Sequence[
                    Union[
                        ResponseType,
                        Matcher[ResponseType],
                    ]
                ]
            ],
        ] = ANYTHING,
        url: Union[furl, str, Matcher[Union[furl, str]]] = ANYTHING,
        encoding: Union[Optional[str], Matcher[Optional[str]]] = ANYTHING,
    ) -> None:
        super().__init__()
        self.status_code: Matcher[int] = wrap_matcher(status_code)
        self.body: Matcher[str] = wrap_matcher(body)
        self.content: Matcher[bytes] = wrap_matcher(content)
        self.json: Matcher[JsonStructure] = wrap_matcher(json)
        self.headers: Matcher[Mapping[str, Union[str, Matcher[str]]]] = wrap_matcher(headers)
        self.cookies: Matcher[Mapping[str, Union[str, Matcher[str]]]] = wrap_matcher(cookies)
        self.elapsed = wrap_matcher(elapsed)
        self.history = wrap_matcher(history)
        self.url = wrap_matcher(url)
        self.encoding = wrap_matcher(encoding)

    def _matches(self, response: ResponseType) -> bool:
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
    def _get_response_json(response: ResponseType) -> Optional[str]:
        try:
            return response.json()
        except (ValueError, AttributeError):
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

    def describe_mismatch(self, response: ResponseType, mismatch_description: Description) -> None:
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

    def describe_match(self, response: ResponseType, match_description: Description) -> None:
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

    def with_status_code(self, status_code: Union[int, Matcher[int]]):
        self.status_code = wrap_matcher(status_code)
        return self

    def and_status_code(self, status_code: Union[int, Matcher[int]]):
        return self.with_status_code(status_code)

    def with_body(self, body: Union[str, Matcher[str]]):
        self.body = wrap_matcher(body)
        return self

    def and_body(self, body: Union[str, Matcher[str]]):
        return self.with_body(body)

    def with_content(self, content: Union[bytes, Matcher[bytes]]):
        self.content = wrap_matcher(content)
        return self

    def and_content(self, content: Union[bytes, Matcher[bytes]]):
        return self.with_content(content)

    def with_json(self, json: Union[JsonStructure, Matcher[JsonStructure]]):
        self.json = wrap_matcher(json)
        return self

    def and_json(self, json: Union[JsonStructure, Matcher[JsonStructure]]):
        return self.with_json(json)

    def with_headers(
        self,
        headers: Union[Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]],
    ):
        self.headers = wrap_matcher(headers)
        return self

    def and_headers(
        self,
        headers: Union[Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]],
    ):
        return self.with_headers(headers)

    def with_cookies(
        self,
        cookies: Union[Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]],
    ):
        self.cookies = wrap_matcher(cookies)
        return self

    def and_cookies(
        self,
        cookies: Union[Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]],
    ):
        return self.with_cookies(cookies)

    def with_elapsed(self, elapsed: Union[timedelta, Matcher[timedelta]]):
        self.elapsed = wrap_matcher(elapsed)
        return self

    def and_elapsed(self, elapsed: Union[timedelta, Matcher[timedelta]]):
        return self.with_elapsed(elapsed)

    def with_history(
        self,
        history: Union[
            Sequence[
                Union[
                    ResponseType,
                    Matcher[ResponseType],
                ]
            ],
            Matcher[
                Sequence[
                    Union[
                        ResponseType,
                        Matcher[ResponseType],
                    ]
                ]
            ],
        ],
    ):
        self.history = wrap_matcher(history)
        return self

    def and_history(
        self,
        history: Union[
            Sequence[Union[ResponseType, Matcher[ResponseType]]],
            Matcher[Sequence[Union[ResponseType, Matcher[ResponseType]]]],
        ],
    ):
        return self.with_history(history)

    def with_url(self, url: Union[furl, str, Matcher[Union[furl, str]]]):
        self.url = wrap_matcher(url)
        return self

    def and_url(self, url: Union[furl, str, Matcher[Union[furl, str]]]):
        return self.with_url(url)

    def with_encoding(self, encoding: Union[Optional[str], Matcher[Optional[str]]]):
        self.encoding = wrap_matcher(encoding)
        return self

    def and_encoding(self, encoding: Union[Optional[str], Matcher[Optional[str]]]):
        return self.with_encoding(encoding)


def redirects_to(url_matcher: Union[str, Matcher[str], URL, Matcher[URL]]) -> Matcher[ResponseType]:
    """Is a response a redirect to a URL matching the supplied matcher? Matches :requests.models.Response: or
    :httpx.Response:.
    :param url_matcher: Expected URL.
    """
    return described_as(
        str(StringDescription().append_text("redirects to ").append_description_of(url_matcher)),
        is_response().with_status_code(between(300, 399)).and_headers(has_entry("Location", url_matcher)),
    )


@deprecated(version="2.3.0", reason="Use builder style is_response()")
def response_with(
    status_code: Union[int, Matcher[int]] = ANYTHING,
    body: Union[str, Matcher[str]] = ANYTHING,
    content: Union[bytes, Matcher[bytes]] = ANYTHING,
    json: Union[JsonStructure, Matcher[JsonStructure]] = ANYTHING,
    headers: Union[Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]] = ANYTHING,
) -> ResponseMatcher:  # pragma: no cover
    return ResponseMatcher(status_code=status_code, body=body, content=content, json=json, headers=headers)
