# encoding=utf-8
import collections
import inspect
from itertools import zip_longest
from typing import Any, Mapping, Union

from hamcrest import (
    all_of,
    greater_than,
    greater_than_or_equal_to,
    less_than,
    less_than_or_equal_to,
    not_,
)
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher


def has_repr(expected: Any) -> Matcher:
    """object with repr() matching
    :param expected: Expected value.
    """
    return HasRepr(expected)


class HasRepr(BaseMatcher):
    """object with repr() matching"""

    def __init__(self, expected: Union[str, Matcher]) -> None:
        self.expected = wrap_matcher(expected)

    def _matches(self, actual: Any) -> bool:
        return self.expected.matches(repr(actual))

    def describe_to(self, description: Description) -> None:
        description.append_text("an object with repr() matching ")
        self.expected.describe_to(description)


def has_identical_properties_to(expected: Any) -> Matcher:
    """Matches object with identical properties to
    :param expected: Expected object
    :return: Matcher(object)
    """
    return HasIdenticalPropertiesTo(expected)


class HasIdenticalPropertiesTo(BaseMatcher):
    def __init__(self, expected: Any) -> None:
        self.expected = expected

    def _matches(self, actual: Any) -> bool:
        return equal_vars(actual, self.expected)

    def describe_to(self, description: Description) -> None:
        description.append_text(
            "object with identical properties to object "
        ).append_description_of(self.expected)


def equal_vars(left: Any, right: Any) -> bool:
    """Test if two objects are equal using public vars() and properties if available, with == otherwise."""
    try:
        left_vars = _vars_and_properties(left)
        right_vars = _vars_and_properties(right)
        if left_vars:
            return left_vars.keys() == right_vars.keys() and all(
                equal_vars(right_vars[key], value) for key, value in left_vars.items()
            )
    except TypeError:
        pass
    return _equal_vars_for_non_objects(left, right)


def _equal_vars_for_non_objects(left: Any, right: Any) -> bool:
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


def _vars_and_properties(obj: Any) -> Mapping[str, Any]:
    """Get an object's public vars() and properties. Raises TypeError if not an obcect with vars()/"""
    vars_and_props = {key: value for key, value in vars(obj).items() if not key.startswith("_")}
    classes = inspect.getmembers(obj, inspect.isclass)
    for cls in classes:
        props = inspect.getmembers(cls[1], lambda o: isinstance(o, property))
        for prop in props:
            vars_and_props[prop[0]] = getattr(obj, prop[0])
    return vars_and_props


class Truthy(BaseMatcher):
    def describe_to(self, description: Description) -> None:
        description.append_text("Truthy value")

    def _matches(self, item: Any) -> bool:
        return bool(item)


def true() -> Matcher:
    """Matches truthy values.
    :return: Matcher(object)
    """
    return Truthy()


def false() -> Matcher:
    """Matches falsey values.
    :return: Matcher(object)
    """
    return not_(true())


def between(lower: Any, upper: Any, lower_inclusive=True, upper_inclusive=True) -> bool:
    """TODO"""
    return all_of(
        greater_than_or_equal_to(lower) if lower_inclusive else greater_than(lower),
        less_than_or_equal_to(upper) if upper_inclusive else less_than(upper),
    )
