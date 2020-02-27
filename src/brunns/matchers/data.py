# encoding=utf-8
import json
from typing import Any, Union

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

# JsonStructure = Union[MutableMapping[str, "JsonStructure"], Iterable["JsonStructure"], str, int, bool, None]
JsonStructure = Any  # TODO Pending a better solution to https://github.com/python/typing/issues/182


class JsonMatching(BaseMatcher[str]):
    def __init__(self, matcher: Union[Matcher[JsonStructure], JsonStructure]) -> None:
        self.matcher = wrap_matcher(matcher)  # type: Matcher[JsonStructure]

    def describe_to(self, description: Description) -> None:
        description.append_text("JSON structure matching ").append_description_of(self.matcher)

    def _matches(self, json_string: str) -> bool:
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


def json_matching(matcher: Union[Matcher[JsonStructure], JsonStructure]) -> JsonMatching:
    """Matches string containing JSON data.
    :param matcher: Expected JSON
    """
    return JsonMatching(matcher)
