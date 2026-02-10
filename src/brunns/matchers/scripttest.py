"""PyHamcrest matchers for scripttest ProcResult objects."""

from collections.abc import Mapping, Sequence
from typing import Any

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


def is_proc_result() -> "ProcResultMatcher":
    """Matches a ``scripttest.ProcResult`` object.

    This function returns a :class:`ProcResultMatcher` which can be refined using builder methods
    (e.g. ``.with_returncode(0)``).

    :return: A matcher for scripttest ProcResult objects.
    """
    return ProcResultMatcher()


class ProcResultMatcher(BaseMatcher[Any]):
    """Matches :class:`scripttest.ProcResult`.

    :param returncode: Expected return code (exit code).
    :param stdout: Expected standard output text.
    :param stderr: Expected standard error text.
    :param args: Expected command arguments.
    :param stdin: Expected standard input bytes.
    :param files_created: Expected files created dictionary.
    :param files_deleted: Expected files deleted dictionary.
    :param files_updated: Expected files updated dictionary.
    """

    def __init__(
        self,
        returncode: int | Matcher[int] = ANYTHING,
        stdout: str | Matcher[str] = ANYTHING,
        stderr: str | Matcher[str] = ANYTHING,
        args: Sequence[str] | Matcher[Sequence[str]] = ANYTHING,
        stdin: bytes | Matcher[bytes] = ANYTHING,
        files_created: Mapping[str, Any] | Matcher[Mapping[str, Any]] = ANYTHING,
        files_deleted: Mapping[str, Any] | Matcher[Mapping[str, Any]] = ANYTHING,
        files_updated: Mapping[str, Any] | Matcher[Mapping[str, Any]] = ANYTHING,
    ) -> None:
        super().__init__()
        self.returncode: Matcher[int] = wrap_matcher(returncode)
        self.stdout: Matcher[str] = wrap_matcher(stdout)
        self.stderr: Matcher[str] = wrap_matcher(stderr)
        self.args: Matcher[Sequence[str]] = wrap_matcher(args)
        self.stdin: Matcher[bytes] = wrap_matcher(stdin)
        self.files_created: Matcher[Mapping[str, Any]] = wrap_matcher(files_created)
        self.files_deleted: Matcher[Mapping[str, Any]] = wrap_matcher(files_deleted)
        self.files_updated: Matcher[Mapping[str, Any]] = wrap_matcher(files_updated)

    def _matches(self, proc_result: Any) -> bool:
        return (
            self.returncode.matches(proc_result.returncode)
            and self.stdout.matches(proc_result.stdout)
            and self.stderr.matches(proc_result.stderr)
            and self.args.matches(proc_result.args)
            and self.stdin.matches(proc_result.stdin)
            and self.files_created.matches(proc_result.files_created)
            and self.files_deleted.matches(proc_result.files_deleted)
            and self.files_updated.matches(proc_result.files_updated)
        )

    def describe_to(self, description: Description) -> None:
        description.append_text("proc result with")
        append_matcher_description(self.returncode, "return code", description)
        append_matcher_description(self.stdout, "stdout", description)
        append_matcher_description(self.stderr, "stderr", description)
        append_matcher_description(self.args, "args", description)
        append_matcher_description(self.stdin, "stdin", description)
        append_matcher_description(self.files_created, "files created", description)
        append_matcher_description(self.files_deleted, "files deleted", description)
        append_matcher_description(self.files_updated, "files updated", description)

    def describe_mismatch(self, proc_result: Any, mismatch_description: Description) -> None:
        mismatch_description.append_text("was proc result with")
        describe_field_mismatch(self.returncode, "return code", proc_result.returncode, mismatch_description)
        describe_field_mismatch(self.stdout, "stdout", proc_result.stdout, mismatch_description)
        describe_field_mismatch(self.stderr, "stderr", proc_result.stderr, mismatch_description)
        describe_field_mismatch(self.args, "args", proc_result.args, mismatch_description)
        describe_field_mismatch(self.stdin, "stdin", proc_result.stdin, mismatch_description)
        describe_field_mismatch(self.files_created, "files created", proc_result.files_created, mismatch_description)
        describe_field_mismatch(self.files_deleted, "files deleted", proc_result.files_deleted, mismatch_description)
        describe_field_mismatch(self.files_updated, "files updated", proc_result.files_updated, mismatch_description)

    def describe_match(self, proc_result: Any, match_description: Description) -> None:
        match_description.append_text("was proc result with")
        describe_field_match(self.returncode, "return code", proc_result.returncode, match_description)
        describe_field_match(self.stdout, "stdout", proc_result.stdout, match_description)
        describe_field_match(self.stderr, "stderr", proc_result.stderr, match_description)
        describe_field_match(self.args, "args", proc_result.args, match_description)
        describe_field_match(self.stdin, "stdin", proc_result.stdin, match_description)
        describe_field_match(self.files_created, "files created", proc_result.files_created, match_description)
        describe_field_match(self.files_deleted, "files deleted", proc_result.files_deleted, match_description)
        describe_field_match(self.files_updated, "files updated", proc_result.files_updated, match_description)

    def with_returncode(self, returncode: int | Matcher[int]):
        """Matches if the return code matches the given value or matcher.

        :param returncode: The expected return code (e.g. 0) or a matcher.
        :return: Self, for chaining.
        """
        self.returncode = wrap_matcher(returncode)
        return self

    def and_returncode(self, returncode: int | Matcher[int]):
        """Matches if the return code matches the given value or matcher.

        A synonym for :meth:`with_returncode`.

        :param returncode: The expected return code.
        :return: Self, for chaining.
        """
        return self.with_returncode(returncode)

    def with_stdout(self, stdout: str | Matcher[str]):
        """Matches if the stdout text matches the given value or matcher.

        :param stdout: The expected stdout string or matcher.
        :return: Self, for chaining.
        """
        self.stdout = wrap_matcher(stdout)
        return self

    def and_stdout(self, stdout: str | Matcher[str]):
        """Matches if the stdout text matches the given value or matcher.

        A synonym for :meth:`with_stdout`.

        :param stdout: The expected stdout string or matcher.
        :return: Self, for chaining.
        """
        return self.with_stdout(stdout)

    def with_stderr(self, stderr: str | Matcher[str]):
        """Matches if the stderr text matches the given value or matcher.

        :param stderr: The expected stderr string or matcher.
        :return: Self, for chaining.
        """
        self.stderr = wrap_matcher(stderr)
        return self

    def and_stderr(self, stderr: str | Matcher[str]):
        """Matches if the stderr text matches the given value or matcher.

        A synonym for :meth:`with_stderr`.

        :param stderr: The expected stderr string or matcher.
        :return: Self, for chaining.
        """
        return self.with_stderr(stderr)

    def with_args(self, args: Sequence[str] | Matcher[Sequence[str]]):
        """Matches if the command arguments match the given value or matcher.

        :param args: The expected args sequence or matcher.
        :return: Self, for chaining.
        """
        self.args = wrap_matcher(args)
        return self

    def and_args(self, args: Sequence[str] | Matcher[Sequence[str]]):
        """Matches if the command arguments match the given value or matcher.

        A synonym for :meth:`with_args`.

        :param args: The expected args sequence or matcher.
        :return: Self, for chaining.
        """
        return self.with_args(args)

    def with_stdin(self, stdin: bytes | Matcher[bytes]):
        """Matches if the stdin bytes match the given value or matcher.

        :param stdin: The expected stdin bytes or matcher.
        :return: Self, for chaining.
        """
        self.stdin = wrap_matcher(stdin)
        return self

    def and_stdin(self, stdin: bytes | Matcher[bytes]):
        """Matches if the stdin bytes match the given value or matcher.

        A synonym for :meth:`with_stdin`.

        :param stdin: The expected stdin bytes or matcher.
        :return: Self, for chaining.
        """
        return self.with_stdin(stdin)

    def with_files_created(self, files_created: Mapping[str, Any] | Matcher[Mapping[str, Any]]):
        """Matches if the files created dictionary matches the given value or matcher.

        :param files_created: The expected files created dictionary or matcher.
        :return: Self, for chaining.
        """
        self.files_created = wrap_matcher(files_created)
        return self

    def and_files_created(self, files_created: Mapping[str, Any] | Matcher[Mapping[str, Any]]):
        """Matches if the files created dictionary matches the given value or matcher.

        A synonym for :meth:`with_files_created`.

        :param files_created: The expected files created dictionary or matcher.
        :return: Self, for chaining.
        """
        return self.with_files_created(files_created)

    def with_files_deleted(self, files_deleted: Mapping[str, Any] | Matcher[Mapping[str, Any]]):
        """Matches if the files deleted dictionary matches the given value or matcher.

        :param files_deleted: The expected files deleted dictionary or matcher.
        :return: Self, for chaining.
        """
        self.files_deleted = wrap_matcher(files_deleted)
        return self

    def and_files_deleted(self, files_deleted: Mapping[str, Any] | Matcher[Mapping[str, Any]]):
        """Matches if the files deleted dictionary matches the given value or matcher.

        A synonym for :meth:`with_files_deleted`.

        :param files_deleted: The expected files deleted dictionary or matcher.
        :return: Self, for chaining.
        """
        return self.with_files_deleted(files_deleted)

    def with_files_updated(self, files_updated: Mapping[str, Any] | Matcher[Mapping[str, Any]]):
        """Matches if the files updated dictionary matches the given value or matcher.

        :param files_updated: The expected files updated dictionary or matcher.
        :return: Self, for chaining.
        """
        self.files_updated = wrap_matcher(files_updated)
        return self

    def and_files_updated(self, files_updated: Mapping[str, Any] | Matcher[Mapping[str, Any]]):
        """Matches if the files updated dictionary matches the given value or matcher.

        A synonym for :meth:`with_files_updated`.

        :param files_updated: The expected files updated dictionary or matcher.
        :return: Self, for chaining.
        """
        return self.with_files_updated(files_updated)
