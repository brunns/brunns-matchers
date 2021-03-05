# encoding=utf-8
import logging
from typing import Any

from hamcrest.core.core.isanything import IsAnything
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher

logger = logging.getLogger(__name__)


def append_matcher_description(
    field_matcher: Matcher[Any], field_name: str, description: Description
) -> None:
    if not isinstance(field_matcher, IsAnything):
        description.append_text(f" {field_name}: ").append_description_of(field_matcher)


def describe_field_mismatch(
    field_matcher: Matcher[Any],
    field_name: str,
    actual_value: Any,
    mismatch_description: Description,
) -> None:
    if not isinstance(field_matcher, IsAnything) and not field_matcher.matches(actual_value):
        mismatch_description.append_text(f" {field_name}: ")
        field_matcher.describe_mismatch(actual_value, mismatch_description)


def describe_field_match(
    field_matcher: Matcher[Any],
    field_name: str,
    actual_value: Any,
    match_description: Description,
) -> None:
    if not isinstance(field_matcher, IsAnything) and field_matcher.matches(actual_value):
        match_description.append_text(f" {field_name}: ")
        field_matcher.describe_match(actual_value, match_description)
