"""Unit tests for scripttest matchers."""

from unittest import mock

from hamcrest import (
    assert_that,
    contains_exactly,
    contains_string,
    has_entries,
    has_key,
    has_string,
    not_,
)

from brunns.matchers.matcher import matches_with, mismatches_with
from brunns.matchers.scripttest import is_proc_result

# Create a mock ProcResult for testing
MOCK_PROC_RESULT = mock.MagicMock(
    returncode=0,
    stdout="test output\n",
    stderr="",
    args=["script.py", "arg1", "arg2"],
    stdin=b"input data",
    files_created={"output.txt": mock.MagicMock(), "result.log": mock.MagicMock()},
    files_deleted={},
    files_updated={"config.ini": mock.MagicMock()},
)


def test_proc_result_matcher_returncode():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When

    # Then
    assert_that(proc_result, is_proc_result().with_returncode(0))
    assert_that(proc_result, not_(is_proc_result().with_returncode(1)))
    assert_that(is_proc_result().with_returncode(0), has_string("proc result with return code: <0>"))
    assert_that(
        is_proc_result().with_returncode(1),
        mismatches_with(proc_result, contains_string("was proc result with return code: was <0>")),
    )
    assert_that(
        is_proc_result().with_returncode(0),
        matches_with(proc_result, contains_string("was proc result with return code: was <0>")),
    )


def test_proc_result_matcher_stdout():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When

    # Then
    assert_that(proc_result, is_proc_result().with_stdout("test output\n"))
    assert_that(proc_result, not_(is_proc_result().with_stdout("different output")))
    assert_that(
        is_proc_result().with_stdout("test output\n"),
        has_string("proc result with stdout: 'test output\\n'"),
    )
    assert_that(
        is_proc_result().with_stdout("different output"),
        mismatches_with(proc_result, contains_string("was proc result with stdout: was 'test output\\n'")),
    )
    assert_that(
        is_proc_result().with_stdout("test output\n"),
        matches_with(proc_result, contains_string("was proc result with stdout: was 'test output\\n'")),
    )


def test_proc_result_matcher_stdout_with_matcher():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When

    # Then
    assert_that(proc_result, is_proc_result().with_stdout(contains_string("test output")))
    assert_that(proc_result, not_(is_proc_result().with_stdout(contains_string("error"))))


def test_proc_result_matcher_stderr():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When

    # Then
    assert_that(proc_result, is_proc_result().with_stderr(""))
    assert_that(proc_result, not_(is_proc_result().with_stderr("error message")))
    assert_that(
        is_proc_result().with_stderr(""),
        has_string("proc result with stderr: ''"),
    )
    assert_that(
        is_proc_result().with_stderr("error message"),
        mismatches_with(proc_result, contains_string("was proc result with stderr: was ''")),
    )
    assert_that(
        is_proc_result().with_stderr(""),
        matches_with(proc_result, contains_string("was proc result with stderr: was ''")),
    )


def test_proc_result_matcher_args():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When

    # Then
    assert_that(proc_result, is_proc_result().with_args(["script.py", "arg1", "arg2"]))
    assert_that(proc_result, not_(is_proc_result().with_args(["different.py"])))
    assert_that(
        str(is_proc_result().with_args(["script.py", "arg1", "arg2"])),
        contains_string("proc result with args: <['script.py', 'arg1', 'arg2']>"),
    )
    assert_that(
        is_proc_result().with_args(["different.py"]),
        mismatches_with(proc_result, contains_string("was proc result with args: was <['script.py', 'arg1', 'arg2']>")),
    )
    assert_that(
        is_proc_result().with_args(["script.py", "arg1", "arg2"]),
        matches_with(proc_result, contains_string("was proc result with args: was <['script.py', 'arg1', 'arg2']>")),
    )


def test_proc_result_matcher_args_with_matcher():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When

    # Then
    assert_that(proc_result, is_proc_result().with_args(contains_exactly("script.py", "arg1", "arg2")))
    assert_that(proc_result, not_(is_proc_result().with_args(contains_exactly("script.py"))))


