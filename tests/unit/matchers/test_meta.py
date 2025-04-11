from dataclasses import dataclass
from typing import Optional

import pytest
from hamcrest import assert_that, has_items, has_string, not_, starts_with
from hamcrest.core.matcher import Matcher

from brunns.matchers.matcher import matches_with, mismatches_with
from brunns.matchers.meta import BaseAutoMatcher


@dataclass
class Status:
    id: int
    code: str
    reason: Optional[str] = None


def test_metaclass():
    class StatusMatcher(BaseAutoMatcher[Status]): ...

    def is_status() -> Matcher[Status]:
        return StatusMatcher()

    status = Status(id=99, code="ACTIVE")

    should_match = is_status().with_code(starts_with("ACT")).and_reason(None)
    should_not_match = is_status().with_id(42)

    assert_that(status, should_match)
    assert_that(status, not_(should_not_match))

    assert_that(should_match, has_string("Status with code: a string starting with 'ACT' reason: <None>"))
    assert_that(should_not_match, mismatches_with(status, "was Status with id: was <99>"))
    assert_that(should_match, matches_with(status, "was Status with code: was 'ACTIVE' reason: was <None>"))

    assert_that(dir(is_status()), has_items("with_id", "with_code", "with_reason", "and_id", "and_code", "and_reason"))

    with pytest.raises(AttributeError):
        is_status().with_banana("banana")


def test_no_domain_class_specified():
    with pytest.raises(TypeError):

        class NothingMatcher(BaseAutoMatcher): ...


def test_metaclass_with_explicit_domain_class():
    class StatusMatcher(BaseAutoMatcher):
        __domain_class__ = Status

    def is_status() -> Matcher[Status]:
        return StatusMatcher()

    status = Status(id=99, code="ACTIVE")

    should_match = is_status().with_code(starts_with("ACT")).and_reason(None)
    should_not_match = is_status().with_id(42)

    assert_that(status, should_match)
    assert_that(status, not_(should_not_match))

    assert_that(should_match, has_string("Status with code: a string starting with 'ACT' reason: <None>"))
    assert_that(should_not_match, mismatches_with(status, "was Status with id: was <99>"))
    assert_that(should_match, matches_with(status, "was Status with code: was 'ACTIVE' reason: was <None>"))
