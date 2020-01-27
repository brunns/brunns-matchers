# encoding=utf-8
import json
from typing import Mapping, Sequence, Union

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

JSON = Union[Sequence["JSON"], Mapping[str, "JSON"], str, int, bool]


class JsonMatching(BaseMatcher[str]):
    def __init__(self, matcher: Union[Matcher, JSON]) -> None:
        self.matcher = wrap_matcher(matcher)

    def describe_to(self, description: Description) -> None:
        description.append_text("JSON structure matching ").append_description_of(self.matcher)

    def _matches(self, json_string) -> bool:
        try:
            loads = json.loads(json_string)
        except ValueError:
            return False
        return self.matcher.matches(loads)

    def describe_mismatch(self, json_string: str, description: Description) -> None:
        try:
            loads = json.loads(json_string)
        except ValueError:
            description.append_text("Got invalid JSON ").append_description_of(json_string)
        else:
            self.matcher.describe_mismatch(loads, description)


def json_matching(matcher: Union[Matcher, JSON]) -> JsonMatching:
    """Matches string containing JSON data.
    :param matcher: Expected JSON
    """
    return JsonMatching(matcher)
