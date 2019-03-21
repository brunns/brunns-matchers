# encoding=utf-8
import difflib
from typing import Any

from brunns.matchers.base import GenericMatcher
from hamcrest import anything, not_
from hamcrest.core.core.isequal import IsEqual
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher
from hamcrest.core.string_description import StringDescription


class MismatchesWith(GenericMatcher[Matcher]):
    def __init__(self, value_not_to_match: Any, expected_message: str) -> None:
        super(MismatchesWith, self).__init__()
        self.value_not_to_match = value_not_to_match
        self.expected_message = wrap_matcher(expected_message)

    def _matches(self, matcher_under_test: Matcher) -> bool:
        actual = StringDescription()
        matched = matcher_under_test.matches(self.value_not_to_match, actual)
        return not matched and self.expected_message.matches(actual.out)

    def describe_to(self, description: Description) -> None:
        description.append_text("a matcher which mismatches the value ").append_description_of(
            self.value_not_to_match
        ).append_text("\ngiving message ").append_description_of(self.expected_message)

    def describe_mismatch(self, matcher_under_test: Matcher, description: Description) -> None:
        actual_message = StringDescription()
        if matcher_under_test.matches(self.value_not_to_match, actual_message):
            description.append_text("matched")
            return
        description.append_text("got message ").append_description_of(actual_message)
        if isinstance(self.expected_message, IsEqual) and isinstance(
            self.expected_message.object, str
        ):
            differ = difflib.Differ()
            diff = differ.compare([self.expected_message.object], [actual_message.out])
            description.append_text("\ndiff:\n").append_text("\n".join(diff))


def mismatches_with(value_not_to_match: Any, expected_message: str) -> MismatchesWith:
    """TODO"""
    return MismatchesWith(value_not_to_match, expected_message)


def mismatches(value_not_to_match: Any) -> MismatchesWith:
    """TODO"""
    return MismatchesWith(value_not_to_match, anything())


def matches(value_to_match: Any) -> Matcher:
    """TODO"""
    return not_(mismatches(value_to_match))
