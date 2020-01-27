from datetime import date
from typing import Union

from brunns.matchers.object import between
from hamcrest import described_as
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher


def is_weekday() -> Matcher:
    """TODO"""
    matcher = HasWeekday(between(0, 4))
    return described_as("A weekday", matcher)


class HasWeekday(BaseMatcher[date]):
    def __init__(self, day: Union[int, Matcher]) -> None:
        self.day = wrap_matcher(day)

    def _matches(self, actual: date) -> bool:
        return self.day.matches(actual.weekday())

    def describe_to(self, description: Description) -> None:
        description.append_text("Date with weekday matching ").append_description_of(self.day)

    def describe_mismatch(self, actual: date, description: Description) -> None:
        description.append_text("was ").append_description_of(actual).append_text(
            " with weekday "
        ).append_description_of(actual.weekday()).append_text(", a ").append_text(
            actual.strftime("%A")
        )
