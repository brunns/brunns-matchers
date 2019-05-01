# encoding=utf-8
import logging

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.url import url_with_fragment, url_with_host, url_with_path, url_with_query
from hamcrest import assert_that, has_entries, has_string, not_

logger = logging.getLogger(__name__)

URL = "http://brunni.ng/path?key1=value1&key2=value2#fragment"


def test_url_with_host():
    should_match = url_with_host("brunni.ng")
    should_not_match = url_with_host("example.com")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with host 'brunni.ng'"))
    assert_that(should_not_match, mismatches_with(URL, "host was 'brunni.ng'"))


def test_url_with_path():
    should_match = url_with_path("/path")
    should_not_match = url_with_path("/banana")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with path '/path'"))
    assert_that(should_not_match, mismatches_with(URL, "path was </path>"))


def test_url_with_query():
    should_match = url_with_query(has_entries(key1="value1", key2="value2"))
    should_not_match = url_with_query(has_entries(key1="value1", key2="nope"))

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(
        should_match,
        has_string("URL with query a dictionary containing {'key1': 'value1', 'key2': 'value2'}"),
    )
    assert_that(should_not_match, mismatches_with(URL, "query value for 'key2' was 'value2'"))


def test_url_with_fragment():
    should_match = url_with_fragment("fragment")
    should_not_match = url_with_fragment("banana")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with fragment 'fragment'"))
    assert_that(should_not_match, mismatches_with(URL, "fragment was <fragment>"))
