import datetime

from hamcrest import assert_that, contains_string, has_string, not_, matches_regexp, all_of

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.object import has_repr, has_identical_properties_to, false, true, between
from junkdrawer.bunch import ReprFromDict


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


def test_between():
    # Given
    r = 2

    # When

    # Then
    assert_that(r, between(1, 3))
    assert_that(r, not_(between(4, 6)))
    assert_that(between(1, 3), has_string("(a value greater than <1> and a value less than <3>)"))
    assert_that(between(4, 6), mismatches_with(3, contains_string("was <3>")))


def test_between_inclusive():
    assert_that(3, not_(between(1, 3)))
    assert_that(3, between(1, 3, upper_inclusive=True))
    assert_that(1, not_(between(1, 3)))
    assert_that(1, between(1, 3, lower_inclusive=True))


def test_between_dates():
    # Given
    date = datetime.date(1968, 7, 21)

    # When

    # Then
    assert_that(date, between(datetime.date(1968, 7, 20), datetime.date(1968, 7, 22)))
    assert_that(date, not_(between(datetime.date(1968, 7, 22), datetime.date(1968, 7, 24))))
    assert_that(
        between(datetime.date(1968, 7, 20), datetime.date(1968, 7, 22)),
        has_string("(a value greater than <1968-07-20> and a value less than <1968-07-22>)"),
    )
    assert_that(
        between(datetime.date(1968, 7, 22), datetime.date(1968, 7, 24)),
        mismatches_with(date, contains_string("was <1968-07-21>")),
    )
