# Copyright 2026 Simon Brunning
from __future__ import annotations

from pathlib import PurePath
from typing import TYPE_CHECKING, Any

from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

from brunns.matchers.utils import (
    append_matcher_description,
    describe_field_match,
    describe_field_mismatch,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from hamcrest.core.description import Description
    from hamcrest.core.matcher import Matcher

ANYTHING = anything()


class PathMatcher(BaseMatcher[PurePath]):
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

    def _fields(self, item: PurePath):
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

    def _matches(self, item: PurePath) -> bool:
        return all(matcher.matches(val) for matcher, _, val in self._fields(item))

    def describe_mismatch(self, item: PurePath, mismatch_description: Description) -> None:
        mismatch_description.append_text("was Path with")
        for matcher, name, val in self._fields(item):
            describe_field_mismatch(matcher, name, val, mismatch_description)

    def describe_match(self, item: PurePath, match_description: Description) -> None:
        match_description.append_text("was Path with")
        for matcher, name, val in self._fields(item):
            describe_field_match(matcher, name, val, match_description)

    def describe_to(self, description: Description) -> None:
        description.append_text("Path with")
        for matcher, name, _ in self._fields(PurePath()):
            append_matcher_description(matcher, name, description)

    def with_anchor(self, item: str | Matcher[str]) -> PathMatcher:
        """Matches the path's anchor (drive and root combined).

        :param item: Expected anchor string or a matcher for the anchor.
        :return: This matcher instance for chaining.
        """
        self.anchor = wrap_matcher(item)
        return self

    and_anchor = with_anchor

    def with_name(self, item: str | Matcher[str]) -> PathMatcher:
        """Matches the path's name (final component).

        :param item: Expected name string or a matcher for the name.
        :return: This matcher instance for chaining.
        """
        self.name = wrap_matcher(item)
        return self

    and_name = with_name

    def with_parent(self, item: Any | Matcher[Any]) -> PathMatcher:
        """Matches the path's parent directory.

        :param item: Expected parent path or a matcher for the parent.
        :return: This matcher instance for chaining.
        """
        self.parent = wrap_matcher(item)
        return self

    and_parent = with_parent

    def with_parents(self, item: Sequence[Any] | Matcher[Sequence[Any]]) -> PathMatcher:
        """Matches the path's sequence of parent directories.

        :param item: Expected sequence of parent paths or a matcher for ancestors.
        :return: This matcher instance for chaining.
        """
        self.parents = wrap_matcher(item)
        return self

    and_parents = with_parents

    def with_parts(self, item: Sequence[str] | Matcher[Sequence[str]]) -> PathMatcher:
        """Matches the path's component sequence.

        :param item: Expected sequence of path part strings or a matcher for them.
        :return: This matcher instance for chaining.
        """
        self.parts = wrap_matcher(item)
        return self

    and_parts = with_parts

    def with_root(self, item: str | Matcher[str]) -> PathMatcher:
        """Matches the path's root string.

        :param item: Expected root string or a matcher for the root.
        :return: This matcher instance for chaining.
        """
        self.root = wrap_matcher(item)
        return self

    and_root = with_root

    def with_stem(self, item: str | Matcher[str]) -> PathMatcher:
        """Matches the path's stem (final component without its extension).

        :param item: Expected stem string or a matcher for the stem.
        :return: This matcher instance for chaining.
        """
        self.stem = wrap_matcher(item)
        return self

    and_stem = with_stem

    def with_suffix(self, item: str | Matcher[str]) -> PathMatcher:
        """Matches the path's file suffix (extension).

        :param item: Expected suffix string or a matcher for the suffix.
        :return: This matcher instance for chaining.
        """
        self.suffix = wrap_matcher(item)
        return self

    and_suffix = with_suffix

    def with_suffixes(self, item: Sequence[str] | Matcher[Sequence[str]]) -> PathMatcher:
        """Matches the path's list of file suffixes (extensions).

        :param item: Expected sequence of suffix strings or a matcher for them.
        :return: This matcher instance for chaining.
        """
        self.suffixes = wrap_matcher(item)
        return self

    and_suffixes = with_suffixes


def is_path() -> PathMatcher:
    """Matches a :class:`pathlib.Path`.

    This function returns a :class:`PathMatcher` which can be refined using builder methods
    to match specific parts of the :class:`pathlib.Path` (e.g. ``.with_name(...)``, ``.with_suffix(...)``).

    :return: A matcher for :class:`pathlib.Path` objects.
    """
    return PathMatcher()
