# encoding=utf-8
from itertools import chain, zip_longest
from typing import Any, Union, cast
from unittest.mock import Mock, _Call

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher


class CallHasPositionalArg(BaseMatcher[_Call]):
    def __init__(self, index: int, expected: Any) -> None:
        super(CallHasPositionalArg, self).__init__()
        self.index = index
        self.expected = wrap_matcher(expected)

    def _matches(self, actual_call: _Call) -> bool:
        args = actual_call[1]
        return len(args) > self.index and self.expected.matches(args[self.index])

    def describe_to(self, description: Description) -> None:
        description.append_text("mock.call with argument index ").append_description_of(
            self.index
        ).append_text(" matching ")
        self.expected.describe_to(description)

    def describe_mismatch(self, actual_call: _Call, mismatch_description: Description) -> None:
        args = actual_call[1]
        if len(args) > self.index:
            mismatch_description.append_text(
                "got mock.call with argument index "
            ).append_description_of(self.index).append_text(" with value ").append_description_of(
                args[self.index]
            )
        else:
            mismatch_description.append_text(
                "got mock.call with without argument index "
            ).append_description_of(self.index)


class CallHasKeywordArg(BaseMatcher[_Call]):
    def __init__(self, key: str, expected: Any) -> None:
        super(CallHasKeywordArg, self).__init__()
        self.key = key
        self.expected = wrap_matcher(expected)

    def _matches(self, actual_call: _Call) -> bool:
        args = actual_call[2]
        return self.key in args and self.expected.matches(args[self.key])

    def describe_to(self, description: Description) -> None:
        description.append_text("mock.call with keyword argument ").append_description_of(
            self.key
        ).append_text(" matching ")
        self.expected.describe_to(description)

    def describe_mismatch(self, actual_call: _Call, mismatch_description: Description) -> None:
        args = actual_call[2]
        if self.key in args:
            mismatch_description.append_text(
                "got mock.call with keyword argument "
            ).append_description_of(self.key).append_text(" with value ").append_description_of(
                args[self.key]
            )
        else:
            mismatch_description.append_text(
                "got mock.call with without keyword argument "
            ).append_description_of(self.key)


class HasCall(BaseMatcher[Mock]):
    def __init__(self, call_matcher: Matcher) -> None:
        super(HasCall, self).__init__()
        self.call_matcher = call_matcher

    def _matches(self, mock: Mock) -> bool:
        for call in mock.mock_calls:
            if self.call_matcher.matches(call):
                return True
        return False

    def describe_to(self, description: Description) -> None:
        description.append_text("has call matching ")
        self.call_matcher.describe_to(description)

    def describe_mismatch(self, mock: Mock, mismatch_description: Description) -> None:
        mismatch_description.append_list(
            "got calls [", ", ", "]", [str(c) for c in mock.mock_calls]
        )


class CallHasArgs(BaseMatcher[_Call]):
    """mock.call with arguments"""

    def __init__(self, *args, **kwargs) -> None:
        super(CallHasArgs, self).__init__()
        self.args = [wrap_matcher(arg) for arg in args]
        self.kwargs = {key: wrap_matcher(value) for key, value in kwargs.items()}

    def _matches(self, actual_call: _Call) -> bool:
        actual_positional = actual_call[1]
        actual_keyword = actual_call[2]
        return all(
            m.matches(a) for m, a in zip_longest(self.args, actual_positional) if m is not None
        ) and all(m.matches(actual_keyword.get(k, None)) for k, m in self.kwargs.items())

    def describe_to(self, description: Description) -> None:
        description.append_text("mock.call with arguments (").append_text(
            ", ".join(
                chain((str(a) for a in self.args), (f"{k}={v}" for k, v in self.kwargs.items()),)
            )
        ).append_text(")")

    def describe_mismatch(self, call: _Call, mismatch_description: Description) -> None:
        mismatch_description.append_text("got arguments (").append_text(
            ", ".join(
                chain((repr(a) for a in call[1]), (f"{k}={v!r}" for k, v in call[2].items()),)
            )
        ).append_text(")")


def call_has_arg(arg: Union[int, str], expected: Any) -> BaseMatcher[_Call]:
    """TODO"""
    if isinstance(arg, int):
        return CallHasPositionalArg(cast("int", arg), expected)
    return CallHasKeywordArg(cast("str", arg), expected)


def has_call(call_matcher: Matcher) -> HasCall:
    """TODO"""
    return HasCall(call_matcher)


def call_has_args(*args, **kwargs) -> CallHasArgs:
    """mock.call with arguments
    TODO"""
    return CallHasArgs(*args, **kwargs)
