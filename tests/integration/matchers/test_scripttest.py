"""Integration tests for scripttest matchers using real commands."""

import platform
import textwrap

import pytest
from hamcrest import assert_that, contains_string, has_key, not_
from scripttest import TestFileEnvironment

from brunns.matchers.scripttest import is_proc_result

# scripttest doesn't track file changes properly on Windows
skipif_windows = pytest.mark.skipif(
    platform.system() == "Windows", reason="scripttest file tracking not supported on Windows"
)


@pytest.fixture
def test_env(tmp_path):
    """Create a TestFileEnvironment for running commands."""
    return TestFileEnvironment(str(tmp_path / "test-output"))


def test_proc_result_with_successful_command(test_env):
    # Given / When
    result = test_env.run("python", "-c", "print('hello world')", expect_error=False)

    # Then
    assert_that(
        result,
        is_proc_result().with_returncode(0).and_stdout(contains_string("hello world")).and_stderr(""),
    )


def test_proc_result_with_failing_command(test_env):
    # Given / When
    result = test_env.run("python", "-c", "import sys; sys.exit(1)", expect_error=True)

    # Then
    assert_that(
        result,
        is_proc_result().with_returncode(1),
    )
    assert_that(
        result,
        not_(is_proc_result().with_returncode(0)),
    )


def test_proc_result_with_stderr_output(test_env):
    # Given / When
    result = test_env.run(
        "python",
        "-c",
        "import sys; sys.stderr.write('error message\\n')",
        expect_error=False,
        expect_stderr=True,
    )

    # Then
    assert_that(
        result,
        is_proc_result().with_returncode(0).and_stderr(contains_string("error message")),
    )


@skipif_windows
def test_proc_result_with_file_creation(test_env):
    # Given
    script_content = textwrap.dedent("""
        with open('output.txt', 'w') as f:
            f.write('test content')
    """)

    # When
    result = test_env.run("python", "-c", script_content)

    # Then
    assert_that(
        result,
        is_proc_result().with_returncode(0).and_files_created(has_key("output.txt")),
    )


@skipif_windows
def test_proc_result_with_file_modification(test_env):
    # Given - create a file first
    test_env.writefile("config.txt", b"initial content")

    script_content = textwrap.dedent("""
        with open('config.txt', 'a') as f:
            f.write('\\nadditional content')
    """)

    # When
    result = test_env.run("python", "-c", script_content, cwd=test_env.base_path)

    # Then
    assert_that(
        result,
        is_proc_result().with_returncode(0).and_files_updated(has_key("config.txt")),
    )


@skipif_windows
def test_proc_result_with_multiple_files(test_env):
    # Given
    script_content = textwrap.dedent("""
        with open('file1.txt', 'w') as f:
            f.write('content1')
        with open('file2.txt', 'w') as f:
            f.write('content2')
    """)

    # When
    result = test_env.run("python", "-c", script_content)

    # Then
    assert_that(
        result,
        is_proc_result()
        .with_returncode(0)
        .and_files_created(has_key("file1.txt"))
        .and_files_created(has_key("file2.txt")),
    )


def test_proc_result_with_command_args(test_env):
    # Given / When
    result = test_env.run("python", "--version")

    # Then
    # Check that args are recorded (exact format may vary by Python version)
    assert_that(
        result,
        is_proc_result().with_returncode(0),
    )
    # Verify args attribute exists and contains python
    assert len(result.args) > 0
    assert "python" in str(result.args[0]).lower()


def test_proc_result_empty_files_dicts(test_env):
    # Given / When - run a command that doesn't touch any files
    result = test_env.run("python", "-c", "print('no files')")

    # Then
    assert_that(
        result,
        is_proc_result()
        .with_returncode(0)
        .and_stdout(contains_string("no files"))
        .and_files_created({})
        .and_files_deleted({})
        .and_files_updated({}),
    )


@skipif_windows
def test_proc_result_chained_matchers(test_env):
    # Given
    script_content = textwrap.dedent("""
        import sys
        print('Success!')
        sys.stderr.write('Warning\\n')
        with open('result.log', 'w') as f:
            f.write('Done')
    """)

    # When
    result = test_env.run("python", "-c", script_content, expect_stderr=True)

    # Then - test full chaining
    assert_that(
        result,
        is_proc_result()
        .with_returncode(0)
        .and_stdout(contains_string("Success"))
        .and_stderr(contains_string("Warning"))
        .and_files_created(has_key("result.log")),
    )
