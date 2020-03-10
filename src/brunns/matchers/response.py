# encoding=utf-8
from typing import Any, Mapping, Optional, Union

from brunns.builder import Builder  # type: ignore
from brunns.matchers.data import JsonStructure
from brunns.matchers.object import between
from hamcrest import anything, described_as, has_entry
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.core.isanything import IsAnything
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription
from requests import Response

ANYTHING = anything()


def response_with(
    status_code: Union[int, Matcher[int]] = ANYTHING,
    body: Union[str, Matcher[str]] = ANYTHING,
    content: Union[bytes, Matcher[bytes]] = ANYTHING,
    json: Union[JsonStructure, Matcher[JsonStructure]] = ANYTHING,
    headers: Union[
        Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]
    ] = ANYTHING,
) -> Matcher:
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
    ) -> None:
        super(ResponseMatcher, self).__init__()
        self.status_code = wrap_matcher(status_code)  # type: Matcher[int]
        self.body = wrap_matcher(body)  # type: Matcher[str]
        self.content = wrap_matcher(content)  # type: Matcher[bytes]
        self.json = wrap_matcher(json)  # type: Matcher[JsonStructure]
        self.headers = wrap_matcher(
            headers
        )  # type: Matcher[Mapping[str, Union[str, Matcher[str]]]]

    def _matches(self, response: Response) -> bool:
        response_json = self._get_response_json(response)
        return (
            self.status_code.matches(response.status_code)
            and self.body.matches(response.text)
            and self.content.matches(response.content)
            and self.json.matches(response_json)
            and self.headers.matches(response.headers)
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


def redirects_to(url_matcher: Union[str, Matcher]) -> Matcher[Response]:
    """Is a response a redirect to a URL matching the suplplied matcher? Matches :requests.models.Response:.
    :param url_matcher: Expected URL.
    """
    description = str(
        StringDescription().append_text("redirects to ").append_description_of(url_matcher)
    )
    matcher = response_with(
        status_code=between(300, 399), headers=has_entry("Location", url_matcher)
    )
    return described_as(description, matcher)


class response(Builder):
    target = ResponseMatcher
