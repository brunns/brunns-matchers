# encoding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import logging

from hamcrest import assert_that, not_, has_string

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.url import to_host, with_path

logger = logging.getLogger(__name__)


def test_to_host():
    URL = "http://brunni.ng/path"
    should_match = to_host("brunni.ng")
    should_not_match = to_host("example.com")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with host 'brunni.ng'"))
    assert_that(should_not_match, mismatches_with(URL, "host was 'brunni.ng'"))


def test_with_path():
    URL = "http://brunni.ng/path"
    should_match = with_path("/path")
    should_not_match = with_path("/banana")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with path '/path'"))
    assert_that(should_not_match, mismatches_with(URL, "path was </path>"))
