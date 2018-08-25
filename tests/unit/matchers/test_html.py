from bs4 import BeautifulSoup
from hamcrest import assert_that, not_, contains_string, has_string, contains

from brunns.matchers.html import has_title, has_tag, has_class, tag_has_string, has_rows, has_table
from brunns.matchers.matcher import mismatches_with

HTML = """<html>
    <head><title>sausages</title></head>
    </body>
        <h1 class="bacon egg">chips</h1>
        <table id="squid" action="/">
            <thead>
                <tr><th>apples</th><th>oranges</th></tr>
            </thead>
            <tbody>
                <tr><td>foo</td><td>bar</td></tr>
                <tr><td>baz</td><td>qux</td></tr>
            </tbody>
        </table>
    </body>
</html>"""


def test_has_title():
    assert_that(HTML, has_title("sausages"))
    assert_that(HTML, not_(has_title("chips")))
    assert_that(HTML, has_title(contains_string("usage")))
    assert_that(has_title("sausages"), has_string("HTML with tag 'title' matching tag with string matching 'sausages'"))
    assert_that(has_title("chips"), mismatches_with(HTML, "got HTML with tag 'title' values [<title>sausages</title>]"))


def test_has_tag():
    assert_that(HTML, has_tag("h1", "chips"))
    assert_that(HTML, not_(has_tag("h1", "bananas")))
    assert_that(HTML, has_tag("h1", tag_has_string(contains_string("hip"))))
    assert_that(
        has_tag("h1", "sausages"), has_string("HTML with tag 'h1' matching tag with string matching 'sausages'")
    )
    assert_that(
        has_tag("h1", "sausages"),
        mismatches_with(HTML, "got HTML with tag 'h1' values [<h1 class=\"bacon egg\">chips</h1>]"),
    )


def test_has_class():
    assert_that(HTML, has_tag("h1", has_class("bacon")))
    assert_that(HTML, not_(has_tag("h1", has_class("bananas"))))
    assert_that(HTML, has_tag("h1", has_class(contains_string("aco"))))
    assert_that(has_class("bacon"), has_string("tag with class matching 'bacon'"))
    assert_that(
        has_tag("h1", has_class("bananas")),
        mismatches_with(HTML, "got HTML with tag 'h1' values [<h1 class=\"bacon egg\">chips</h1>]"),
    )


def test_table_has_row():
    # Given
    soup = BeautifulSoup(HTML, "html.parser")
    t = soup.table

    # Then
    assert_that(t, has_rows(contains(tag_has_string("foo"), tag_has_string("bar"))))
    assert_that(t, not_(has_rows(contains(tag_has_string("egg"), tag_has_string("chips")))))


def test_html_has_table():
    assert_that(HTML, has_table(has_rows(contains(tag_has_string("foo"), tag_has_string("bar")))))
    assert_that(HTML, not_(has_table(has_rows(contains(tag_has_string("egg"), tag_has_string("chips"))))))
