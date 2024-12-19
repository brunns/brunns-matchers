import logging
import os
import platform
from datetime import timedelta

import pytest
import requests
from hamcrest import assert_that, contains_exactly, contains_string, has_entries, has_key, not_

from brunns.matchers.bytestring import contains_bytestring
from brunns.matchers.matcher import mismatches_with
from brunns.matchers.object import between
from brunns.matchers.response import is_response
from brunns.matchers.url import is_url
from tests.utils.network import internet_connection

logger = logging.getLogger(__name__)

INTERNET_CONNECTED = internet_connection()
LOCAL = os.getenv("GITHUB_ACTIONS") != "true"
LINUX = platform.system() == "Linux"
HTTPBIN_CONTAINERISED = LINUX or LOCAL


@pytest.mark.xfail(not HTTPBIN_CONTAINERISED, reason="Public httpbin horribly flaky.")
def test_response_status_code(httpbin):
    # Given

    # When
    actual = requests.get(httpbin / "status/345", timeout=5)

    # Then
    assert_that(actual, is_response().with_status_code(345))
    assert_that(actual, not_(is_response().with_status_code(201)))
    assert_that(
        is_response().with_status_code(201),
        mismatches_with(actual, contains_string("was response with status code: was <345>")),
    )


@pytest.mark.xfail(not HTTPBIN_CONTAINERISED, reason="Public httpbin horribly flaky.")
def test_response_json(httpbin):
    # Given

    # When
    actual = requests.get(httpbin / "json", timeout=5)

    # Then
    assert_that(actual, is_response().with_json(has_key("slideshow")))
    assert_that(actual, not_(is_response().with_json(has_key("shitshow"))))


@pytest.mark.xfail(not HTTPBIN_CONTAINERISED, reason="Public httpbin horribly flaky.")
def test_response_content(httpbin):
    # Given

    # When
    actual = requests.get(
        httpbin / "anything" % {"foo": "bar"},
        headers={"X-Clacks-Overhead": "Sir Terry Pratchett"},
        timeout=5,
    )

    # Then
    assert_that(actual, is_response().with_status_code(200))
    assert_that(actual, is_response().with_status_code(200).and_content(contains_bytestring(b"foo")))
    assert_that(actual, not_(is_response().with_content(b"seems unlikely")))


@pytest.mark.xfail(not HTTPBIN_CONTAINERISED, reason="Public httpbin horribly flaky.")
def test_response_cookies(httpbin):
    # Given

    # When
    actual = requests.get(httpbin / "cookies/set" % {"foo": "bar"}, allow_redirects=False, timeout=5)

    # Then
    assert_that(actual, is_response().with_status_code(302).and_cookies(has_entries(foo="bar")))


@pytest.mark.xfail(not HTTPBIN_CONTAINERISED, reason="Public httpbin horribly flaky.")
def test_response_elapsed(httpbin):
    # Given

    # When
    actual = requests.get(httpbin / "delay/0.5", timeout=5)

    # Then
    assert_that(
        actual,
        is_response().with_status_code(200).and_elapsed(between(timedelta(seconds=0.5), timedelta(seconds=1.5))),
    )


@pytest.mark.xfail(not HTTPBIN_CONTAINERISED, reason="Public httpbin horribly flaky.")
def test_response_history(httpbin):
    # Given

    # When
    actual = requests.get(httpbin / "cookies/set" % {"foo": "bar"}, timeout=5)

    # Then
    assert_that(
        actual,
        is_response()
        .with_status_code(200)
        .and_url(is_url().with_path("/cookies"))
        .and_history(contains_exactly(is_response().with_url(is_url().with_path("/cookies/set")))),
    )


@pytest.mark.xfail(not HTTPBIN_CONTAINERISED, reason="Public httpbin horribly flaky.")
def test_response_encoding(httpbin):
    # Given

    # When
    actual = requests.get(httpbin / "encoding/utf8", timeout=5)

    # Then
    assert_that(actual, is_response().with_encoding("utf-8"))
    assert_that(actual, not_(is_response().with_encoding("ISO-8859-1")))
