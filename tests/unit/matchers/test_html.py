from hamcrest import assert_that, not_, contains_string, has_string

from brunns.matchers.html import has_title
from brunns.matchers.matcher import mismatches_with


def test_has_title():
    # Given
    html = """<html><head><title>sausages</title></head></html>"""

    # When

    # Then
    assert_that(html, has_title("sausages"))
    assert_that(html, not_(has_title("chips")))
    assert_that(html, has_title(contains_string("usage")))
    assert_that(has_title("sausages"), has_string("HTML with tag 'title' matching tag matching 'sausages'"))
    assert_that(has_title("chips"), mismatches_with(html, "got HTML with tag 'title'was <[<title>sausages</title>]>"))
