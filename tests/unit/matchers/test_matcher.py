# encoding=utf-8
from hamcrest import assert_that, contains_string, has_string

from brunns.matchers.matcher import matches, mismatches, mismatches_with


def test_matcher_mismatches_with():
    # Given
    banana_matcher = contains_string("Banana")

    # When

    # Then
    assert_that(banana_matcher, matches("Banana"))
    assert_that(banana_matcher, mismatches("Apple"))
    assert_that(banana_matcher, mismatches_with("Apple", "was 'Apple'"))
    assert_that(banana_matcher, has_string("a string containing 'Banana'"))
