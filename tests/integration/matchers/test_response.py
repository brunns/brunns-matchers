# encoding=utf-8
import logging

import requests
from brunns.matchers.matcher import mismatches_with
from brunns.matchers.response import response_with
from hamcrest import assert_that, contains_string, has_key, not_

logger = logging.getLogger(__name__)


def test_response_status_code():
    # Given

    # When
    response = requests.get("https://httpbin.org/status/345")

    # Then
    assert_that(response, response_with(status_code=345))
    assert_that(response, not_(response_with(status_code=201)))
    assert_that(
        response_with(status_code=201),
        mismatches_with(response, contains_string("was response with status code: <345>")),
    )


def test_response_json():
    # Given

    # When
    response = requests.get("https://httpbin.org/json")

    # Then
    assert_that(response, response_with(json=has_key("slideshow")))
    assert_that(response, not_(response_with(json=has_key("shitshow"))))


def test_response_content():
    # Given

    # When
    response = requests.get(
        "https://httpbin.org/anything?foo=bar", headers={"X-Clacks-Overhead": "Sir Terry Pratchett"}
    )

    # Then
    assert_that(response, not_(response_with(content=b"seems unlikely")))
