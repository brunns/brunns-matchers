# encoding=utf-8
import collections
import inspect
from itertools import zip_longest

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
    """Test if two objects are equal using public vars() and properties if available, with == otherwise."""
    try:
        left_vars = vars_and_properties(left)
        right_vars = vars_and_properties(right)
        if left_vars:
            return left_vars.keys() == right_vars.keys() and all(
                equal_vars(right_vars[key], value) for key, value in left_vars.items()
            )
    except TypeError:
        pass
    return _equal_vars_for_non_objects(left, right)


def _equal_vars_for_non_objects(left, right):
    if (
        isinstance(left, collections.abc.Sequence)
        and not isinstance(left, str)
        and isinstance(right, collections.abc.Sequence)
        and not isinstance(right, str)
    ):
        return all(equal_vars(l, r) for l, r in zip_longest(left, right))
    elif isinstance(left, collections.abc.Mapping) and isinstance(right, collections.abc.Mapping):
        return left.keys() == right.keys() and all(
            equal_vars(right[key], value) for key, value in left.items()
        )
    else:
        return left == right


def vars_and_properties(obj):
    """Get an object's public vars() and properties. Raises TypeError if not an obcect with vars()/"""
    vars_and_props = {key: value for key, value in vars(obj).items() if not key.startswith("_")}
    classes = inspect.getmembers(obj, inspect.isclass)
    for cls in classes:
        props = inspect.getmembers(cls[1], lambda o: isinstance(o, property))
        for prop in props:
            vars_and_props[prop[0]] = getattr(obj, prop[0])
    return vars_and_props


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
