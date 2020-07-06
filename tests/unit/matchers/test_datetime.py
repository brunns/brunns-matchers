import datetime

from hamcrest import assert_that, has_string, not_

from brunns.matchers.datetime import HasWeekday, is_weekday
from brunns.matchers.matcher import mismatches_with


def test_HasWeekday():
    assert_that(datetime.date(1968, 7, 21), HasWeekday(6))
    assert_that(datetime.date(1968, 7, 21), not_(HasWeekday(2)))

    assert_that(HasWeekday(2), has_string("Date with weekday matching <2>"))
    assert_that(
        HasWeekday(2),
        mismatches_with(datetime.date(1968, 7, 21), "was <1968-07-21> with weekday <6>, a Sunday"),
    )


def test_is_weekday():
    assert_that(datetime.date(1968, 7, 19), is_weekday())
    assert_that(datetime.date(1968, 7, 21), not_(is_weekday()))

    assert_that(is_weekday(), has_string("A weekday"))
    assert_that(
        is_weekday(),
        mismatches_with(datetime.date(1968, 7, 21), "was <1968-07-21> with weekday <6>, a Sunday"),
    )
