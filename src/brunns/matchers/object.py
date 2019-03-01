# encoding=utf-8
from hamcrest import (
    not_,
    greater_than_or_equal_to,
    greater_than,
    less_than_or_equal_to,
    less_than,
    all_of,
)
from hamcrest.core.base_matcher import BaseMatcher

from hamcrest.core.helpers.wrap_matcher import wrap_matcher


def has_repr(expected):
    """object with repr() matching
    :param expected: Expected value.
    :type expected: str or Matcher(str)
    :return: Matcher(object)
    """
    return HasRepr(expected)


class HasRepr(BaseMatcher):
    """object with repr() matching"""

    def __init__(self, expected):
        self.expected = wrap_matcher(expected)

    def _matches(self, actual):
        return self.expected.matches(repr(actual))

    def describe_to(self, description):
        description.append_text("an object with repr() matching ")
        self.expected.describe_to(description)


def has_identical_properties_to(expected):
    """Matches object with identical properties to
    :param expected: Expected object
    :return: Matcher(object)
    """
    return HasIdenticalPropertiesTo(expected)


class HasIdenticalPropertiesTo(BaseMatcher):
    def __init__(self, expected):
        self.expected = expected

    def _matches(self, actual):
        return equal_vars(actual, self.expected)

    def describe_to(self, description):
        description.append_text(
            "object with identical properties to object "
        ).append_description_of(self.expected)


def equal_vars(left, right):
    try:
        lvars = vars(left)
        rvars = vars(right)
    except TypeError:
        return left == right
    return lvars.keys() == rvars.keys() and all(equal_vars(rvars[k], v) for k, v in lvars.items())


class Truthy(BaseMatcher):
    def describe_to(self, description):
        description.append_text("Truthy value")

    def _matches(self, item):
        return bool(item)


def true():
    """Matches truthy values.
    :return: Matcher(object)
    """
    return Truthy()


def false():
    """Matches falsey values.
    :return: Matcher(object)
    """
    return not_(true())


def between(lower, upper, lower_inclusive=True, upper_inclusive=True):
    return all_of(
        greater_than_or_equal_to(lower) if lower_inclusive else greater_than(lower),
        less_than_or_equal_to(upper) if upper_inclusive else less_than(upper),
    )
