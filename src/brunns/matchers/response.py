# encoding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

from hamcrest import equal_to, anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.core.isanything import IsAnything
from hamcrest.core.matcher import Matcher

ANYTHING = anything()


def response_with(status_code=ANYTHING, body=ANYTHING, content=ANYTHING, json=ANYTHING, headers=ANYTHING):
    """Matches :requests.models.Response:.
    :param status_code: Expected status code
    :type status_code: int or Matcher
    :param body: Expected body
    :type body: str or Matcher
    :param content: Expected content
    :type content: bytes or Matcher
    :param json: Expected json
    :type json: Matcher or dict or list
    :param headers: Expected headers
    :type headers: dict or Matcher
    :return: Matcher
    :rtype: Matcher(requests.models.Response)
    """
    return ResponseMatcher(status_code=status_code, body=body, content=content, json=json, headers=headers)


class ResponseMatcher(BaseMatcher):
    def __init__(self, status_code=ANYTHING, body=ANYTHING, content=ANYTHING, json=ANYTHING, headers=ANYTHING):
        super(ResponseMatcher, self).__init__()
        self.status_code = status_code if isinstance(status_code, Matcher) else equal_to(status_code)
        self.body = body if isinstance(body, Matcher) else equal_to(body)
        self.content = content if isinstance(content, Matcher) else equal_to(content)
        self.json = json if isinstance(json, Matcher) else equal_to(json)
        self.headers = headers if isinstance(headers, Matcher) else equal_to(headers)

    def _matches(self, response):
        return (
            self.status_code.matches(response.status_code)
            and self.body.matches(response.text)
            and self.content.matches(response.content)
            and self.json.matches(self._get_response_json(response))
            and self.headers.matches(response.headers)
        )

    @staticmethod
    def _get_response_json(response):
        try:
            return response.json
        except ValueError:
            return None

    def describe_to(self, description):
        description.append_text("response with")
        self._optional_description(description)

    def _optional_description(self, description):
        self._append_matcher_descrption(description, self.status_code, "status_code")
        self._append_matcher_descrption(description, self.body, "body")
        self._append_matcher_descrption(description, self.content, "content")
        self._append_matcher_descrption(description, self.json, "json")
        self._append_matcher_descrption(description, self.headers, "headers")

    def _append_matcher_descrption(self, description, matcher, text):
        if not isinstance(matcher, IsAnything):
            description.append_text(" {0}: ".format(text)).append_description_of(matcher)

    def describe_mismatch(self, response, mismatch_description):
        mismatch_description.append_text("was response with status code: ").append_description_of(
            response.status_code
        ).append_text(" body: ").append_description_of(response.text).append_text(" content: ").append_description_of(
            response.content
        ).append_text(
            " json: "
        ).append_description_of(
            self._get_response_json(response)
        ).append_text(
            " headers: "
        ).append_description_of(
            response.headers
        )
