from __future__ import annotations

import json
from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING, TypeAlias

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

if TYPE_CHECKING:
    from hamcrest.core.description import Description
    from hamcrest.core.matcher import Matcher

JsonObject: TypeAlias = Mapping[str, "JsonValue"]
JsonValue: TypeAlias = str | int | float | bool | None | Sequence["JsonValue"] | JsonObject


class JsonMatching(BaseMatcher[str]):
    """Matches string containing JSON data.

    :param matcher: Value to match against deserialised JSON.
    """

    def __init__(self, matcher: JsonValue | Matcher[JsonValue]) -> None:
        self.matcher: Matcher[JsonValue] = wrap_matcher(matcher)

    def describe_to(self, description: Description) -> None:
        description.append_text("JSON structure matching ").append_description_of(self.matcher)

    def _matches(self, json_string: str) -> bool:
        try:
            loads: JsonValue = json.loads(json_string)
        except ValueError:
            return False
        return self.matcher.matches(loads)

    def describe_mismatch(self, json_string: str, description: Description) -> None:
        try:
            loads: JsonValue = json.loads(json_string)
        except ValueError:
            description.append_text("Got invalid JSON ").append_description_of(json_string)
        else:
            self.matcher.describe_mismatch(loads, description)


def json_matching(matcher: Matcher[JsonValue] | JsonValue) -> JsonMatching:
    """Matches string containing JSON data.

    :param matcher: Value to match against deserialised JSON.
    """
    return JsonMatching(matcher)
