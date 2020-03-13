# encoding=utf-8
import logging
from datetime import timedelta

import pytest
import requests
from brunns.matchers.bytestring import contains_bytestring
from brunns.matchers.matcher import mismatches_with
from brunns.matchers.object import between
from brunns.matchers.response import is_response, response_with
from brunns.utils.network import internet_connection
from hamcrest import assert_that, contains_string, has_entries, has_key, not_

logger = logging.getLogger(__name__)

INTERNET_CONNECTED = internet_connection()


@pytest.mark.skipif(not INTERNET_CONNECTED, reason="No internet connection.")
def test_response_status_code():
    # Given

    # When
    actual = requests.get("https://httpbin.org/status/345")

    # Then
    assert_that(actual, response_with(status_code=345))
    assert_that(actual, not_(response_with(status_code=201)))
    assert_that(
        response_with(status_code=201),
        mismatches_with(actual, contains_string("was response with status code: <345>")),
    )


@pytest.mark.skipif(not INTERNET_CONNECTED, reason="No internet connection.")
def test_response_json():
    # Given

    # When
    actual = requests.get("https://httpbin.org/json")

    # Then
    assert_that(actual, response_with(json=has_key("slideshow")))
    assert_that(actual, not_(response_with(json=has_key("shitshow"))))


@pytest.mark.skipif(not INTERNET_CONNECTED, reason="No internet connection.")
def test_response_content():
    # Given

    # When
    actual = requests.get(
        "https://httpbin.org/anything?foo=bar", headers={"X-Clacks-Overhead": "Sir Terry Pratchett"}
    )

    # Then
    assert_that(actual, is_response().with_status_code(200))
    assert_that(
        actual, is_response().with_status_code(200).and_content(contains_bytestring(b"foo"))
    )
    assert_that(actual, not_(is_response().with_content(b"seems unlikely")))


@pytest.mark.skipif(not INTERNET_CONNECTED, reason="No internet connection.")
def test_response_cookies():
    # Given

    # When
    actual = requests.get("https://httpbin.org/cookies/set?foo=bar", allow_redirects=False)

    # Then
    assert_that(actual, is_response().with_status_code(302).and_cookies(has_entries(foo="bar")))


@pytest.mark.skipif(not INTERNET_CONNECTED, reason="No internet connection.")
def test_response_elapsed():
    # Given

    # When
    actual = requests.get("https://httpbin.org/delay/0.5")

    # Then
    assert_that(
        actual,
        is_response()
        .with_status_code(200)
        .and_elapsed(between(timedelta(seconds=0.5), timedelta(seconds=1.5))),
    )
