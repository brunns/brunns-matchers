# encoding=utf-8
from datetime import timedelta
from unittest import mock

from brunns.builder.internet import UrlBuilder as a_url  # type: ignore
from hamcrest import assert_that, contains_exactly, contains_string, has_entries, has_string, not_

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.object import between
from brunns.matchers.response import is_response, redirects_to
from brunns.matchers.url import is_url

MOCK_RESPONSE = mock.MagicMock(
    status_code=200,
    text="sausages",
    content=b"content",
    json=mock.MagicMock(return_value={"a": "b"}),
    headers={"key": "value"},
    cookies={"name": "value"},
    elapsed=timedelta(seconds=1),
    history=[
        mock.MagicMock(url=a_url().with_path("/path1").build()),
        mock.MagicMock(url=a_url().with_path("/path2").build()),
    ],
    url=a_url().with_path("/path0").build(),
    encoding="utf-8",
)


def test_response_matcher_status_code():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, is_response().with_status_code(200))
    assert_that(stub_response, not_(is_response().with_status_code(201)))
    assert_that(is_response().with_status_code(200), has_string("response with status_code: <200>"))
    assert_that(
        is_response().with_status_code(201),
        mismatches_with(stub_response, contains_string("was response with status code: was <200>")),
    )


def test_response_matcher_body():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, is_response().with_body("sausages"))
    assert_that(stub_response, not_(is_response().with_body("chips")))
    assert_that(is_response().with_body("chips"), has_string("response with body: 'chips'"))
    assert_that(
        is_response().with_body("chips"),
        mismatches_with(stub_response, contains_string("was response with body: was 'sausages'")),
    )


def test_response_matcher_content():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, is_response().with_content(b"content"))
    assert_that(stub_response, not_(is_response().with_content(b"chips")))
    assert_that(
        str(is_response().with_content(b"content")),
        contains_string("response with content: <b'content'>"),
    )
    assert_that(
        is_response().with_content(b"chips"),
        mismatches_with(
            stub_response, contains_string("was response with content: was <b'content'>")
        ),
    )


def test_response_matcher_json():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, is_response().with_json({"a": "b"}))
    assert_that(stub_response, not_(is_response().with_json({"a": "c"})))
    assert_that(
        str(is_response().with_json({"a": "b"})),
        contains_string("response with json: <{'a': 'b'}>"),
    )
    assert_that(
        is_response().with_json([1, 2, 4]),
        mismatches_with(stub_response, contains_string("was response with json: was <{'a': 'b'}>")),
    )


def test_response_matcher_headers():
    # Given
    response = MOCK_RESPONSE

    # When

    # Then
    assert_that(response, is_response().with_headers({"key": "value"}))
    assert_that(response, not_(is_response().with_headers({"key": "nope"})))
    assert_that(
        str(is_response().with_headers({"key": "value"})),
        contains_string("response with headers: <{'key': 'value'}"),
    )
    assert_that(
        is_response().with_headers({"key": "nope"}),
        mismatches_with(
            response, contains_string("was response with headers: was <{'key': 'value'}")
        ),
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
        mismatches_with(
            response, contains_string("was response with cookies: was <{'name': 'value'}")
        ),
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
        mismatches_with(response, contains_string("was response with elapsed: was <0:00:01>")),
    )


def test_response_matcher_history_and_url():
    # Given
    response = MOCK_RESPONSE

    # When

    # Then
    assert_that(
        response,
        is_response().with_history(
            contains_exactly(
                is_response().with_url(is_url().with_path("/path1")),
                is_response().with_url(is_url().with_path("/path2")),
            )
        ),
    )
    assert_that(
        response,
        not_(
            is_response().with_history(
                contains_exactly(
                    is_response().with_url(is_url().with_path("/path1")),
                    is_response().with_url(is_url().with_path("/path3")),
                )
            )
        ),
    )
    assert_that(
        str(
            is_response().with_history(
                contains_exactly(
                    is_response().with_url(is_url().with_path("/path1")),
                    is_response().with_url(is_url().with_path("/path2")),
                )
            )
        ),
        contains_string(
            "response with history: a sequence containing "
            "[response with url: URL with path: '/path1', response with url: URL with path: '/path2']"
        ),
    )
    assert_that(
        is_response().with_history(
            contains_exactly(
                is_response().with_url(is_url().with_path("/path1")),
                is_response().with_url(is_url().with_path("/path3")),
            )
        ),
        mismatches_with(
            response,
            contains_string(
                "was response with history: item 1: was response with url: was URL with path: was </path2>"
            ),
        ),
    )


