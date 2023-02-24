# encoding=utf-8
import logging
from datetime import timedelta

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


def test_response_status_code(httpbin):
    # Given

    # When
    actual = requests.get(httpbin.replace(path="/status/345"))

    # Then
    assert_that(actual, is_response().with_status_code(345))
    assert_that(actual, not_(is_response().with_status_code(201)))
    assert_that(
        is_response().with_status_code(201),
        mismatches_with(actual, contains_string("was response with status code: was <345>")),
    )


def test_response_json(httpbin):
    # Given

    # When
    actual = requests.get(httpbin.replace(path="/json"))

    # Then
    assert_that(actual, is_response().with_json(has_key("slideshow")))
    assert_that(actual, not_(is_response().with_json(has_key("shitshow"))))


def test_response_content(httpbin):
    # Given

    # When
    actual = requests.get(
        httpbin.replace(path="/anything").set_query("foo", "bar"),
        headers={"X-Clacks-Overhead": "Sir Terry Pratchett"},
    )

    # Then
    assert_that(actual, is_response().with_status_code(200))
    assert_that(
        actual, is_response().with_status_code(200).and_content(contains_bytestring(b"foo"))
    )
    assert_that(actual, not_(is_response().with_content(b"seems unlikely")))


def test_response_cookies(httpbin):
    # Given

    # When
    actual = requests.get(
        httpbin.replace(path="/cookies/set").set_query("foo", "bar"), allow_redirects=False
    )

    # Then
    assert_that(actual, is_response().with_status_code(302).and_cookies(has_entries(foo="bar")))


def test_response_elapsed(httpbin):
    # Given

    # When
    actual = requests.get(httpbin.replace(path="/delay/0.5"))

    # Then
    assert_that(
        actual,
        is_response()
        .with_status_code(200)
        .and_elapsed(between(timedelta(seconds=0.5), timedelta(seconds=1.5))),
    )


def test_response_history(httpbin):
    # Given

    # When
    actual = requests.get(httpbin.replace(path="/cookies/set").set_query("foo", "bar"))

    # Then
    assert_that(
        actual,
        is_response()
        .with_status_code(200)
        .and_url(is_url().with_path("/cookies"))
        .and_history(contains_exactly(is_response().with_url(is_url().with_path("/cookies/set")))),
    )


def test_response_encoding(httpbin):
    # Given

    # When
    actual = requests.get(httpbin.replace(path="/encoding/utf8"))

    # Then
    assert_that(actual, is_response().with_encoding("utf-8"))
    assert_that(actual, not_(is_response().with_encoding("ISO-8859-1")))
