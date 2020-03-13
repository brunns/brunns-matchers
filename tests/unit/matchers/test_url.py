# encoding=utf-8
import logging

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.url import is_url
from hamcrest import assert_that, has_entries, has_string, not_

logger = logging.getLogger(__name__)

URL = "http://brunni.ng/path?key1=value1&key2=value2#fragment"


def test_url_with_host():
    should_match = is_url().with_host("brunni.ng")
    should_not_match = is_url().with_host("example.com")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with host: 'brunni.ng'"))
    assert_that(should_not_match, mismatches_with(URL, "was URL with host: was 'brunni.ng'"))


def test_url_with_path():
    should_match = is_url().with_path("/path")
    should_not_match = is_url().with_path("/banana")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with path: '/path'"))
    assert_that(should_not_match, mismatches_with(URL, "was URL with path: was </path>"))


def test_url_with_query():
    should_match = is_url().with_query(has_entries(key1="value1", key2="value2"))
    should_not_match = is_url().with_query(has_entries(key1="value1", key2="nope"))

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(
        should_match,
        has_string("URL with query: a dictionary containing {'key1': 'value1', 'key2': 'value2'}"),
    )
    assert_that(
        should_not_match, mismatches_with(URL, "was URL with query: value for 'key2' was 'value2'")
    )


def test_url_with_fragment():
    should_match = is_url().with_fragment("fragment")
    should_not_match = is_url().with_fragment("banana")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with fragment: 'fragment'"))
    assert_that(should_not_match, mismatches_with(URL, "was URL with fragment: was <fragment>"))


# TODO scheme, username, password, port, netloc, origin, path.segments,
URL = "http://brunni.ng/path?key1=value1&key2=value2#fragment"


def test_url_matcher_builder():
    # Given
    should_match = (
        is_url()
        .with_host("brunni.ng")
        .and_path("/path")
        .and_query(has_entries(key1="value1", key2="value2"))
        .and_fragment("fragment")
    )
    should_not_match = is_url().with_path("hoah!").and_host("example.com")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(
        should_match,
        has_string(
            "URL with "
            "host: 'brunni.ng' "
            "path: '/path' "
            "query: a dictionary containing {'key1': 'value1', 'key2': 'value2'} "
            "fragment: 'fragment'"
        ),
    )
    assert_that(
        should_not_match,
        mismatches_with(URL, "was URL with host: was 'brunni.ng' path: was </path>"),
    )
