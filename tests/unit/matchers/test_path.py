# Copyright 2026 Simon Brunning
import sys
from pathlib import Path

import pytest
from hamcrest import assert_that, contains_exactly, equal_to, has_string, not_

from brunns.matchers.matcher import matches_with, mismatches_with
from brunns.matchers.path import is_path


@pytest.mark.skipif(sys.platform == "win32", reason="Paths are different on Windows")
def test_is_path():
    path = Path("/usr/bin/python3.tar.gz")

    should_match = (
        is_path()
        .with_parts(contains_exactly("/", "usr", "bin", "python3.tar.gz"))
        .and_name("python3.tar.gz")
        .and_stem("python3.tar")
        .and_suffix(".gz")
        .and_suffixes(contains_exactly(".tar", ".gz"))
        .and_parent(equal_to(Path("/usr/bin")))
        .and_parents(contains_exactly(Path("/usr/bin"), Path("/usr"), Path("/")))
        .and_root("/")
        .and_anchor("/")
    )

    should_not_match = (
        is_path()
        .with_name("python2.zip")
        .with_parts(contains_exactly("foo", "bar", "baz", "python2.zip"))
        .and_stem("python1")
        .and_suffix(".zip")
        .and_suffixes(contains_exactly(".tar", ".zip"))
        .and_parent(equal_to(Path("/foo/bar")))
        .and_parents(contains_exactly(Path("/foo/bar"), Path("/foo"), Path("/")))
        .and_root("")
        .and_anchor("c:")
    )

    assert_that(path, should_match)
    assert_that(path, not_(should_not_match))

    assert_that(
        should_match,
        has_string(
            "Path with anchor: '/' "
            "name: 'python3.tar.gz' "
            "parent: </usr/bin> "
            "parents: a sequence containing [</usr/bin>, </usr>, </>] "
            "parts: a sequence containing ['/', 'usr', 'bin', 'python3.tar.gz'] "
            "root: '/' "
            "stem: 'python3.tar' "
            "suffix: '.gz' "
            "suffixes: a sequence containing ['.tar', '.gz']"
        ),
    )
    assert_that(
        should_not_match,
        mismatches_with(
            path,
            "was Path with anchor: was '/' "
            "name: was 'python3.tar.gz' "
            "parent: was </usr/bin> "
            "parents: item 0: was </usr/bin> "
            "parts: item 0: was '/' "
            "root: was '/' "
            "stem: was 'python3.tar' "
            "suffix: was '.gz' "
            "suffixes: item 1: was '.gz'",
        ),
    )
    assert_that(
        should_match,
        matches_with(
            path,
            "was Path with anchor: was '/' "
            "name: was 'python3.tar.gz' "
            "parent: was </usr/bin> "
            "parents: was <PosixPath.parents> "  ## Ugly, but describe_match() is pretty niche, so not worth fixing.
            "parts: was <('/', 'usr', 'bin', 'python3.tar.gz')> "
            "root: was '/' "
            "stem: was 'python3.tar' "
            "suffix: was '.gz' "
            "suffixes: was <['.tar', '.gz']>",
        ),
    )


@pytest.mark.skipif(sys.platform == "win32", reason="Paths are different on Windows")
def test_is_path_from_string():
    path = "/usr/bin/python3.tar.gz"

    should_match = (
        is_path()
        .with_parts(contains_exactly("/", "usr", "bin", "python3.tar.gz"))
        .and_name("python3.tar.gz")
        .and_stem("python3.tar")
        .and_suffix(".gz")
        .and_suffixes(contains_exactly(".tar", ".gz"))
        .and_parent(equal_to(Path("/usr/bin")))
        .and_parents(contains_exactly(Path("/usr/bin"), Path("/usr"), Path("/")))
        .and_root("/")
        .and_anchor("/")
    )

    should_not_match = (
        is_path()
        .with_name("python2.zip")
        .with_parts(contains_exactly("foo", "bar", "baz", "python2.zip"))
        .and_stem("python1")
        .and_suffix(".zip")
        .and_suffixes(contains_exactly(".tar", ".zip"))
        .and_parent(equal_to(Path("/foo/bar")))
        .and_parents(contains_exactly(Path("/foo/bar"), Path("/foo"), Path("/")))
        .and_root("")
        .and_anchor("c:")
    )

    assert_that(path, should_match)
    assert_that(path, not_(should_not_match))

    assert_that(
        should_not_match,
        mismatches_with(
            path,
            "was Path with anchor: was '/' "
            "name: was 'python3.tar.gz' "
            "parent: was </usr/bin> "
            "parents: item 0: was </usr/bin> "
            "parts: item 0: was '/' "
            "root: was '/' "
            "stem: was 'python3.tar' "
            "suffix: was '.gz' "
            "suffixes: item 1: was '.gz'",
        ),
    )
    assert_that(
        should_match,
        matches_with(
            path,
            "was Path with anchor: was '/' "
            "name: was 'python3.tar.gz' "
            "parent: was </usr/bin> "
            "parents: was <PosixPath.parents> "
            "parts: was <('/', 'usr', 'bin', 'python3.tar.gz')> "
            "root: was '/' "
            "stem: was 'python3.tar' "
            "suffix: was '.gz' "
            "suffixes: was <['.tar', '.gz']>",
        ),
    )


def test_is_path_non_path_type():
    matcher = is_path().with_name("python3")

    assert_that(123, not_(matcher))
    assert_that(
        matcher,
        mismatches_with(123, "was invalid path <123>"),
    )
