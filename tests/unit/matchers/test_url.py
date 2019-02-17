# encoding=utf-8
import logging

from hamcrest import assert_that, not_, has_string, has_entries

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.url import to_host, with_path, with_query, with_fragment

logger = logging.getLogger(__name__)

URL = "http://brunni.ng/path?key1=value1&key2=value2#fragment"


def test_to_host():
    should_match = to_host("brunni.ng")
    should_not_match = to_host("example.com")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with host 'brunni.ng'"))
    assert_that(should_not_match, mismatches_with(URL, "host was 'brunni.ng'"))


def test_with_path():
    should_match = with_path("/path")
    should_not_match = with_path("/banana")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with path '/path'"))
    assert_that(should_not_match, mismatches_with(URL, "path was </path>"))


def test_with_query():
    should_match = with_query(has_entries(key1="value1", key2="value2"))
    should_not_match = with_query(has_entries(key1="value1", key2="nope"))

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(
        should_match,
        has_string("URL with query a dictionary containing {'key1': 'value1', 'key2': 'value2'}"),
    )
    assert_that(should_not_match, mismatches_with(URL, "query value for 'key2' was 'value2'"))


def test_with_fragment():
    should_match = with_fragment("fragment")
    should_not_match = with_fragment("banana")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with fragment 'fragment'"))
    assert_that(should_not_match, mismatches_with(URL, "fragment was <fragment>"))
