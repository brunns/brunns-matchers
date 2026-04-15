from __future__ import annotations

import json
from typing import TYPE_CHECKING, TypeAlias

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

if TYPE_CHECKING:
    from hamcrest.core.description import Description
    from hamcrest.core.matcher import Matcher

JsonStructure: TypeAlias = str | int | float | bool | None | list["JsonStructure"] | dict[str, "JsonStructure"]


class JsonMatching(BaseMatcher[str]):
    """Matches string containing JSON data.

    :param matcher: Value to match against deserialised JSON.
    """

    def __init__(self, matcher: JsonStructure | Matcher[JsonStructure]) -> None:
        self.matcher: Matcher[JsonStructure] = wrap_matcher(matcher)

    def describe_to(self, description: Description) -> None:
        description.append_text("JSON structure matching ").append_description_of(self.matcher)

    def _matches(self, json_string: str) -> bool:
        try:
            loads: JsonStructure = json.loads(json_string)
        except ValueError:
            return False
        return self.matcher.matches(loads)

    def describe_mismatch(self, json_string: str, description: Description) -> None:
        try:
            loads: JsonStructure = json.loads(json_string)
        except ValueError:
            description.append_text("Got invalid JSON ").append_description_of(json_string)
        else:
            self.matcher.describe_mismatch(loads, description)


def json_matching(matcher: Matcher[JsonStructure] | JsonStructure) -> JsonMatching:
    """Matches string containing JSON data.

    :param matcher: Value to match against deserialised JSON.
    """
    return JsonMatching(matcher)
