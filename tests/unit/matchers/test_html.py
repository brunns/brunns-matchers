from hamcrest import assert_that, not_, contains_string, has_string

from brunns.matchers.html import has_title, has_tag, has_class, tag_has_string
from brunns.matchers.matcher import mismatches_with

HTML = """<html>
    <head><title>sausages</title></head>
    </body>
        <h1 class="bacon egg">chips</h1>
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


# TODO Row in table
