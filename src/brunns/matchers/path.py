# Copyright 2026 Simon Brunning
from collections.abc import Sequence
from pathlib import Path

from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

from brunns.matchers.utils import append_matcher_description, describe_field_match, describe_field_mismatch

ANYTHING = anything()


class PathMatcher(BaseMatcher[Path]):
    def __init__(self) -> None:
        super().__init__()
        self.parts: Matcher[Sequence[str]] = ANYTHING

    def _matches(self, item: Path) -> bool:
        return self.parts.matches(item.parts)

    def describe_mismatch(self, item: Path, mismatch_description: Description) -> None:
        mismatch_description.append_text("was Path with")
        describe_field_mismatch(self.parts, "parts", item.parts, mismatch_description)

    def describe_match(self, item: Path, match_description: Description) -> None:
        match_description.append_text("was Path with")
        describe_field_match(self.parts, "parts", item.parts, match_description)

    def describe_to(self, description: Description) -> None:
        description.append_text("Path with")
        append_matcher_description(self.parts, "parts", description)

    def with_parts(self, item: Sequence[str] | Matcher[Sequence[str]]):
        self.parts = wrap_matcher(item)
        return self


def is_path() -> PathMatcher:
    return PathMatcher()
