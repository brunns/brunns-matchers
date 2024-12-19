from hamcrest import assert_that, contains_string, has_string

from brunns.matchers.matcher import matches, matches_with, mismatches, mismatches_with


def test_matcher_mismatches_with():
    # Given
    banana_matcher = contains_string("Banana")

    # When

    # Then
    assert_that(banana_matcher, mismatches("Apple"))
    assert_that(banana_matcher, mismatches_with("Apple", "was 'Apple'"))
    assert_that(
        mismatches_with("Apple", "was 'Apple'"),
        has_string("a matcher which mismatches the value 'Apple'\ngiving message \"was 'Apple'\""),
    )


def test_matcher_matches_with():
    # Given
    banana_matcher = contains_string("Banana")

    # When

    # Then

    assert_that(banana_matcher, matches("Banana"))
    assert_that(banana_matcher, matches_with("Banana", "was 'Banana'"))
    assert_that(
        matches_with("Apple", "was 'Apple'"),
        has_string("a matcher which matches the value 'Apple'\ngiving message \"was 'Apple'\""),
    )