def test_response_matcher_url():
    # Given
    response = MOCK_RESPONSE

    # When

    # Then
    assert_that(response, is_response().with_url(is_url().with_path("/path0")))
    assert_that(response, not_(is_response().with_url(is_url().with_path("/nope"))))
    assert_that(
        str(is_response().with_url(is_url().with_path("/path0"))),
        contains_string("response with url: URL with path: '/path0'"),
    )
    assert_that(
        is_response().with_url(is_url().with_path("/nope")),
        mismatches_with(
            response, contains_string("was response with url: was URL with path: was </path0>")
        ),
    )


def test_response_matcher_encoding():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, is_response().with_encoding("utf-8"))
    assert_that(stub_response, not_(is_response().with_encoding("ISO-8859-1")))
    assert_that(is_response().with_encoding("utf-8"), has_string("response with encoding: 'utf-8'"))
    assert_that(
        is_response().with_encoding("ISO-8859-1"),
        mismatches_with(stub_response, contains_string("was response with encoding: was 'utf-8'")),
    )


def test_response_matcher_invalid_json():
    # Given
    stub_response = mock.MagicMock(
        status_code=200, text="body", content=b"content", headers={"key": "value"}
    )
    type(stub_response).json = mock.PropertyMock(side_effect=ValueError)

    # When

    # Then
    assert_that(stub_response, not_(is_response().with_json([1, 2, 4])))
    assert_that(
        is_response().with_json([1, 2, 4]),
        mismatches_with(stub_response, contains_string("was response with json: was <None>")),
    )


def test_redirect_to():
    # Given
    stub_response = mock.MagicMock(
        status_code=301, headers={"Location": a_url().with_path("/sausages").build()}
    )

    # When

    # Then
    assert_that(stub_response, redirects_to(is_url().with_path("/sausages")))
    assert_that(stub_response, not_(redirects_to(is_url().with_path("/bacon"))))
    assert_that(
        redirects_to(is_url().with_path("/sausages")),
        has_string("redirects to URL with path: '/sausages'"),
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
        .and_cookies(has_entries(name="value"))
        .and_elapsed(between(timedelta(seconds=1), timedelta(minutes=1)))
        .and_history(
            contains_exactly(
                is_response().with_url(is_url().with_path("/path1")),
                is_response().with_url(is_url().with_path("/path2")),
            )
        )
        .and_url(is_url().with_path("/path0"))
        .and_encoding("utf-8")
    )
    mismatcher = is_response().with_body("kale").and_status_code(404)

    # When

    # Then
    assert_that(stub_response, matcher)
    assert_that(stub_response, not_(mismatcher))
    assert_that(
        matcher,
        has_string(
            "response with "
            "status_code: <200> "
            "body: 'sausages' "
            "content: <b'content'> "
            "json: a dictionary containing {'a': 'b'} "
            "headers: a dictionary containing {'key': 'value'} "
            "cookies: a dictionary containing {'name': 'value'} "
            "elapsed: (a value greater than or equal to <0:00:01> and a value less than or equal to <0:01:00>) "
            "history: a sequence containing "
            "[response with url: URL with path: '/path1', response with url: URL with path: '/path2'] "
            "url: URL with path: '/path0' "
            "encoding: 'utf-8'"
        ),
    )
    assert_that(
        mismatcher,
        mismatches_with(
            stub_response,
            contains_string("was response with status code: was <200> body: was 'sausages'"),
        ),
    )