def test_proc_result_matcher_stdin():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When

    # Then
    assert_that(proc_result, is_proc_result().with_stdin(b"input data"))
    assert_that(proc_result, not_(is_proc_result().with_stdin(b"different input")))
    assert_that(
        str(is_proc_result().with_stdin(b"input data")),
        contains_string("proc result with stdin: <b'input data'>"),
    )
    assert_that(
        is_proc_result().with_stdin(b"different input"),
        mismatches_with(proc_result, contains_string("was proc result with stdin: was <b'input data'>")),
    )
    assert_that(
        is_proc_result().with_stdin(b"input data"),
        matches_with(proc_result, contains_string("was proc result with stdin: was <b'input data'>")),
    )


def test_proc_result_matcher_files_created():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When

    # Then
    assert_that(proc_result, is_proc_result().with_files_created(has_key("output.txt")))
    assert_that(proc_result, not_(is_proc_result().with_files_created(has_key("nonexistent.txt"))))
    assert_that(
        str(is_proc_result().with_files_created(has_key("output.txt"))),
        contains_string("proc result with files created: a dictionary containing key 'output.txt'"),
    )
    assert_that(
        is_proc_result().with_files_created(has_key("nonexistent.txt")),
        mismatches_with(
            proc_result,
            contains_string("was proc result with files created: was <"),
        ),
    )
    assert_that(
        is_proc_result().with_files_created(has_key("output.txt")),
        matches_with(
            proc_result,
            contains_string("was proc result with files created: was <"),
        ),
    )


def test_proc_result_matcher_files_deleted():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When

    # Then
    assert_that(proc_result, is_proc_result().with_files_deleted({}))
    assert_that(proc_result, not_(is_proc_result().with_files_deleted(has_key("some_file.txt"))))


def test_proc_result_matcher_files_updated():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When

    # Then
    assert_that(proc_result, is_proc_result().with_files_updated(has_key("config.ini")))
    assert_that(proc_result, not_(is_proc_result().with_files_updated(has_key("nonexistent.ini"))))


def test_proc_result_matcher_builder():
    # Given
    proc_result = MOCK_PROC_RESULT
    matcher = (
        is_proc_result()
        .with_returncode(0)
        .and_stdout(contains_string("output"))
        .and_stderr("")
        .and_args(contains_exactly("script.py", "arg1", "arg2"))
        .and_stdin(b"input data")
        .and_files_created(has_entries({"output.txt": mock.ANY, "result.log": mock.ANY}))
        .and_files_deleted({})
        .and_files_updated(has_key("config.ini"))
    )
    mismatcher = is_proc_result().with_returncode(1).and_stdout("wrong output")

    # When

    # Then
    assert_that(proc_result, matcher)
    assert_that(proc_result, not_(mismatcher))
    # Check that the string representation contains expected parts
    matcher_str = str(matcher)
    assert_that(matcher_str, contains_string("proc result with"))
    assert_that(matcher_str, contains_string("return code: <0>"))
    assert_that(matcher_str, contains_string("stdout: a string containing 'output'"))
    assert_that(matcher_str, contains_string("stderr: ''"))
    assert_that(matcher_str, contains_string("files created: a dictionary containing"))
    assert_that(
        mismatcher,
        mismatches_with(
            proc_result,
            contains_string("was proc result with return code: was <0> stdout: was 'test output\\n'"),
        ),
    )
    assert_that(
        matcher,
        matches_with(
            proc_result,
            contains_string("was proc result with return code: was <0> stdout: was 'test output\\n'"),
        ),
    )


def test_proc_result_matcher_and_synonyms():
    # Given
    proc_result = MOCK_PROC_RESULT

    # When
    matcher = (
        is_proc_result()
        .and_returncode(0)
        .and_stdout(contains_string("output"))
        .and_stderr("")
        .and_args(contains_exactly("script.py", "arg1", "arg2"))
        .and_stdin(b"input data")
        .and_files_created(has_key("output.txt"))
        .and_files_deleted({})
        .and_files_updated(has_key("config.ini"))
    )

    # Then
    assert_that(proc_result, matcher)
