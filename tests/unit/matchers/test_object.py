# encoding=utf-8
import datetime
from pathlib import Path

from brunns.builder.internet import UrlBuilder
from brunns.matchers.matcher import mismatches_with
from brunns.matchers.object import (
    between,
    equal_vars,
    false,
    has_identical_properties_to,
    has_repr,
    true,
)
from hamcrest import assert_that, contains_string, has_string, not_


def test_has_repr():
    # Given
    r = [1, "2"]

    # When

    # Then
    assert_that(r, has_repr(contains_string("[1, '2']")))
    assert_that(r, has_repr(contains_string("[1")))
    assert_that(has_repr("a"), has_string("an object with repr() matching 'a'"))
    assert_that(has_repr("a"), mismatches_with("b", "was 'b'"))


def test_identical_properties():
    # Given
    class SomeClass(object):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    class OtherClass(object):
        def __init__(self, a, b):
            self.a = a
            self._b = b

        @property
        def b(self):
            return self._b

    class YetAnotherClass(object):
        def __init__(self, a, b):
            self.a = a
            self.b = b

    a = SomeClass(1, 2)
    b = OtherClass(1, 2)
    c = YetAnotherClass(1, 3)

    # Then
    assert_that(a, has_identical_properties_to(b))
    assert_that(a, not_(has_identical_properties_to(c)))
    assert_that(
        has_identical_properties_to(a),
        has_string("object with identical properties to object {0}".format(a)),
    )
    assert_that(has_identical_properties_to(a), mismatches_with(c, "was {0}".format(c)))


def test_nested_identical_properties():
    # Given
    class SomeClass(object):
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self._c = c

        @property
        def c(self):
            return self._c

        def some_method(self):
            pass

    a = SomeClass(1, SomeClass(2, 3, 4), 4)
    b = SomeClass(1, SomeClass(2, 3, 4), 4)
    c = SomeClass(1, SomeClass(2, 4, 5), 6)

    # Then
    assert_that(a, has_identical_properties_to(b))
    assert_that(a, not_(has_identical_properties_to(c)))
    assert_that(
        has_identical_properties_to(a),
        has_string("object with identical properties to object {0}".format(a)),
    )
    assert_that(has_identical_properties_to(a), mismatches_with(c, "was {0}".format(c)))


def test_equal_vars():
    # Given
    class SomeClass(object):
        def __init__(self, a, b, c):
            self.a = a
            self.b = b
            self._c = c

        @property
        def c(self):
            return self._c

    a = SomeClass(1, SomeClass(2, 3, 4), 4)
    b = SomeClass(1, SomeClass(2, 3, 4), 4)
    c = SomeClass(1, SomeClass(2, 4, 5), 6)
    d = SomeClass(1, SomeClass(2, 4, 5), SomeClass(2, 4, 5))

    date1 = datetime.date(1968, 7, 21)
    date2 = datetime.date(1968, 7, 21)
    date3 = datetime.date.today()

    path1 = Path("some/path")
    path2 = Path("some/path")
    path3 = Path("some/other/path")

    url_builder = UrlBuilder()
    url1 = url_builder.build()
    url2 = url_builder.build()
    url3 = url_builder.with_host("example.com").build()

    # Then
    assert equal_vars(a, b)
    assert equal_vars(b, a)
    assert not equal_vars(a, c)
    assert not equal_vars(c, a)
    assert not equal_vars(a, d)
    assert not equal_vars(d, a)

    b.d = "foo"
    assert not equal_vars(a, b)

    assert not equal_vars(a, "string")
    assert not equal_vars("string", a)

    assert not equal_vars(a, date1)
    assert not equal_vars(date1, a)

    assert equal_vars(date1, date2)
    assert not equal_vars(date1, date3)

    assert equal_vars(path1, path2)
    assert not equal_vars(path1, path3)

    assert equal_vars(url1, url2)
    assert not equal_vars(url1, url3)


def test_equal_vars_for_objects_containing_list_of_objects():
    # Given
    class SomeClass(object):
        def __init__(self, a):
            self.a = a

    a = SomeClass(a=[SomeClass(a="a")])
    b = SomeClass(a=[SomeClass(a="a")])
    c = SomeClass(a=[SomeClass(a="sausages")])

    # Then
    assert equal_vars(a, b)
    assert not equal_vars(a, c)


def test_equal_vars_for_objects_containing_dict_of_objects():
    # Given
    class SomeClass(object):
        def __init__(self, a):
            self.a = a

    a = SomeClass(a={"key": SomeClass(a="a")})
    b = SomeClass(a={"key": SomeClass(a="a")})
    c = SomeClass(a={"key": SomeClass(a="sausages")})

    # Then
    assert equal_vars(a, b)
    assert not equal_vars(a, c)


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
    assert_that(
        between(1, 3),
        has_string("(a value greater than or equal to <1> and a value less than or equal to <3>)"),
    )
    assert_that(
        between(1, 3, lower_inclusive=False, upper_inclusive=False),
        has_string("(a value greater than <1> and a value less than <3>)"),
    )
    assert_that(between(4, 6), mismatches_with(3, contains_string("was <3>")))


def test_between_exclusive():
    assert_that(3, not_(between(1, 3, upper_inclusive=False)))
    assert_that(3, between(1, 3))
    assert_that(1, not_(between(1, 3, lower_inclusive=False)))
    assert_that(1, between(1, 3))


def test_between_dates():
    # Given
    date = datetime.date(1968, 7, 21)

    # When

    # Then
    assert_that(date, between(datetime.date(1968, 7, 20), datetime.date(1968, 7, 22)))
    assert_that(date, not_(between(datetime.date(1968, 7, 22), datetime.date(1968, 7, 24))))
    assert_that(
        between(datetime.date(1968, 7, 20), datetime.date(1968, 7, 22)),
        has_string(
            "(a value greater than or equal to <1968-07-20> and a value less than or equal to <1968-07-22>)"
        ),
    )
    assert_that(
        between(datetime.date(1968, 7, 22), datetime.date(1968, 7, 24)),
        mismatches_with(date, contains_string("was <1968-07-21>")),
    )
