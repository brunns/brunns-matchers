import collections
import inspect
from collections.abc import Iterable, Mapping
from itertools import zip_longest
from typing import Any

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
    """Matches if the object's ``repr()`` matches the expected string or matcher.

    :param expected: The expected string representation or a string matcher.
    :return: A matcher that validates ``repr(obj)``.
    """
    return HasRepr(expected)


class HasRepr(BaseMatcher[Any]):
    def __init__(self, expected: str | Matcher[str]) -> None:
        self.expected: Matcher[str] = wrap_matcher(expected)

    def _matches(self, actual: Any) -> bool:
        return self.expected.matches(repr(actual))

    def describe_to(self, description: Description) -> None:
        description.append_text("an object with repr() matching ")
        self.expected.describe_to(description)


def has_identical_properties_to(expected: Any, ignoring: Iterable[str] | None = None) -> Matcher[Any]:
    """Matches an object if its public properties and attributes are identical to the expected object's.

    This matcher performs a deep recursive comparison of all public attributes (those not starting with ``_``)
    and properties. It gracefully handles nested dictionaries and sequences.

    :param expected: The reference object to compare against.
    :param ignoring: A collection of attribute names to exclude from the comparison.
    :return: A matcher for object equality based on public state.
    """
    return HasIdenticalPropertiesTo(expected, ignoring=ignoring)


class HasIdenticalPropertiesTo(BaseMatcher[Any]):
    def __init__(self, expected: Any, ignoring: Iterable[str] | None = None) -> None:
        self.expected = expected
        self.ignoring = ignoring

    def _matches(self, actual: Any) -> bool:
        return equal_vars(actual, self.expected, ignoring=self.ignoring)

    # TODO: Needs a describe_mismatch()

    def describe_to(self, description: Description) -> None:
        description.append_text("object with identical properties to object ").append_description_of(self.expected)
        if self.ignoring:
            description.append_text(" ignoring properties named ").append_list("{", ", ", "}", self.ignoring)


def equal_vars(left: Any, right: Any, ignoring: Iterable[str] | None = None) -> bool:
    """Test if two objects are equal using public vars() and properties if available, with == otherwise.

    :param left: The first object to compare.
    :param right: The second object to compare.
    :param ignoring: Optional list of attribute names to ignore.
    :return: True if objects are equivalent, False otherwise.
    """
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


def _vars_and_properties(obj: Any, ignoring: Iterable[str] | None = None) -> Mapping[str, Any]:
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
    """Matches any value that evaluates to True in a boolean context (truthy).

    :return: A matcher for truthiness.
    """
    return Truthy()


def false() -> Matcher[Any]:
    """Matches any value that evaluates to False in a boolean context (falsy).

    :return: A matcher for falsiness.
    """
    return not_(true())


def between(lower: Any, upper: Any, *, lower_inclusive=True, upper_inclusive=True) -> Matcher[Any]:
    """Matches if a value is within a specific range.

    :param lower: The lower bound of the range.
    :param upper: The upper bound of the range.
    :param lower_inclusive: If True, the range includes the lower bound (>=).
                            If False, it is exclusive (>). Defaults to True.
    :param upper_inclusive: If True, the range includes the upper bound (<=).
                            If False, it is exclusive (<). Defaults to True.
    :return: A matcher for the specified range.
    """
    return all_of(
        greater_than_or_equal_to(lower) if lower_inclusive else greater_than(lower),
        less_than_or_equal_to(upper) if upper_inclusive else less_than(upper),
    )
