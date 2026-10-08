# Copyright 2026 Simon Brunning
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Self

from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

from brunns.matchers.utils import (
    append_matcher_description,
    describe_field_match,
    describe_field_mismatch,
)

ANYTHING = anything()


class PathMatcher(BaseMatcher[Path]):
    def __init__(self) -> None:
        super().__init__()
        self.anchor: Matcher[str] = ANYTHING
        self.name: Matcher[str] = ANYTHING
        self.parent: Matcher[Any] = ANYTHING
        self.parents: Matcher[Sequence[Any]] = ANYTHING
        self.parts: Matcher[Sequence[str]] = ANYTHING
        self.root: Matcher[str] = ANYTHING
        self.stem: Matcher[str] = ANYTHING
        self.suffix: Matcher[str] = ANYTHING
        self.suffixes: Matcher[Sequence[str]] = ANYTHING

    def _fields(self, item: Path):
        return [
            (self.anchor, "anchor", item.anchor),
            (self.name, "name", item.name),
            (self.parent, "parent", item.parent),
            (self.parents, "parents", item.parents),
            (self.parts, "parts", item.parts),
            (self.root, "root", item.root),
            (self.stem, "stem", item.stem),
            (self.suffix, "suffix", item.suffix),
            (self.suffixes, "suffixes", item.suffixes),
        ]

    def _matches(self, item: Path) -> bool:
        return all(matcher.matches(val) for matcher, _, val in self._fields(item))

    def describe_mismatch(self, item: Path, mismatch_description: Description) -> None:
        mismatch_description.append_text("was Path with")
        for matcher, name, val in self._fields(item):
            describe_field_mismatch(matcher, name, val, mismatch_description)

    def describe_match(self, item: Path, match_description: Description) -> None:
        match_description.append_text("was Path with")
        for matcher, name, val in self._fields(item):
            describe_field_match(matcher, name, val, match_description)

    def describe_to(self, description: Description) -> None:
        description.append_text("Path with")
        for matcher, name, _ in self._fields(Path()):
            append_matcher_description(matcher, name, description)

    def with_anchor(self, item: str | Matcher[str]) -> Self:
        self.anchor = wrap_matcher(item)
        return self

    and_anchor = with_anchor

    def with_name(self, item: str | Matcher[str]) -> Self:
        self.name = wrap_matcher(item)
        return self

    and_name = with_name

    def with_parent(self, item: Any | Matcher[Any]) -> Self:
        self.parent = wrap_matcher(item)
        return self

    and_parent = with_parent

    def with_parents(self, item: Sequence[Any] | Matcher[Sequence[Any]]) -> Self:
        self.parents = wrap_matcher(item)
        return self

    and_parents = with_parents

    def with_parts(self, item: Sequence[str] | Matcher[Sequence[str]]) -> Self:
        self.parts = wrap_matcher(item)
        return self

    and_parts = with_parts

    def with_root(self, item: str | Matcher[str]) -> Self:
        self.root = wrap_matcher(item)
        return self

    and_root = with_root

    def with_stem(self, item: str | Matcher[str]) -> Self:
        self.stem = wrap_matcher(item)
        return self

    and_stem = with_stem

    def with_suffix(self, item: str | Matcher[str]) -> Self:
        self.suffix = wrap_matcher(item)
        return self

    and_suffix = with_suffix

    def with_suffixes(self, item: Sequence[str] | Matcher[Sequence[str]]) -> Self:
        self.suffixes = wrap_matcher(item)
        return self

    and_suffixes = with_suffixes


def is_path() -> PathMatcher:
    """Matches a :class:`pathlib.Path`.

    This function returns a :class:`PathWith` matcher which can be refined using builder methods
    to match specific parts of the :class:`pathlib.Path` (e.g. ``.with_name(...)``, ``.with_suffix(...)``).

    :return: A matcher for :class:`pathlib.Path` objects.
    """
    return PathMatcher()
