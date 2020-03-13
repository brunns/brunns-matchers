# encoding=utf-8
from datetime import timedelta
from unittest import mock

from brunns.builder.internet import UrlBuilder  # type: ignore
from brunns.matchers.matcher import mismatches_with
from brunns.matchers.response import is_response, redirects_to, response_with
from brunns.matchers.url import url_with_path
from hamcrest import assert_that, contains_string, has_entries, has_string, not_

MOCK_RESPONSE = mock.MagicMock(
    status_code=200,
    text="sausages",
    content=b"content",
    json=mock.MagicMock(return_value={"a": "b"}),
    headers={"key": "value"},
    cookies={"name": "value"},
    elapsed=timedelta(seconds=1),
)


def test_response_matcher_status_code():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, response_with(status_code=200))
    assert_that(stub_response, not_(response_with(status_code=201)))
    assert_that(response_with(status_code=200), has_string("response with status_code: <200>"))
    assert_that(
        response_with(status_code=201),
        mismatches_with(stub_response, contains_string("was response with status code: <200>"),),
    )


def test_response_matcher_body():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, response_with(body="sausages"))
    assert_that(stub_response, not_(response_with(body="chips")))
    assert_that(response_with(body="chips"), has_string("response with body: 'chips'"))
    assert_that(
        response_with(body="chips"),
        mismatches_with(stub_response, contains_string("was response with body: 'sausages'"),),
    )


def test_response_matcher_content():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, response_with(content=b"content"))
    assert_that(stub_response, not_(response_with(content=b"chips")))
    assert_that(
        str(response_with(content=b"content")),
        contains_string("response with content: <b'content'>"),
    )
    assert_that(
        response_with(content=b"chips"),
        mismatches_with(stub_response, contains_string("was response with content: <b'content'>"),),
    )


def test_response_matcher_json():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, response_with(json={"a": "b"}))
    assert_that(stub_response, not_(response_with(json={"a": "c"})))
    assert_that(
        str(response_with(json={"a": "b"})), contains_string("response with json: <{'a': 'b'}>"),
    )
    assert_that(
        response_with(json=[1, 2, 4]),
        mismatches_with(stub_response, contains_string("was response with json: <{'a': 'b'}>"),),
    )


def test_response_matcher_headers():
    # Given
    response = MOCK_RESPONSE

    # When

    # Then
    assert_that(response, response_with(headers={"key": "value"}))
    assert_that(response, not_(response_with(headers={"key": "nope"})))
    assert_that(
        str(response_with(headers={"key": "value"})),
        contains_string("response with headers: <{'key': 'value'}"),
    )
    assert_that(
        response_with(headers={"key": "nope"}),
        mismatches_with(response, contains_string("was response with headers: <{'key': 'value'}"),),
    )


def test_response_matcher_cookies():
    # Given
    response = MOCK_RESPONSE

    # When

    # Then
    assert_that(response, is_response().with_cookies({"name": "value"}))
    assert_that(response, not_(is_response().with_cookies({"name": "nope"})))
    assert_that(
        str(is_response().with_cookies({"name": "value"})),
        contains_string("response with cookies: <{'name': 'value'}"),
    )
    assert_that(
        is_response().with_cookies({"name": "nope"}),
        mismatches_with(response, contains_string("was response with cookies: <{'name': 'value'}")),
    )


def test_response_matcher_elapsed():
    # Given
    response = MOCK_RESPONSE

    # When

    # Then
    assert_that(response, is_response().with_elapsed(timedelta(seconds=1)))
    assert_that(response, not_(is_response().with_elapsed(timedelta(seconds=60))))
    assert_that(
        str(is_response().with_elapsed(timedelta(seconds=1))),
        contains_string("response with elapsed: <0:00:01>"),
    )
    assert_that(
        is_response().with_elapsed(timedelta(seconds=60)),
        mismatches_with(response, contains_string("was response with elapsed: <0:00:01>")),
    )


# TODO history, encoding, url


def test_response_matcher_invalid_json():
    # Given
    stub_response = mock.MagicMock(
        status_code=200, text="body", content=b"content", headers={"key": "value"}
    )
    type(stub_response).json = mock.PropertyMock(side_effect=ValueError)

    # When

    # Then
    assert_that(stub_response, not_(response_with(json=[1, 2, 4])))
    assert_that(
        response_with(json=[1, 2, 4]),
        mismatches_with(stub_response, contains_string("was response with json: <None>"),),
    )


def test_redirect_to():
    # Given
    stub_response = mock.MagicMock(
        status_code=301, headers={"Location": UrlBuilder().with_path("/sausages").build()}
    )

    # When

    # Then
    assert_that(stub_response, redirects_to(url_with_path("/sausages")))
    assert_that(stub_response, not_(redirects_to(url_with_path("/bacon"))))
    assert_that(
        redirects_to(url_with_path("/sausages")),
        has_string("redirects to URL with path '/sausages'"),
    )


def test_response_matcher_builder():
    # Given
    stub_response = MOCK_RESPONSE
    matcher = (
        is_response()
        .with_status_code(200)
        .and_body("sausages")
        .and_content(b"content")
        .and_json(has_entries(a="b"))
        .and_headers(has_entries(key="value"))
    )
    mismatcher = is_response().with_body("kale").and_status_code(404)

    # When

    # Then
    assert_that(stub_response, matcher)
    assert_that(stub_response, not_(mismatcher))
    assert_that(
        matcher,
        has_string(
            "response with status_code: <200> "
            "body: 'sausages' "
            "content: <b'content'> "
            "json: a dictionary containing {'a': 'b'} "
            "headers: a dictionary containing {'key': 'value'}"
        ),
    )
    assert_that(
        mismatcher,
        mismatches_with(stub_response, contains_string("was response with status code: <200>"),),
    )
