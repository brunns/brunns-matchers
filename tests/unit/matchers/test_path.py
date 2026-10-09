# Copyright 2026 Simon Brunning
import sys
from pathlib import Path

import pytest
from hamcrest import assert_that, contains_exactly, equal_to, has_string, not_
from pyfakefs.fake_filesystem import FakeFilesystem

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


def test_exists_matching(fs: FakeFilesystem):
    fs.create_file("/var/log/app.log")

    existing_file = Path("/var/log/app.log")
    nonexistant_file = Path("/var/log/app.json")

    file_matcher = is_path().which_exists()

    assert_that(existing_file, file_matcher)
    assert_that(nonexistant_file, not_(file_matcher))

    assert_that(
        file_matcher,
        has_string("Path with exists: <True>"),
    )
    assert_that(
        file_matcher,
        matches_with(
            existing_file,
            "was Path with exists: was <True>",
        ),
    )
    assert_that(
        file_matcher,
        mismatches_with(
            nonexistant_file,
            "was Path with exists: was <False>",
        ),
    )


def test_does_not_exist_matching(fs: FakeFilesystem):
    fs.create_file("/var/log/app.log")

    existing_file = Path("/var/log/app.log")
    nonexistant_file = Path("/var/log/app.json")

    file_matcher = is_path().which_does_not_exist()

    assert_that(nonexistant_file, file_matcher)
    assert_that(existing_file, not_(file_matcher))

    assert_that(
        file_matcher,
        has_string("Path with exists: <False>"),
    )
    assert_that(
        file_matcher,
        matches_with(
            nonexistant_file,
            "was Path with exists: was <False>",
        ),
    )
    assert_that(
        file_matcher,
        mismatches_with(
            existing_file,
            "was Path with exists: was <True>",
        ),
    )


def test_is_file_matching(fs: FakeFilesystem):
    fs.create_file("/var/log/app.log")
    fs.create_dir("/var/log/subdir")

    is_a_file = Path("/var/log/app.log")
    is_a_directory = Path("/var/log/subdir")

    file_matcher = is_path().which_is_a_file()

    assert_that(is_a_file, file_matcher)
    assert_that(is_a_directory, not_(file_matcher))

    assert_that(
        file_matcher,
        has_string("Path with is_file: <True>"),
    )
    assert_that(
        file_matcher,
        matches_with(
            is_a_file,
            "was Path with is_file: was <True>",
        ),
    )
    assert_that(
        file_matcher,
        mismatches_with(
            is_a_directory,
            "was Path with is_file: was <False>",
        ),
    )


def test_is_not_a_file_matching(fs: FakeFilesystem):
    fs.create_file("/var/log/app.log")
    fs.create_dir("/var/log/subdir")

    is_a_file = Path("/var/log/app.log")
    is_a_directory = Path("/var/log/subdir")

    file_matcher = is_path().which_is_not_a_file()

    assert_that(is_a_directory, file_matcher)
    assert_that(is_a_file, not_(file_matcher))

    assert_that(
        file_matcher,
        has_string("Path with is_file: <False>"),
    )
    assert_that(
        file_matcher,
        matches_with(
            is_a_directory,
            "was Path with is_file: was <False>",
        ),
    )
    assert_that(
        file_matcher,
        mismatches_with(
            is_a_file,
            "was Path with is_file: was <True>",
        ),
    )


def test_is_directory_matching(fs: FakeFilesystem):
    fs.create_file("/var/log/app.log")
    fs.create_dir("/var/log/subdir")

    is_a_file = Path("/var/log/app.log")
    is_a_directory = Path("/var/log/subdir")

    directory_matcher = is_path().which_is_a_directory()

    assert_that(is_a_directory, directory_matcher)
    assert_that(is_a_file, not_(directory_matcher))

    assert_that(
        directory_matcher,
        has_string("Path with is_directory: <True>"),
    )
    assert_that(
        directory_matcher,
        matches_with(
            is_a_directory,
            "was Path with is_directory: was <True>",
        ),
    )
    assert_that(
        directory_matcher,
        mismatches_with(
            is_a_file,
            "was Path with is_directory: was <False>",
        ),
    )


def test_is_not_a_directory_matching(fs: FakeFilesystem):
    fs.create_file("/var/log/app.log")
    fs.create_dir("/var/log/subdir")

    is_a_file = Path("/var/log/app.log")
    is_a_directory = Path("/var/log/subdir")

    directory_matcher = is_path().which_is_not_a_directory()

    assert_that(is_a_file, directory_matcher)
    assert_that(is_a_directory, not_(directory_matcher))

    assert_that(
        directory_matcher,
        has_string("Path with is_directory: <False>"),
    )
    assert_that(
        directory_matcher,
        matches_with(
            is_a_file,
            "was Path with is_directory: was <False>",
        ),
    )
    assert_that(
        directory_matcher,
        mismatches_with(
            is_a_directory,
            "was Path with is_directory: was <True>",
        ),
    )
