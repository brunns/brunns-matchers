# encoding=utf-8
from typing import Mapping, Optional, Union

from brunns.matchers.base import GenericMatcher
from hamcrest import anything
from hamcrest.core.core.isanything import IsAnything
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher
from requests import Response

ANYTHING = anything()


def response_with(
    status_code: Union[int, Matcher] = ANYTHING,
    body: Union[str, Matcher] = ANYTHING,
    content: Union[str, Matcher] = ANYTHING,
    json: Union[str, Matcher] = ANYTHING,
    headers: Union[Mapping[str, str], Matcher] = ANYTHING,
) -> Matcher:
    """Matches :requests.models.Response:.
    :param status_code: Expected status code
    :param body: Expected body
    :param content: Expected content
    :param json: Expected json
    :param headers: Expected headers
    :return: Matcher
    """
    return ResponseMatcher(
        status_code=status_code, body=body, content=content, json=json, headers=headers
    )


class ResponseMatcher(GenericMatcher[Response]):
    def __init__(
        self,
        status_code: Union[int, Matcher] = ANYTHING,
        body: Union[str, Matcher] = ANYTHING,
        content: Union[str, Matcher] = ANYTHING,
        json: Union[str, Matcher] = ANYTHING,
        headers: Union[Mapping[str, str], Matcher] = ANYTHING,
    ) -> None:
        super(ResponseMatcher, self).__init__()
        self.status_code = wrap_matcher(status_code)
        self.body = wrap_matcher(body)
        self.content = wrap_matcher(content)
        self.json = wrap_matcher(json)
        self.headers = wrap_matcher(headers)

    def _matches(self, response: Response) -> bool:
        return (
            self.status_code.matches(response.status_code)
            and self.body.matches(response.text)
            and self.content.matches(response.content)
            and self.json.matches(self._get_response_json(response))
            and self.headers.matches(response.headers)
        )

    @staticmethod
    def _get_response_json(response: Response) -> Optional[str]:
        try:
            return response.json
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
        mismatch_description.append_text("was response with status code: ").append_description_of(
            response.status_code
        ).append_text(" body: ").append_description_of(response.text).append_text(
            " content: "
        ).append_description_of(
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
