from hamcrest import assert_that, contains_string, has_string, not_, matches_regexp, all_of

from junkdrawer.bunch import ReprFromDict
from brunns.matchers.matcher import mismatches_with
from brunns.matchers.object import has_repr, has_identical_properties_to, false, true


def test_has_repr():
    # Given
    r = [1, "2"]

    # When

    # Then
    assert_that(r, has_repr("[1, '2']"))
    assert_that(r, has_repr(contains_string("[1")))
    assert_that(has_repr("a"), has_string("an object with repr() matching 'a'"))
    assert_that(has_repr("a"), mismatches_with("b", "was 'b'"))


def test_identical_properties():
    # Given
    class SomeClass(ReprFromDict):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    class OtherClass(ReprFromDict):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    class YetAnotherClass(ReprFromDict):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    a = SomeClass(1, 2)
    b = OtherClass(1, 2)
    c = YetAnotherClass(1, 3)

    # When

    # Then
    assert_that(a, has_identical_properties_to(b))
    assert_that(a, not_(has_identical_properties_to(c)))
    assert_that(
        has_identical_properties_to(a),
        has_string(
            all_of(
                matches_regexp(r"object with identical properties to object .*SomeClass\("),
                contains_string("a=1"),
                contains_string("b=2"),
            )
        ),
    )
    assert_that(
        has_identical_properties_to(a),
        mismatches_with(
            c, all_of(matches_regexp(r"was .*YetAnotherClass\("), contains_string("a=1"), contains_string("b=3"))
        ),
    )


def test_truthy():
    assert_that([1], true())
    assert_that([], false())
    assert_that(true(), has_string("Truthy value"))
    assert_that(false(), has_string("not Truthy value"))
    assert_that(true(), mismatches_with([], "was <[]>"))
