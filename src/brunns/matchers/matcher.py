# encoding=utf-8
import difflib
from typing import Any, Union

from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.core.isequal import IsEqual
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription


class MismatchesWith(BaseMatcher[Matcher]):
    def __init__(self, value_not_to_match: Any, expected_message: Union[str, Matcher[str]]) -> None:
        super(MismatchesWith, self).__init__()
        self.value_not_to_match = value_not_to_match
        self.expected_message: Matcher[str] = wrap_matcher(expected_message)

    def _matches(self, matcher_under_test: Matcher[Any]) -> bool:
        actual = StringDescription()
        matched = matcher_under_test.matches(self.value_not_to_match, actual)
        return not matched and self.expected_message.matches(actual.out)

    def describe_to(self, description: Description) -> None:
        description.append_text("a matcher which mismatches the value ").append_description_of(
            self.value_not_to_match
        ).append_text("\ngiving message ").append_description_of(self.expected_message)

    def describe_mismatch(self, matcher_under_test: Matcher[Any], description: Description) -> None:
        actual_message = StringDescription()
        if matcher_under_test.matches(self.value_not_to_match, actual_message):
            description.append_text("matched")
            return
        description.append_text("got message ").append_description_of(actual_message)
        self.append_diff(actual_message, description)

    def append_diff(self, actual_message, description):
        if isinstance(self.expected_message, IsEqual) and isinstance(
            self.expected_message.object, str
        ):
            differ = difflib.Differ()
            diff = differ.compare([self.expected_message.object], [actual_message.out])
            description.append_text("\ndiff:\n").append_text("\n".join(diff))


def mismatches_with(
    value_not_to_match: Any, expected_message: Union[str, Matcher[str]]
) -> MismatchesWith:
    """TODO"""
    return MismatchesWith(value_not_to_match, expected_message)


def mismatches(value_not_to_match: Any) -> MismatchesWith:
    """TODO"""
    return MismatchesWith(value_not_to_match, anything())


class MatchesWith(BaseMatcher[Matcher]):
    def __init__(self, value_to_match: Any, expected_message: Union[str, Matcher[str]]) -> None:
        super(MatchesWith, self).__init__()
        self.value_to_match = value_to_match
        self.expected_message: Matcher[str] = wrap_matcher(expected_message)

    def _matches(self, matcher_under_test: Matcher[Any]) -> bool:
        actual = StringDescription()
        matched = matcher_under_test.matches(self.value_to_match)
        if matched:
            matcher_under_test.describe_match(self.value_to_match, actual)
        return matched and self.expected_message.matches(actual.out)

    def describe_to(self, description: Description) -> None:
        description.append_text("a matcher which matches the value ").append_description_of(
            self.value_to_match
        ).append_text("\ngiving message ").append_description_of(self.expected_message)

    def describe_mismatch(self, matcher_under_test: Matcher[Any], description: Description) -> None:
        actual_message = StringDescription()
        if not matcher_under_test.matches(self.value_to_match):
            description.append_text("mismatched")
            return
        matcher_under_test.describe_match(self.value_to_match, actual_message)
        description.append_text("got message ").append_description_of(actual_message)
        self.append_diff(actual_message, description)

    def append_diff(self, actual_message, description):
        if isinstance(self.expected_message, IsEqual) and isinstance(
            self.expected_message.object, str
        ):
            differ = difflib.Differ()
            diff = differ.compare([self.expected_message.object], [actual_message.out])
            description.append_text("\ndiff:\n").append_text("\n".join(diff))


def matches_with(value_to_match: Any, expected_message: Union[str, Matcher[str]]) -> MatchesWith:
    """TODO"""
    return MatchesWith(value_to_match, expected_message)


def matches(value_to_match: Any) -> MatchesWith:
    """TODO"""
    return MatchesWith(value_to_match, anything())
