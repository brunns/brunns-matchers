# encoding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

from hamcrest import assert_that, has_string, not_, matches_regexp

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.response import response_with


def test_response_matcher():
    # Given
    response = MagicMock(status_code=200, text="sausages", headers={})

    # When

    # Then
    assert_that(response, response_with(status_code=200, body="sausages"))
    assert_that(response, not_(response_with(status_code=200, body="chips")))
    assert_that(
        response_with(status_code=200, body="chips"), has_string("response with status_code: <200> body: 'chips'")
    )
    assert_that(
        response_with(status_code=200, body="chips"),
        mismatches_with(
            response, matches_regexp(r"was response with status code: <200> body: ['<]sausages['>] headers: <{}>")
        ),
    )
