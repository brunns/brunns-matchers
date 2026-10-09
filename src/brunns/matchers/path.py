# Copyright 2026 Simon Brunning
from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from hamcrest import anything, is_
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

logger = logging.getLogger(__name__)
ANYTHING = anything()


class PathMatcher(BaseMatcher[Path | str]):
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
        self.exists: Matcher[bool] = ANYTHING
        self.is_file: Matcher[bool] = ANYTHING
        self.is_directory: Matcher[bool] = ANYTHING

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

    def _to_path(self, item: Any) -> Path | None:
        try:
            return Path(item)
        except (TypeError, ValueError):
            return None

    def _matches(self, item: Path | str) -> bool:
        path = self._to_path(item)
        if path is None:
            return False
        return (
            all(matcher.matches(val) for matcher, _, val in self._fields(path))
            and self.exists.matches(path.exists())
            and self.is_file.matches(path.is_file())
            and self.is_directory.matches(path.is_dir())
        )

    def describe_mismatch(self, item: Path | str, mismatch_description: Description) -> None:
        path = self._to_path(item)
        if path is None:
            mismatch_description.append_text("was invalid path ").append_description_of(item)
            return
        mismatch_description.append_text("was Path with")
        for matcher, name, val in self._fields(path):
            describe_field_mismatch(matcher, name, val, mismatch_description)
        describe_field_mismatch(self.exists, "exists", path.exists(), mismatch_description)
        describe_field_mismatch(self.is_file, "is_file", path.is_file(), mismatch_description)
        describe_field_mismatch(self.is_directory, "is_directory", path.is_dir(), mismatch_description)

    def describe_match(self, item: Path | str, match_description: Description) -> None:
        path = self._to_path(item)
        if path is None:  # pragma: no cover
            logger.error("We should not have matched an invalid path.")
            match_description.append_text("was invalid path ").append_description_of(item)
            return
        match_description.append_text("was Path with")
        for matcher, name, val in self._fields(path):
            describe_field_match(matcher, name, val, match_description)
        describe_field_match(self.exists, "exists", path.exists(), match_description)
        describe_field_match(self.is_file, "is_file", path.is_file(), match_description)
        describe_field_match(self.is_directory, "is_directory", path.is_dir(), match_description)

    def describe_to(self, description: Description) -> None:
        description.append_text("Path with")
        for matcher, name, _ in self._fields(Path()):
            append_matcher_description(matcher, name, description)
        append_matcher_description(self.exists, "exists", description)
        append_matcher_description(self.is_file, "is_file", description)
        append_matcher_description(self.is_directory, "is_directory", description)

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

    def which_exists(self) -> PathMatcher:
        """Matches that the path exists on the filesystem.

        :return: This matcher instance for chaining.
        """
        self.exists = is_(True)
        return self

    and_which_exists = which_exists

    def which_does_not_exist(self) -> PathMatcher:
        """Matches that the path does not exist on the filesystem.

        :return: This matcher instance for chaining.
        """
        self.exists = is_(False)
        return self

    and_which_does_not_exist = which_does_not_exist

    def which_is_a_file(self) -> PathMatcher:
        """Matches that the path is a regular file.

        :return: This matcher instance for chaining.
        """
        self.is_file = is_(True)
        return self

    and_is_a_file = which_is_a_file

    def which_is_not_a_file(self) -> PathMatcher:
        """Matches that the path is not a regular file.

        :return: This matcher instance for chaining.
        """
        self.is_file = is_(False)
        return self

    and_is_not_a_file = which_is_not_a_file

    def which_is_a_directory(self) -> PathMatcher:
        """Matches that the path is a directory.

        :return: This matcher instance for chaining.
        """
        self.is_directory = is_(True)
        return self

    and_is_a_directory = which_is_a_directory

    def which_is_not_a_directory(self) -> PathMatcher:
        """Matches that the path is not a directory.

        :return: This matcher instance for chaining.
        """
        self.is_directory = is_(False)
        return self

    and_is_not_a_directory = which_is_not_a_directory


def is_path() -> PathMatcher:
    """Matches a :class:`pathlib.Path` or string filepath.

    This function returns a :class:`PathMatcher` which can be refined using builder methods
    to match specific parts of the :class:`pathlib.Path` (e.g. ``.with_name(...)``, ``.with_suffix(...)``).

    :return: A matcher for :class:`pathlib.Path` objects or string filepaths.
    """
    return PathMatcher()
