# encoding=utf-8
import logging

from hamcrest import assert_that, contains_exactly, empty, has_entries, has_string, not_

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.url import is_url

logger = logging.getLogger(__name__)

URL = "https://username:password@brunni.ng:1234/path1/path2/path3?key1=value1&key2=value2#fragment"


def test_url_with_scheme():
    should_match = is_url().with_scheme("https")
    should_not_match = is_url().and_scheme("http")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with scheme: 'https'"))
    assert_that(should_not_match, mismatches_with(URL, "was URL with scheme: was 'https'"))


def test_url_with_username():
    should_match = is_url().with_username("username")
    should_not_match = is_url().with_username("nope")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with username: 'username'"))
    assert_that(should_not_match, mismatches_with(URL, "was URL with username: was 'username'"))


def test_url_with_password():
    should_match = is_url().with_password("password")
    should_not_match = is_url().with_password("nope")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with password: 'password'"))
    assert_that(should_not_match, mismatches_with(URL, "was URL with password: was 'password'"))


def test_url_with_host():
    should_match = is_url().with_host("brunni.ng")
    should_not_match = is_url().with_host("example.com")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with host: 'brunni.ng'"))
    assert_that(should_not_match, mismatches_with(URL, "was URL with host: was 'brunni.ng'"))


def test_url_with_port():
    should_match = is_url().with_port(1234)
    should_not_match = is_url().with_port(5678)

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with port: <1234>"))
    assert_that(should_not_match, mismatches_with(URL, "was URL with port: was <1234>"))


def test_url_with_path():
    should_match = is_url().with_path("/path1/path2/path3")
    should_not_match = is_url().with_path("/banana")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(should_match, has_string("URL with path: '/path1/path2/path3'"))
    assert_that(
        should_not_match, mismatches_with(URL, "was URL with path: was </path1/path2/path3>")
    )


def test_url_with_path_segments():
    should_match = is_url().with_path_segments(contains_exactly("path1", "path2", "path3"))
    should_not_match = is_url().with_path_segments(empty())

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(
        should_match,
        has_string("URL with path segments: a sequence containing ['path1', 'path2', 'path3']"),
    )
    assert_that(
        should_not_match,
        mismatches_with(URL, "was URL with path segments: was <['path1', 'path2', 'path3']>"),
    )


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


# TODO path.segments


def test_url_matcher_builder():
    # Given
    should_match = (
        is_url()
        .with_scheme("https")
        .and_username("username")
        .and_password("password")
        .and_host("brunni.ng")
        .and_port(1234)
        .and_path("/path1/path2/path3")
        .and_path_segments(contains_exactly("path1", "path2", "path3"))
        .and_query(has_entries(key1="value1", key2="value2"))
        .and_fragment("fragment")
    )
    should_not_match = is_url().with_path("woah!").and_host("example.com")

    assert_that(URL, should_match)
    assert_that(URL, not_(should_not_match))

    assert_that(
        should_match,
        has_string(
            "URL with "
            "scheme: 'https' "
            "username: 'username' "
            "password: 'password' "
            "host: 'brunni.ng' "
            "port: <1234> "
            "path: '/path1/path2/path3' "
            "path segments: a sequence containing ['path1', 'path2', 'path3'] "
            "query: a dictionary containing {'key1': 'value1', 'key2': 'value2'} "
            "fragment: 'fragment'"
        ),
    )
    assert_that(
        should_not_match,
        mismatches_with(URL, "was URL with host: was 'brunni.ng' path: was </path1/path2/path3>"),
    )
