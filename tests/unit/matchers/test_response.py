# encoding=utf-8
from unittest import mock
from hamcrest import assert_that, has_string, not_, matches_regexp

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.response import response_with


def test_response_matcher_status_code():
    # Given
    response = mock.MagicMock(
        status_code=200, text="body", content=b"content", json=[1, 2, 3], headers={"key": "value"}
    )

    # When

    # Then
    assert_that(response, response_with(status_code=200))
    assert_that(response, not_(response_with(status_code=201)))
    assert_that(response_with(status_code=200), has_string("response with status_code: <200>"))
    assert_that(
        response_with(status_code=201),
        mismatches_with(
            response,
            matches_regexp(
                r"was response with status code: <200> body: ['<]body['>] content: <?b?'content'?>? "
                r"json: <\[1, 2, 3\]> headers: <{u?'key': u?'value'}>"
            ),
        ),
    )


def test_response_matcher_body():
    # Given
    response = mock.MagicMock(
        status_code=200, text="sausages", content=b"content", json=[1, 2, 3], headers={"key": "value"}
    )

    # When

    # Then
    assert_that(response, response_with(body="sausages"))
    assert_that(response, not_(response_with(body="chips")))
    assert_that(response_with(body="chips"), has_string("response with body: 'chips'"))
    assert_that(
        response_with(body="chips"),
        mismatches_with(
            response,
            matches_regexp(
                r"was response with status code: <200> body: ['<]sausages['>] content: <?b?'content'?>? "
                r"json: <\[1, 2, 3\]> headers: <{u?'key': u?'value'}>"
            ),
        ),
    )


def test_response_matcher_content():
    # Given
    response = mock.MagicMock(
        status_code=200, text="body", content=b"content", json=[1, 2, 3], headers={"key": "value"}
    )

    # When

    # Then
    assert_that(response, response_with(content=b"content"))
    assert_that(response, not_(response_with(content=b"chips")))
    assert_that(str(response_with(content=b"content")), matches_regexp(r"response with content: <?b?'content'>?"))
    assert_that(
        response_with(content=b"chips"),
        mismatches_with(
            response,
            matches_regexp(
                r"was response with status code: <200> body: ['<]body['>] content: <?b?'content'?>? "
                r"json: <\[1, 2, 3\]> headers: <{u?'key': u?'value'}>"
            ),
        ),
    )


def test_response_matcher_json():
    # Given
    response = mock.MagicMock(
        status_code=200, text="body", content=b"content", json=[1, 2, 3], headers={"key": "value"}
    )

    # When

    # Then
    assert_that(response, response_with(json=[1, 2, 3]))
    assert_that(response, not_(response_with(json=[1, 2, 4])))
    assert_that(str(response_with(json=[1, 2, 3])), matches_regexp(r"response with json: <\[1, 2, 3\]>"))
    assert_that(
        response_with(json=[1, 2, 4]),
        mismatches_with(
            response,
            matches_regexp(
                r"was response with status code: <200> body: ['<]body['>] content: <?b?'content'?>? "
                r"json: <\[1, 2, 3\]> headers: <{u?'key': u?'value'}>"
            ),
        ),
    )


def test_response_matcher_invalid_json():
    # Given
    response = mock.MagicMock(status_code=200, text="body", content=b"content", headers={"key": "value"})
    type(response).json = mock.PropertyMock(side_effect=ValueError)

    # When

    # Then
    assert_that(response, not_(response_with(json=[1, 2, 4])))
    assert_that(
        response_with(json=[1, 2, 4]),
        mismatches_with(
            response,
            matches_regexp(
                r"was response with status code: <200> body: ['<]body['>] content: <?b?'content'?>? "
                r"json: <None> headers: <{u?'key': u?'value'}>"
            ),
        ),
    )
