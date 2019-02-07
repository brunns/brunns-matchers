# encoding=utf-8
import warnings

from bs4 import BeautifulSoup
from hamcrest import (
    assert_that,
    not_,
    contains_string,
    has_string,
    contains,
    anything,
    matches_regexp,
    has_properties,
    has_item,
    has_entries,
    starts_with,
    all_of,
)

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
    has_row,
    has_nth_row,
    has_link,
    has_id,
    has_attributes,
)
from brunns.matchers.matcher import mismatches_with
from brunns.matchers.url import to_host, with_path
from tests.utils.string_utils import repr_no_unicode_prefix

HTML = """<html>
    <head>
        <title>sausages</title>
        <meta charset="utf-8"/>
        </head>
    </body>
        <h1 class="bacon egg">chips</h1>
        <h2>what is &mdash; this</h2>
        <a id="a-link" class="link-me-baby" href="https://brunni.ng">A link</a>
        <div id="fish" class="banana grapes"><p>Some text.</p></div>
        <table id="squid" action="/">
            <thead>
                <tr><th>apples</th><th>oranges</th></tr>
            </thead>
            <tbody>
                <tr><td>foo</td><td>bar</td></tr>
                <tr><td>baz</td><td>qux</td></tr>
                <tr class="bazz"><td>fizz</td><td>buzz</td></tr>
                <tr class="eden"><td>Adam</td><td><a href="http://thepub.com/thebar">Steve</a></td></tr>
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
    assert_that(
        should_match,
        has_string(matches_regexp(r"HTML with tag name=['<]title['>] matching tag with string matching 'sausages'")),
    )
    assert_that(
        should_not_match,
        mismatches_with(
            HTML, matches_regexp(r"got HTML with tag name=['<]title['>] values \['<title>sausages</title>'\]")
        ),
    )


def test_has_named_tag():
    should_match = has_named_tag("h1", "chips")
    should_not_match = has_named_tag("h1", "bananas")

    assert_that(HTML, should_match)
    assert_that(HTML, not_(should_not_match))
    assert_that(HTML, has_named_tag("h1", tag_has_string(contains_string("hip"))))
    assert_that(
        should_match,
        has_string(matches_regexp(r"HTML with tag name=['<]h1['>] matching tag with string matching 'chips'")),
    )
    assert_that(
        should_not_match,
        mismatches_with(
            HTML, matches_regexp(r"got HTML with tag name=['<]h1['>] values \['<h1 class=\"bacon egg\">chips</h1>'\]")
        ),
    )


def test_mdash():
    assert_that(HTML, has_named_tag("h2", "what is — this"))
    assert_that(
        has_named_tag("h2", "what is this"),
        mismatches_with(
            HTML, matches_regexp(r"got HTML with tag name=['<]h2['>] values \['<h2>what is (\\u2014|—) this</h2>'\]")
        ),
    )


def test_has_tag_deprecated():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        assert_that(HTML, has_tag("h1", "chips"))

        assert_that(
            w,
            has_item(
                has_properties(category=DeprecationWarning, message=has_string("deprecated - use has_named_tag()"))
            ),
        )


def test_has_nth_row_deprecated():
    soup = BeautifulSoup(HTML, "html.parser")
    table = soup.table
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        assert_that(table, has_nth_row(0, anything()))

        assert len(w) == 1
        assert issubclass(w[-1].category, DeprecationWarning)
        assert "deprecated - use has_row(index_matches=index)" in str(w[-1].message)


def test_has_class():
    should_match = has_class("bacon")
    should_not_match = has_class("bananas")

    assert_that(HTML, has_named_tag("h1", should_match))
    assert_that(HTML, not_(has_named_tag("h1", should_not_match)))
    assert_that(HTML, has_named_tag("h1", has_class(contains_string("aco"))))
    assert_that(should_match, has_string("tag with class matching 'bacon'"))
    assert_that(
        has_named_tag("h1", should_not_match),
        mismatches_with(
            HTML, matches_regexp(r"got HTML with tag name=['<]h1['>] values \['<h1 class=\"bacon egg\">chips</h1>'\]")
        ),
    )


def test_has_id_tag():
    # Given
    should_match = has_id_tag("fish", has_class("banana"))
    should_not_match_1 = has_id_tag("fish", has_class("foo"))
    should_not_match_2 = has_id_tag("grrgug", anything())

    assert_that(HTML, should_match)
    assert_that(HTML, not_(should_not_match_1))
    assert_that(HTML, not_(should_not_match_2))
    assert_that(
        should_match,
        has_string(matches_regexp(r"HTML with tag id=['<]fish['>] matching tag with class matching 'banana'")),
    )
    assert_that(
        should_not_match_1,
        mismatches_with(
            HTML,
            matches_regexp(
                r"""got HTML with tag id=['<]fish['>] values """
                r"""\['<div class="banana grapes" id="fish"><p>Some text.</p></div>'\]"""
            ),
        ),
    )
    assert_that(
        should_not_match_2, mismatches_with(HTML, matches_regexp(r"got HTML with tag id=['<]grrgug['>] values \[\]"))
    )


def test_table_has_row_cells():
    # Given
    soup = BeautifulSoup(HTML, "html.parser")
    table = soup.table
    should_match = has_row(cells_match=contains(tag_has_string("foo"), tag_has_string("bar")))
    should_not_match = has_row(cells_match=contains(tag_has_string("egg"), tag_has_string("chips")))

    # Then
    assert_that(table, should_match)
    assert_that(table, not_(should_not_match))
    assert_that(
        should_match,
        has_string(
            "table with row "
            "cells matching a sequence containing [tag with string matching 'foo', tag with string matching 'bar']"
        ),
    )
    assert_that(should_not_match, mismatches_with(table, starts_with("was {0}".format(table))))


def test_has_row():
    # Given
    soup = BeautifulSoup(HTML, "html.parser")
    table = soup.table
    should_match = has_row(
        index_matches=2,
        row_matches=has_class("bazz"),
        cells_match=contains(tag_has_string("fizz"), tag_has_string("buzz")),
    )
    should_not_match_1 = has_row(
        index_matches=2,
        row_matches=has_class("bazz"),
        cells_match=contains(tag_has_string("egg"), tag_has_string("chips")),
    )
    should_not_match_2 = has_row(
        index_matches=3,
        row_matches=has_class("bazz"),
        cells_match=contains(tag_has_string("fizz"), tag_has_string("buzz")),
    )
    should_not_match_3 = has_row(
        index_matches=2,
        row_matches=has_class("eden"),
        cells_match=contains(tag_has_string("fizz"), tag_has_string("buzz")),
    )

    # Then
    assert_that(table, should_match)
    assert_that(table, not_(should_not_match_1))
    assert_that(table, not_(should_not_match_2))
    assert_that(table, not_(should_not_match_3))
    assert_that(
        should_match,
        has_string(
            "table with row "
            "cells matching a sequence containing [tag with string matching 'fizz', tag with string matching 'buzz'] "
            "row matching tag with class matching 'bazz' "
            "index matching <2>"
        ),
    )
    assert_that(
        has_row(row_matches=has_class("banana")),
        has_string("table with row row matching tag with class matching 'banana'"),
    )
    assert_that(
        should_not_match_1,
        mismatches_with(
            table,
            all_of(
                starts_with("was {0}".format(table)),
                contains_string("found rows:"),
                contains_string("<tr><td>baz</td><td>qux</td></tr>"),
            ),
        ),
    )


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
            "table with header row cells matching a sequence containing "
            "[tag with string matching 'apples', tag with string matching 'oranges']"
        ),
    )
    assert_that(should_not_match, mismatches_with(table, starts_with("was {0}".format(table))))


def test_html_has_table():
    should_match = has_table(has_rows(contains(tag_has_string("foo"), tag_has_string("bar"))))
    should_not_match = has_table(has_rows(contains(tag_has_string("egg"), tag_has_string("chips"))))

    assert_that(HTML, should_match)
    assert_that(HTML, not_(should_not_match))
    assert_that(should_match, has_string("row matching {0}".format(should_match.matcher)))
    assert_that(should_not_match, mismatches_with(HTML, "was {0}".format(repr_no_unicode_prefix(HTML))))


def test_html_without_table():
    html = "<html/>"
    matcher = has_table(anything())

    assert_that(html, not_(matcher))
    assert_that(matcher, mismatches_with(html, "was '<html/>'"))


def test_has_id():
    should_match = has_named_tag("div", has_id("fish"))
    should_not_match = has_named_tag("div", has_id("wanda"))

    assert_that(HTML, should_match)
    assert_that(HTML, not_(should_not_match))
    assert_that(
        should_match,
        has_string(
            "HTML with tag name='div' matching tag with attributes matching " "a dictionary containing ['id': 'fish']"
        ),
    )
    assert_that(
        should_not_match,
        mismatches_with(
            HTML,
            """got HTML with tag name='div' """
            """values ['<div class="banana grapes" id="fish"><p>Some text.</p></div>']""",
        ),
    )


def test_has_attributes():
    should_match = has_named_tag("div", has_attributes(has_entries(id="fish")))
    should_not_match = has_named_tag("div", has_attributes(has_entries(id="wanda")))

    assert_that(HTML, should_match)
    assert_that(HTML, not_(should_not_match))
    assert_that(should_match, has_string(contains_string("attributes matching a dictionary containing {'id': 'fish'}")))
    assert_that(
        should_not_match,
        mismatches_with(
            HTML,
            """got HTML with tag name='div' """
            """values ['<div class="banana grapes" id="fish"><p>Some text.</p></div>']""",
        ),
    )


def test_has_link():
    # Given
    should_match = has_link(href=to_host("brunni.ng"))
    should_not_match_1 = has_link(href=to_host("example.com"))

    assert_that(HTML, should_match)
    assert_that(HTML, not_(should_not_match_1))


def test_has_row_with_link():
    # Given
    soup = BeautifulSoup(HTML, "html.parser")
    table = soup.table
    should_match = has_row(index_matches=3, cells_match=has_item(has_link(href=with_path("/thebar"))))
    should_not_match_1 = has_row(index_matches=3, cells_match=has_item(has_link(href=with_path("/cup-of-tea"))))

    # Then
    assert_that(table, should_match)
    assert_that(table, not_(should_not_match_1))

    assert_that(
        should_match,
        has_string(
            "table with row cells matching a sequence containing HTML with tag matching "
            "tag with name matching 'a' "
            "attributes matching (a dictionary containing ['href': URL with path '/thebar'] and ANYTHING) "
            "index matching <3>"
        ),
    )
