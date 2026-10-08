# Copyright 2026 Simon Brunning
from pathlib import Path

from hamcrest import assert_that, contains_exactly, has_string, not_

from brunns.matchers.matcher import matches_with, mismatches_with
from brunns.matchers.path import is_path


def test_is_path():
    path = Path("/usr/bin/python3")

    should_match = is_path().with_parts(contains_exactly("/", "usr", "bin", "python3"))
    should_not_match = is_path().with_parts(contains_exactly("/", "foo", "bar", "baz"))

    assert_that(path, should_match)
    assert_that(path, not_(should_not_match))

    assert_that(
        should_match,
        has_string("Path with parts: a sequence containing ['/', 'usr', 'bin', 'python3']"),
    )
    assert_that(
        should_not_match,
        mismatches_with(path, "was Path with parts: item 1: was 'usr'"),
    )
    assert_that(
        should_match,
        matches_with(path, "was Path with parts: was <('/', 'usr', 'bin', 'python3')>"),
    )
