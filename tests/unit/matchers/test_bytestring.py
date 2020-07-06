# encoding=utf-8
import logging

from hamcrest import assert_that, has_string, not_

from brunns.matchers.bytestring import contains_bytestring
from brunns.matchers.matcher import mismatches_with

logger = logging.getLogger(__name__)


def test_contains_bytestring():
    should_match = contains_bytestring(b"foo")
    should_not_match = contains_bytestring(b"bar")

    assert_that(b"a foo b", should_match)
    assert_that(b"a foo b", not_(should_not_match))

    assert_that(should_match, has_string("bytestring containing <b'foo'>"))
    assert_that(should_not_match, mismatches_with(b" a foo b", "was <b' a foo b'>"))
