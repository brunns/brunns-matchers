from collections.abc import Mapping
from typing import Any, Union, cast

from hamcrest import anything, described_as, has_entry
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription
from werkzeug.test import TestResponse as Response

from brunns.matchers.data import JsonStructure
from brunns.matchers.object import between
from brunns.matchers.utils import (
    append_matcher_description,
    describe_field_match,
    describe_field_mismatch,
)

ANYTHING = anything()


def is_werkzeug_response() -> "WerkzeugResponseMatcher":
    """Matches a ``werkzeug.test.TestResponse`` object (e.g. from Flask test client).

    This function returns a :class:`WerkzeugResponseMatcher` which can be refined using builder methods
    (e.g., ``.with_status_code(200)``).

    :return: A matcher for Werkzeug/Flask test responses.
    """
    return WerkzeugResponseMatcher()


class WerkzeugResponseMatcher(BaseMatcher[Response]):
    """Matches a ``werkzeug.test.TestResponse`` object.

    This matcher is useful for testing Flask applications using the built-in test client.
    """

    def __init__(
        self,
    ) -> None:
        super().__init__()
        self.status_code: Matcher[int] = ANYTHING
        self.text: Matcher[str] = ANYTHING
        self.mimetype: Matcher[str] = ANYTHING
        self.json: Matcher[JsonStructure] = ANYTHING
        self.headers: Matcher[Mapping[str, Union[str, Matcher[str]]]] = ANYTHING

    def _matches(self, response: Response) -> bool:
        return (
            self.status_code.matches(response.status_code)
            and self.text.matches(response.text)
            and self.mimetype.matches(response.mimetype or "")
            and self.json.matches(response.json)
            and self.headers.matches(cast("Mapping[str, Any]", response.headers))
        )

    def describe_to(self, description: Description) -> None:
        description.append_text("response with")
        append_matcher_description(self.status_code, "status code", description)
        append_matcher_description(self.text, "text", description)
        append_matcher_description(self.mimetype, "mimetype", description)
        append_matcher_description(self.json, "json", description)
        append_matcher_description(self.headers, "headers", description)

    def describe_mismatch(self, response: Response, mismatch_description: Description) -> None:
        mismatch_description.append_text("was response with")
        describe_field_mismatch(self.status_code, "status code", response.status_code, mismatch_description)
        describe_field_mismatch(self.text, "text", response.text, mismatch_description)
        describe_field_mismatch(self.mimetype, "mimetype", response.mimetype, mismatch_description)
        describe_field_mismatch(self.json, "json", response.json, mismatch_description)
        describe_field_mismatch(self.headers, "headers", response.headers, mismatch_description)

    def describe_match(self, response: Response, match_description: Description) -> None:
        match_description.append_text("was response with")
        describe_field_match(self.status_code, "status code", response.status_code, match_description)
        describe_field_match(self.text, "text", response.text, match_description)
        describe_field_match(self.mimetype, "mimetype", response.mimetype, match_description)
        describe_field_match(self.json, "json", response.json, match_description)
        describe_field_match(self.headers, "headers", response.headers, match_description)

    def with_status_code(self, status_code: Union[int, Matcher[int]]) -> "WerkzeugResponseMatcher":
        """Matches if the response status code matches the given value or matcher.

        :param status_code: The expected status code (e.g. 200) or matcher.
        :return: Self, for chaining.
        """
        self.status_code = wrap_matcher(status_code)
        return self

    def and_status_code(self, status_code: Union[int, Matcher[int]]) -> "WerkzeugResponseMatcher":
        """Matches if the response status code matches the given value or matcher.

        A synonym for :meth:`with_status_code`.

        :param status_code: The expected status code or matcher.
        :return: Self, for chaining.
        """
        return self.with_status_code(status_code)

    def with_text(self, text: Union[str, Matcher[str]]) -> "WerkzeugResponseMatcher":
        """Matches if the response body text matches the given value or matcher.

        :param text: The expected body text string or matcher.
        :return: Self, for chaining.
        """
        self.text = wrap_matcher(text)
        return self

    def and_text(self, text: Union[str, Matcher[str]]) -> "WerkzeugResponseMatcher":
        """Matches if the response body text matches the given value or matcher.

        A synonym for :meth:`with_text`.

        :param text: The expected body text string or matcher.
        :return: Self, for chaining.
        """
        return self.with_text(text)

    def with_mimetype(self, mimetype: Union[str, Matcher[str]]) -> "WerkzeugResponseMatcher":
        """Matches if the response mimetype matches the given value or matcher.

        :param mimetype: The expected mimetype string or matcher.
        :return: Self, for chaining.
        """
        self.mimetype = wrap_matcher(mimetype)
        return self

    def and_mimetype(self, mimetype: Union[str, Matcher[str]]) -> "WerkzeugResponseMatcher":
        """Matches if the response mimetype matches the given value or matcher.

        A synonym for :meth:`with_mimetype`.

        :param mimetype: The expected mimetype string or matcher.
        :return: Self, for chaining.
        """
        return self.with_mimetype(mimetype)

    def with_json(self, json: Union[JsonStructure, Matcher[JsonStructure]]) -> "WerkzeugResponseMatcher":
        """Matches if the response JSON body matches the given value or matcher.

        The response body is parsed as JSON before matching.

        :param json: The expected JSON structure or matcher.
        :return: Self, for chaining.
        """
        self.json = wrap_matcher(json)
        return self

    def and_json(self, json: Union[JsonStructure, Matcher[JsonStructure]]) -> "WerkzeugResponseMatcher":
        """Matches if the response JSON body matches the given value or matcher.

        A synonym for :meth:`with_json`.

        :param json: The expected JSON structure or matcher.
        :return: Self, for chaining.
        """
        return self.with_json(json)

    def with_headers(
        self,
        headers: Union[Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]],
    ) -> "WerkzeugResponseMatcher":
        """Matches if the response headers match the given value or matcher.

        :param headers: The expected headers dictionary or matcher.
        :return: Self, for chaining.
        """
        self.headers = wrap_matcher(headers)
        return self

    def and_headers(
        self,
        headers: Union[Mapping[str, Union[str, Matcher[str]]], Matcher[Mapping[str, Union[str, Matcher[str]]]]],
    ) -> "WerkzeugResponseMatcher":
        """Matches if the response headers match the given value or matcher.

        A synonym for :meth:`with_headers`.

        :param headers: The expected headers dictionary or matcher.
        :return: Self, for chaining.
        """
        return self.with_headers(headers)


def redirects_to(url_matcher: Union[str, Matcher]) -> Matcher[Response]:
    """Matches if the Werkzeug response is a redirect to the specified URL.

    Checks if the status code is between 300 and 399 and the ``Location`` header matches.

    :param url_matcher: The expected URL string or matcher.
    :return: A matcher for redirect responses.
    """
    return described_as(
        str(StringDescription().append_text("redirects to ").append_description_of(url_matcher)),
        is_werkzeug_response().with_status_code(between(300, 399)).and_headers(has_entry("Location", url_matcher)),
    )
