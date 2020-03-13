# encoding=utf-8
from typing import Any, Mapping, Optional, Union

from brunns.matchers.data import JsonStructure
from brunns.matchers.object import between
from deprecated import deprecated
from hamcrest import anything, described_as, has_entry
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.core.isanything import IsAnything
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription
from requests import Response

ANYTHING = anything()


def is_response() -> "ResponseMatcher":
    """Matches :requests.models.Response:.


    """
    return ResponseMatcher()


@deprecated(version="2.3.0", reason="Use builder style is_response()")
def response_with(
    status_code: Union[int, Matcher[int]] = ANYTHING,
    body: Union[str, Matcher[str]] = ANYTHING,
    content: Union[bytes, Matcher[bytes]] = ANYTHING,
    json: Union[JsonStructure, Matcher[JsonStructure]] = ANYTHING,
    headers: Union[
        Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
    ] = ANYTHING,
) -> "ResponseMatcher":  # pragma: no cover
    """Matches :requests.models.Response:.

    :param status_code: Expected status code
    :param body: Expected body
    :param content: Expected content
    :param json: Expected json
    :param headers: Expected headers
    """
    return ResponseMatcher(
        status_code=status_code, body=body, content=content, json=json, headers=headers
    )


class ResponseMatcher(BaseMatcher[Response]):
    """Matches :requests.models.Response:.
    :param status_code: Expected status code
    :param body: Expected body
    :param content: Expected content
    :param json: Expected json
    :param headers: Expected headers
    :param cookies: Expected cookies
    """

    def __init__(
        self,
        status_code: Union[int, Matcher[int]] = ANYTHING,
        body: Union[str, Matcher[str]] = ANYTHING,
        content: Union[bytes, Matcher[bytes]] = ANYTHING,
        json: Union[JsonStructure, Matcher[JsonStructure]] = ANYTHING,
        headers: Union[
            Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
        ] = ANYTHING,
        cookies: Union[
            Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
        ] = ANYTHING,
    ) -> None:
        super(ResponseMatcher, self).__init__()
        self.status_code = wrap_matcher(status_code)  # type: Matcher[int]
        self.body = wrap_matcher(body)  # type: Matcher[str]
        self.content = wrap_matcher(content)  # type: Matcher[bytes]
        self.json = wrap_matcher(json)  # type: Matcher[JsonStructure]
        self.headers = wrap_matcher(
            headers
        )  # type: Matcher[Mapping[str, Union[str, Matcher[str]]]]
        self.cookies = wrap_matcher(
            cookies
        )  # type: Matcher[Mapping[str, Union[str, Matcher[str]]]]

    def _matches(self, response: Response) -> bool:
        response_json = self._get_response_json(response)
        return (
            self.status_code.matches(response.status_code)
            and self.body.matches(response.text)
            and self.content.matches(response.content)
            and self.json.matches(response_json)
            and self.headers.matches(response.headers)
            and self.cookies.matches(response.cookies)
        )

    @staticmethod
    def _get_response_json(response: Response) -> Optional[str]:
        try:
            return response.json()
        except ValueError:
            return None

    def describe_to(self, description: Description) -> None:
        description.append_text("response with")
        self._optional_description(description)

    def _optional_description(self, description: Description):
        self._append_matcher_descrption(description, self.status_code, "status_code")
        self._append_matcher_descrption(description, self.body, "body")
        self._append_matcher_descrption(description, self.content, "content")
        self._append_matcher_descrption(description, self.json, "json")
        self._append_matcher_descrption(description, self.headers, "headers")
        self._append_matcher_descrption(description, self.cookies, "cookies")

    @staticmethod
    def _append_matcher_descrption(description: Description, matcher: Matcher, text: str) -> None:
        if not isinstance(matcher, IsAnything):
            description.append_text(" {0}: ".format(text)).append_description_of(matcher)

    def describe_mismatch(self, response: Response, mismatch_description: Description) -> None:
        mismatch_description.append_text("was response with")
        self._describe_field_mismatch(
            self.status_code, "status code", response.status_code, mismatch_description
        )
        self._describe_field_mismatch(self.body, "body", response.text, mismatch_description)
        self._describe_field_mismatch(
            self.content, "content", response.content, mismatch_description
        )
        self._describe_field_mismatch(
            self.json, "json", self._get_response_json(response), mismatch_description
        )
        self._describe_field_mismatch(
            self.headers, "headers", response.headers, mismatch_description
        )
        self._describe_field_mismatch(
            self.cookies, "cookies", response.cookies, mismatch_description
        )

    @staticmethod
    def _describe_field_mismatch(
        field_matcher: Matcher[Any],
        field_name: str,
        actual_value: Any,
        mismatch_description: Description,
    ) -> None:
        if field_matcher is not ANYTHING:
            mismatch_description.append_text(" {0}: ".format(field_name)).append_description_of(
                actual_value
            )

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
        headers: Union[
            Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
        ],
    ):
        self.headers = wrap_matcher(headers)
        return self

    def and_headers(
        self,
        headers: Union[
            Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
        ],
    ):
        return self.with_headers(headers)

    def with_cookies(
        self,
        cookies: Union[
            Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
        ],
    ):
        self.cookies = wrap_matcher(cookies)
        return self

    def and_cookies(
        self,
        cookies: Union[
            Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
        ],
    ):
        return self.with_cookies(cookies)


def redirects_to(url_matcher: Union[str, Matcher]) -> Matcher[Response]:
    """Is a response a redirect to a URL matching the suplplied matcher? Matches :requests.models.Response:.
    :param url_matcher: Expected URL.
    """
    return described_as(
        str(StringDescription().append_text("redirects to ").append_description_of(url_matcher)),
        is_response()
        .with_status_code(between(300, 399))
        .and_headers(has_entry("Location", url_matcher)),
    )
