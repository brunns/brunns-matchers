from brunns.builder.internet import UrlBuilder as a_url  # type: ignore[attr-defined]
from hamcrest import assert_that, contains_string, has_entries, has_string, not_
from mockito import mock

from brunns.matchers.matcher import matches_with, mismatches_with
from brunns.matchers.url import is_url
from brunns.matchers.werkzeug import is_werkzeug_response, redirects_to

MOCK_RESPONSE = mock(
    {
        "status_code": 200,
        "text": "sausages",
        "json": {"a": "b"},
        "headers": {"key": "value"},
        "mimetype": "text/xml",
    },
)


def test_response_matcher_status_code():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, is_werkzeug_response().with_status_code(200))
    assert_that(stub_response, not_(is_werkzeug_response().with_status_code(201)))
    assert_that(is_werkzeug_response().with_status_code(200), has_string("response with status code: <200>"))
    assert_that(
        is_werkzeug_response().with_status_code(201),
        mismatches_with(stub_response, contains_string("was response with status code: was <200>")),
    )
    assert_that(
        is_werkzeug_response().with_status_code(200),
        matches_with(stub_response, "was response with status code: was <200>"),
    )


def test_response_matcher_text():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, is_werkzeug_response().with_text("sausages"))
    assert_that(stub_response, not_(is_werkzeug_response().with_text("chips")))
    assert_that(is_werkzeug_response().with_text("chips"), has_string("response with text: 'chips'"))
    assert_that(
        is_werkzeug_response().with_text("chips"),
        mismatches_with(stub_response, contains_string("was response with text: was 'sausages'")),
    )
    assert_that(
        is_werkzeug_response().with_text("sausages"),
        matches_with(stub_response, contains_string("was response with text: was 'sausages'")),
    )


def test_response_matcher_mimetype():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, is_werkzeug_response().with_mimetype("text/xml"))
    assert_that(stub_response, not_(is_werkzeug_response().with_mimetype("text/json")))
    assert_that(
        is_werkzeug_response().with_mimetype("text/json"),
        has_string("response with mimetype: 'text/json'"),
    )
    assert_that(
        is_werkzeug_response().with_mimetype("text/json"),
        mismatches_with(stub_response, contains_string("was response with mimetype: was 'text/xml'")),
    )
    assert_that(
        is_werkzeug_response().with_mimetype("text/xml"),
        matches_with(stub_response, contains_string("was response with mimetype: was 'text/xml'")),
    )


def test_response_matcher_json():
    # Given
    stub_response = MOCK_RESPONSE

    # When

    # Then
    assert_that(stub_response, is_werkzeug_response().with_json({"a": "b"}))
    assert_that(stub_response, not_(is_werkzeug_response().with_json({"a": "c"})))
    assert_that(
        str(is_werkzeug_response().with_json({"a": "b"})),
        contains_string("response with json: <{'a': 'b'}>"),
    )
    assert_that(
        is_werkzeug_response().with_json([1, 2, 4]),
        mismatches_with(stub_response, contains_string("was response with json: was <{'a': 'b'}>")),
    )
    assert_that(
        is_werkzeug_response().with_json({"a": "b"}),
        matches_with(stub_response, contains_string("was response with json: was <{'a': 'b'}>")),
    )


def test_response_matcher_headers():
    # Given
    response = MOCK_RESPONSE

    # When

    # Then
    assert_that(response, is_werkzeug_response().with_headers({"key": "value"}))
    assert_that(response, not_(is_werkzeug_response().with_headers({"key": "nope"})))
    assert_that(
        str(is_werkzeug_response().with_headers({"key": "value"})),
        contains_string("response with headers: <{'key': 'value'}"),
    )
    assert_that(
        is_werkzeug_response().with_headers({"key": "nope"}),
        mismatches_with(response, contains_string("was response with headers: was <{'key': 'value'}")),
    )
    assert_that(
        is_werkzeug_response().with_headers({"key": "value"}),
        matches_with(response, contains_string("was response with headers: was <{'key': 'value'}")),
    )


def test_redirect_to():
    # Given
    stub_response = mock(
        {
            "status_code": 301,
            "headers": {"Location": a_url().with_path("/sausages").build()},
        },
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
        is_werkzeug_response()
        .with_status_code(200)
        .and_text("sausages")
        .and_mimetype("text/xml")
        .and_json(has_entries(a="b"))
        .and_headers(has_entries(key="value"))
    )
    mismatcher = is_werkzeug_response().with_text("kale").and_status_code(404)

    # When

    # Then
    assert_that(stub_response, matcher)
    assert_that(stub_response, not_(mismatcher))
    assert_that(
        matcher,
        has_string(
            "response with "
            "status code: <200> "
            "text: 'sausages' "
            "mimetype: 'text/xml' "
            "json: a dictionary containing {'a': 'b'} "
            "headers: a dictionary containing {'key': 'value'}",
        ),
    )
    assert_that(
        mismatcher,
        mismatches_with(
            stub_response,
            contains_string("was response with status code: was <200> text: was 'sausages'"),
        ),
    )
    assert_that(
        matcher,
        matches_with(
            stub_response,
            contains_string("was response with status code: was <200> text: was 'sausages'"),
        ),
    )
