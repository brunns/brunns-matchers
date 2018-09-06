import warnings

from bs4 import BeautifulSoup
from hamcrest import assert_that, not_, contains_string, has_string, contains, anything

from brunns.matchers.html import (
    has_title,
    has_named_tag,
    has_class,
    tag_has_string,
    has_rows,
    has_table,
    has_header_row,
    has_tag,
    has_id_tag,
)
from brunns.matchers.matcher import mismatches_with

HTML = """<html>
    <head><title>sausages</title></head>
    </body>
        <h1 class="bacon egg">chips</h1>
        <div id="fish" class="banana grapes"><p>Some text.</p></div>
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
    should_match = has_title("sausages")
    should_not_match = has_title("chips")

    assert_that(HTML, should_match)
    assert_that(HTML, not_(should_not_match))
    assert_that(HTML, has_title(contains_string("usage")))
    assert_that(should_match, has_string("HTML with tag name='title' matching tag with string matching 'sausages'"))
    assert_that(
        should_not_match, mismatches_with(HTML, "got HTML with tag name='title' values [<title>sausages</title>]")
    )


def test_has_named_tag():
    should_match = has_named_tag("h1", "chips")
    should_not_match = has_named_tag("h1", "bananas")

    assert_that(HTML, should_match)
    assert_that(HTML, not_(should_not_match))
    assert_that(HTML, has_named_tag("h1", tag_has_string(contains_string("hip"))))
    assert_that(should_match, has_string("HTML with tag name='h1' matching tag with string matching 'chips'"))
    assert_that(
        should_not_match,
        mismatches_with(HTML, "got HTML with tag name='h1' values [<h1 class=\"bacon egg\">chips</h1>]"),
    )


def test_has_tag_deprecated():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        assert_that(HTML, has_tag("h1", "chips"))

        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated - use has_named_tag()" in str(w[-1].message)


def test_has_class():
    should_match = has_class("bacon")
    should_not_match = has_class("bananas")

    assert_that(HTML, has_named_tag("h1", should_match))
    assert_that(HTML, not_(has_named_tag("h1", should_not_match)))
    assert_that(HTML, has_named_tag("h1", has_class(contains_string("aco"))))
    assert_that(should_match, has_string("tag with class matching 'bacon'"))
    assert_that(
        has_named_tag("h1", should_not_match),
        mismatches_with(HTML, "got HTML with tag name='h1' values [<h1 class=\"bacon egg\">chips</h1>]"),
    )


def test_has_id_tag():
    # Given
    should_match = has_id_tag("fish", has_class("banana"))
    should_not_match_1 = has_id_tag("fish", has_class("foo"))
    should_not_match_2 = has_id_tag("grrgug", anything())

    assert_that(HTML, should_match)
    assert_that(HTML, not_(should_not_match_1))
    assert_that(HTML, not_(should_not_match_2))
    assert_that(should_match, has_string("HTML with tag id='fish' matching tag with class matching 'banana'"))
    assert_that(
        should_not_match_1,
        mismatches_with(
            HTML,
            """got HTML with tag id='fish' values [<div class="banana grapes" id="fish"><p>Some text.</p></div>]""",
        ),
    )
    assert_that(should_not_match_2, mismatches_with(HTML, "got HTML with tag id='grrgug' values []"))


def test_table_has_row():
    # Given
    soup = BeautifulSoup(HTML, "html.parser")
    table = soup.table
    should_match = has_rows(contains(tag_has_string("foo"), tag_has_string("bar")))
    should_not_match = has_rows(contains(tag_has_string("egg"), tag_has_string("chips")))

    # Then
    assert_that(table, should_match)
    assert_that(table, not_(should_not_match))
    assert_that(
        should_match,
        has_string(
            "table with row matching a sequence containing "
            "[tag with string matching 'foo', tag with string matching 'bar']"
        ),
    )
    assert_that(should_not_match, mismatches_with(table, "was {0}".format(table)))


def test_table_has_header_row():
    # Given
    soup = BeautifulSoup(HTML, "html.parser")
    table = soup.table
    should_match = has_header_row(contains(tag_has_string("apples"), tag_has_string("oranges")))
    should_not_match = has_header_row(contains(tag_has_string("foo"), tag_has_string("bar")))

    # Then
    assert_that(table, should_match)
    assert_that(table, not_(should_not_match))
    assert_that(
        should_match,
        has_string(
            "table with header row matching a sequence containing "
            "[tag with string matching 'apples', tag with string matching 'oranges']"
        ),
    )
    assert_that(should_not_match, mismatches_with(table, "was {0}".format(table)))


def test_html_has_table():
    should_match = has_table(has_rows(contains(tag_has_string("foo"), tag_has_string("bar"))))
    should_not_match = has_table(has_rows(contains(tag_has_string("egg"), tag_has_string("chips"))))

    assert_that(HTML, should_match)
    assert_that(HTML, not_(should_not_match))
    assert_that(should_match, has_string("row matching {0}".format(should_match.matcher)))
    assert_that(should_not_match, mismatches_with(HTML, "was {0!r}".format(HTML)))


def test_html_without_table():
    html = "<html/>"
    matcher = has_table(anything())

    assert_that(html, not_(matcher))
    assert_that(matcher, mismatches_with(html, "was '<html/>'"))
