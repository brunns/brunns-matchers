import collections
import inspect
from collections.abc import Iterable, Mapping
from itertools import zip_longest
from typing import Any, Optional, Union

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


def has_repr(expected: Any) -> Matcher[Any]:
    """Object with repr() matching
    :param expected: Expected value.
    """
    return HasRepr(expected)


class HasRepr(BaseMatcher[Any]):
    """object with repr() matching"""

    def __init__(self, expected: Union[str, Matcher[str]]) -> None:
        self.expected: Matcher[str] = wrap_matcher(expected)

    def _matches(self, actual: Any) -> bool:
        return self.expected.matches(repr(actual))

    def describe_to(self, description: Description) -> None:
        description.append_text("an object with repr() matching ")
        self.expected.describe_to(description)


def has_identical_properties_to(expected: Any, ignoring: Optional[Iterable[str]] = None) -> Matcher[Any]:
    """Matches object with identical properties to
    :param expected: Expected object
    :param ignoring: Collection of names to ignore in comparisons
    """
    return HasIdenticalPropertiesTo(expected, ignoring=ignoring)


class HasIdenticalPropertiesTo(BaseMatcher[Any]):
    def __init__(self, expected: Any, ignoring: Optional[Iterable[str]] = None) -> None:
        self.expected = expected
        self.ignoring = ignoring

    def _matches(self, actual: Any) -> bool:
        return equal_vars(actual, self.expected, ignoring=self.ignoring)

    # TODO: Needs a describe_mismatch()

    def describe_to(self, description: Description) -> None:
        description.append_text("object with identical properties to object ").append_description_of(self.expected)
        if self.ignoring:
            description.append_text(" ignoring properties named ").append_list("{", ", ", "}", self.ignoring)


def equal_vars(left: Any, right: Any, ignoring: Optional[Iterable[str]] = None) -> bool:
    """Test if two objects are equal using public vars() and properties if available, with == otherwise."""
    try:
        left_vars = _vars_and_properties(left, ignoring=ignoring)
        right_vars = _vars_and_properties(right, ignoring=ignoring)
    except TypeError:
        return _equal_vars_for_non_objects(left, right)
    else:
        return left_vars.keys() == right_vars.keys() and all(
            equal_vars(right_vars[key], value, ignoring=ignoring) for key, value in left_vars.items()
        )


def _equal_vars_for_non_objects(left: Any, right: Any) -> bool:
    if (
        isinstance(left, collections.abc.Sequence)
        and not isinstance(left, str)
        and isinstance(right, collections.abc.Sequence)
        and not isinstance(right, str)
    ):
        return all(equal_vars(left_var, right_var) for left_var, right_var in zip_longest(left, right))
    if isinstance(left, collections.abc.Mapping) and isinstance(right, collections.abc.Mapping):
        return left.keys() == right.keys() and all(equal_vars(right[key], value) for key, value in left.items())
    return left == right


def _vars_and_properties(obj: Any, ignoring: Optional[Iterable[str]] = None) -> Mapping[str, Any]:
    """Get an object's public vars() and properties. Raises TypeError if not an object with vars()."""
    ignoring = ignoring or {}
    vars_and_props = {
        key: value for key, value in vars(obj).items() if not key.startswith("_") and key not in ignoring
    }  # vars
    classes = inspect.getmembers(obj, inspect.isclass)
    for cls in classes:  # props
        props = inspect.getmembers(cls[1], lambda o: isinstance(o, property))
        for prop in props:
            name = prop[0]
            if name not in ignoring:
                vars_and_props[name] = getattr(obj, name)
    return vars_and_props


class Truthy(BaseMatcher[Any]):
    def describe_to(self, description: Description) -> None:
        description.append_text("Truthy value")

    def _matches(self, item: Any) -> bool:
        return bool(item)


def true() -> Matcher[Any]:
    """Matches truthy values.
    :return: Matcher(object)
    """
    return Truthy()


def false() -> Matcher[Any]:
    """Matches falsey values.
    :return: Matcher(object)
    """
    return not_(true())


def between(lower: Any, upper: Any, *, lower_inclusive=True, upper_inclusive=True) -> Matcher[Any]:
    """TODO"""
    return all_of(
        greater_than_or_equal_to(lower) if lower_inclusive else greater_than(lower),
        less_than_or_equal_to(upper) if upper_inclusive else less_than(upper),
    )
