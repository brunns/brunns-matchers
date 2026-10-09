Examples of usage
=================

The "brunns.matchers" package
-----------------------------

The "brunns.matchers.bytestring" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Code under test:

.. code:: python

    def my_function(a_string: str) -> bytes:
        return a_string.upper().encode("utf-8")

Test:

.. code:: python

    from hamcrest import assert_that
    from brunns.matchers.bytestring import contains_bytestring

    def test_bytestrings():
        # Given
        a_string = "hello"

        # When
        actual = my_function(a_string)

        # Then
        assert_that(actual, contains_bytestring(b"ELL"))

The "brunns.matchers.data" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import json

    from brunns.matchers.data import json_matching
    from hamcrest import assert_that, contains_exactly, not_


    def make_data() -> str:
        return json.dumps([1, 2, 3])


    def test_json():
        # Given
        actual = make_data()

        # Then
        assert_that(actual, json_matching([1, 2, 3]))
        assert_that(actual, json_matching(contains_exactly(1, 2, 3)))
        assert_that(actual, not_(json_matching([1, 2, 5])))

The "brunns.matchers.datetime" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import datetime

    from brunns.matchers.datetime import is_weekday
    from hamcrest import assert_that, not_


    def test_weekday():
        # 1968-07-19 is a Friday; 1968-07-21 is a Sunday.
        assert_that(datetime.date(1968, 7, 19), is_weekday())
        assert_that(datetime.date(1968, 7, 21), not_(is_weekday()))

The "brunns.matchers.dbapi" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import sqlite3

    from brunns.matchers.dbapi import has_table, has_table_with_rows
    from hamcrest import assert_that, contains_inanyorder, has_properties, not_


    def make_db() -> sqlite3.Connection:
        db = sqlite3.connect(":memory:")
        db.execute("CREATE TABLE sausages (kind VARCHAR, rating INT);")
        for kind, rating in (("cumberland", 10), ("vegetarian", 0), ("lincolnshire", 9)):
            db.execute("INSERT INTO sausages VALUES (?, ?);", (kind, rating))
        db.commit()
        return db


    def test_db():
        # Given
        db = make_db()

        # Then
        assert_that(db, has_table("sausages"))
        assert_that(db, not_(has_table("bacon")))
        assert_that(
            db,
            has_table_with_rows(
                "sausages",
                contains_inanyorder(
                    has_properties(kind="cumberland"),
                    has_properties(kind="lincolnshire"),
                    has_properties(kind="vegetarian"),
                ),
            ),
        )

The "brunns.matchers.html" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The HTML matchers require the ``html`` extra (``pip install brunns-matchers[html]``).

.. code:: python

    from brunns.matchers.html import (
        has_attributes,
        has_class,
        has_header_row,
        has_id,
        has_id_tag,
        has_image,
        has_link,
        has_named_tag,
        has_row,
        has_table,
        has_title,
        tag_has_string,
    )
    from brunns.matchers.url import is_url
    from bs4 import BeautifulSoup
    from hamcrest import assert_that, contains_exactly, has_entries, not_


    HTML = """\
    <html>
        <head>
            <title>sausages</title>
        </head>
        <body>
            <h1 class="bacon egg">chips</h1>
            <a id="a-link" class="link-me-baby" href="https://brunni.ng">A link</a>
            <div id="fish" class="banana">some text</div>
            <img src="https://brunni.ng/some.png"/>
            <table>
                <thead>
                    <tr><th>apples</th><th>oranges</th></tr>
                </thead>
                <tbody>
                    <tr><td>foo</td><td>bar</td></tr>
                    <tr class="bazz"><td>fizz</td><td>buzz</td></tr>
                </tbody>
            </table>
        </body>
    </html>
    """


    def test_html():
        # Tags by name, by id, and links / images.
        assert_that(HTML, has_title("sausages"))
        assert_that(HTML, not_(has_title("bacon")))
        assert_that(HTML, has_named_tag("h1", "chips"))
        assert_that(HTML, has_named_tag("h1", has_class("bacon")))
        assert_that(HTML, has_id_tag("fish", has_class("banana")))
        assert_that(HTML, has_named_tag("div", has_id("fish")))
        assert_that(HTML, has_named_tag("div", has_attributes(has_entries(id="fish"))))
        assert_that(HTML, has_link(href=is_url().with_host("brunni.ng")))
        assert_that(HTML, has_image(src="https://brunni.ng/some.png"))

        # Tables, rows, and header rows.
        assert_that(HTML, has_table(has_row(contains_exactly(tag_has_string("foo"), tag_has_string("bar")))))

        table = BeautifulSoup(HTML, "html.parser").table
        assert_that(
            table,
            has_row(
                index_matches=1,
                row_matches=has_class("bazz"),
                cells_match=contains_exactly(tag_has_string("fizz"), tag_has_string("buzz")),
            ),
        )
        assert_that(table, has_header_row(contains_exactly(tag_has_string("apples"), tag_has_string("oranges"))))

The "brunns.matchers.matcher" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

These matchers test *other* matchers -- useful when writing tests for your own custom matchers.

.. code:: python

    from brunns.matchers.matcher import matches, matches_with, mismatches, mismatches_with
    from hamcrest import assert_that, contains_string


    def test_matchers():
        matcher = contains_string("Banana")

        # matches / mismatches: did the matcher accept / reject the value?
        assert_that(matcher, matches("Banana"))
        assert_that(matcher, mismatches("Apple"))

        # The *_with variants also describe the text reported on match / mismatch.
        assert_that(matcher, matches_with("Banana", "was 'Banana'"))
        assert_that(matcher, mismatches_with("Apple", "was 'Apple'"))

The "brunns.matchers.meta" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Subclassing :class:`~brunns.matchers.meta.BaseAutoMatcher` with a domain type generates
``with_<field>()`` / ``and_<field>()`` builders for every annotated field, so you can build
a fluent matcher for a dataclass or ``pydantic`` model.

.. code:: python

    from dataclasses import dataclass

    from brunns.matchers.meta import BaseAutoMatcher
    from hamcrest import assert_that, not_, starts_with


    @dataclass
    class Status:
        id: int
        code: str
        reason: str | None = None


    class StatusMatcher(BaseAutoMatcher[Status]):
        pass


    def test_meta():
        status = Status(id=99, code="ACTIVE")

        assert_that(status, StatusMatcher().with_code(starts_with("ACT")).and_reason(None))
        assert_that(status, not_(StatusMatcher().with_id(42)))

The "brunns.matchers.mock" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from brunns.matchers.mock import call_has_arg, call_has_args, has_call
    from hamcrest import assert_that, contains_string, not_
    from unittest import mock


    def test_mocks():
        m = mock.MagicMock()
        m("first", "second", "third", key="forth")
        call = m.mock_calls[0]

        # call_has_arg / call_has_args inspect a single recorded call.
        assert_that(call, call_has_arg(1, "second"))
        assert_that(call, call_has_arg(1, contains_string("eco")))      # "second" contains "eco"
        assert_that(call, call_has_args("first", "second", "third", key="forth"))
        assert_that(call, not_(call_has_args("first", "second", "third", key="banana")))

        # has_call checks whether a mock was ever called a particular way.
        method = m.m
        method("first")
        assert_that(method, has_call(call_has_args("first")))

The "brunns.matchers.object" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from brunns.matchers.object import (
        between,
        false,
        has_identical_properties_to,
        has_repr,
        true,
    )
    from hamcrest import assert_that, contains_string, not_


    class Point:
        def __init__(self, x: int, y: int) -> None:
            self.x = x
            self.y = y


    def test_object():
        # repr() of the object.
        assert_that([1, "2"], has_repr(contains_string("[1, '2']")))

        # Truthiness / falsiness.
        assert_that([1], true())
        assert_that([], false())

        # Ranges (inclusive by default; pass *_inclusive=False to exclude an endpoint).
        assert_that(2, between(1, 3))
        assert_that(1, not_(between(1, 3, lower_inclusive=False)))

        # Structural comparison of an object's public attributes / properties.
        assert_that(Point(1, 2), has_identical_properties_to(Point(1, 2)))

The "brunns.matchers.path" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from brunns.matchers.path import is_path
    from hamcrest import assert_that, contains_exactly, equal_to, not_
    from pathlib import Path


    def test_path():
        path = Path("/usr/bin/python3.tar.gz")

        assert_that(
            path,
            is_path()
            .with_name("python3.tar.gz")
            .and_stem("python3.tar")
            .and_suffix(".gz")
            .and_suffixes(contains_exactly(".tar", ".gz"))
            .and_parts(contains_exactly("/", "usr", "bin", "python3.tar.gz"))
            .and_parent(equal_to(Path("/usr/bin")))
            .and_root("/"),
        )
        assert_that(path, not_(is_path().with_name("python2.zip")))

The "brunns.matchers.response" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``response`` matchers duck-type a :class:`requests.Response` / :mod:`httpx` response,
so no extra is needed as long as one of those libraries is available.
``redirects_to`` uses the ``url`` matcher, so install the ``url`` extra.

.. code:: python

    import httpx

    from brunns.matchers.response import is_response, redirects_to
    from brunns.matchers.url import is_url
    from hamcrest import assert_that


    def test_response():
        # is_response() matches a response, refined with builders.
        response = httpx.get("https://httpbin.org/status/345", timeout=5)
        assert_that(response, is_response().with_status_code(345))

        # redirects_to() checks a redirecting response's Location header.
        redirect = httpx.get(
            "https://httpb.in/redirect-to?url=https://httpbin.org/sausages",
            follow_redirects=False,
        )
        assert_that(redirect, redirects_to(is_url().with_path("/sausages")))

The "brunns.matchers.rss" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The RSS matchers require the ``rss`` extra (``pip install brunns-matchers[rss]``).

.. code:: python

    import feedparser

    from brunns.matchers.rss import is_rss_category, is_rss_entry, is_rss_feed
    from brunns.matchers.url import is_url
    from hamcrest import assert_that, contains_inanyorder
    from yarl import URL


    RSS = """\
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <title>Test channel</title>
            <link>https://example.com</link>
            <item>
                <title>An article</title>
                <link>https://example.com/article</link>
                <category term="Python" domain="https://example.com/category"/>
            </item>
        </channel>
    </rss>
    """


    def test_rss():
        # is_rss_feed() matches a feed parsed from a string or URL.
        assert_that(
            RSS,
            is_rss_feed()
            .with_title("Test channel")
            .and_link(URL("https://example.com")),
        )
        assert_that(
            RSS,
            is_rss_feed().with_entries(contains_inanyorder(is_rss_entry().with_title("An article"))),
        )

        # is_rss_entry() / is_rss_category() match a single entry and its categories.
        entry = feedparser.parse(RSS).entries[0]
        assert_that(
            entry,
            is_rss_entry()
            .with_title("An article")
            .and_link(URL("https://example.com/article"))
            .and_categories(
                contains_inanyorder(is_rss_category().with_text("Python")),
            ),
        )

The "brunns.matchers.scripttest" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``scripttest`` matchers duck-type a :class:`scripttest.ProcResult` produced by
:meth:`scripttest.TestFileEnvironment.run`.

.. code:: python

    from brunns.matchers.scripttest import is_proc_result
    from hamcrest import assert_that, contains_exactly, contains_string


    def test_proc_result(test_env):
        result = test_env.run("python", "-c", "print('hello world')", expect_error=False)

        assert_that(
            result,
            is_proc_result()
            .with_returncode(0)
            .and_stdout(contains_string("hello world"))
            .and_stderr(""),
        )
        assert_that(
            result,
            is_proc_result().with_args(contains_exactly("python", "-c", "print('hello world')")),
        )

The "brunns.matchers.smtp" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import email.message

    from brunns.matchers.smtp import is_email
    from hamcrest import assert_that, not_


    def make_message() -> str:
        message = email.message.Message()
        message["To"] = "simon <simon@brunni.ng>"
        message["From"] = "fred <fred@beardy.dev>"
        message["Subject"] = "chips"
        message.set_payload("bananas")
        return message.as_string()


    def test_email():
        # Given
        message = make_message()

        # Then
        assert_that(message, is_email().with_to_name("simon"))
        assert_that(message, not_(is_email().with_subject("bacon")))
        assert_that(
            message,
            is_email()
            .with_from_name("fred")
            .and_from_address("fred@beardy.dev")
            .and_subject("chips")
            .and_body_text("bananas"),
        )

The "brunns.matchers.url" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``url`` matchers require the ``url`` extra (``pip install brunns-matchers[url]``).

.. code:: python

    from brunns.matchers.url import is_url
    from hamcrest import assert_that, contains_exactly, has_entries, not_


    URL = "https://username:password@brunni.ng:1234/path1/path2/path3?key1=value1&key2=value2#fragment"


    def test_url():
        assert_that(URL, is_url().with_scheme("https"))
        assert_that(URL, is_url().with_host("brunni.ng"))
        assert_that(URL, not_(is_url().with_host("bacon.co")))
        assert_that(URL, is_url().with_path_segments(contains_exactly("path1", "path2", "path3")))
        assert_that(URL, is_url().with_query(has_entries(key1="value1", key2="value2")))
        assert_that(URL, is_url().with_fragment("fragment"))
        assert_that(
            URL,
            is_url()
            .with_scheme("https")
            .and_username("username")
            .and_password("password")
            .and_port(1234),
        )

The "brunns.matchers.werkzeug" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``werkzeug`` matchers duck-type a :class:`werkzeug.test.TestResponse` (e.g. from Flask's
test client), so any object exposing the same attributes works. As with the project's own tests,
the example below stubs one with :func:`mockito.mock`. ``redirects_to`` uses the ``url`` matcher,
so install the ``url`` extra.

.. code:: python

    from brunns.matchers.url import is_url
    from brunns.matchers.werkzeug import is_werkzeug_response, redirects_to
    from hamcrest import assert_that, has_entries, not_
    from mockito import mock


    def test_werkzeug():
        response = mock(
            {
                "status_code": 200,
                "text": "sausages",
                "mimetype": "text/xml",
                "json": {"a": "b"},
                "headers": {"key": "value"},
            },
        )

        assert_that(response, is_werkzeug_response().with_status_code(200).and_text("sausages"))
        assert_that(response, is_werkzeug_response().with_mimetype("text/xml"))
        assert_that(response, is_werkzeug_response().with_json(has_entries(a="b")))
        assert_that(response, is_werkzeug_response().with_headers(has_entries(key="value")))
        assert_that(response, not_(is_werkzeug_response().with_status_code(404)))

        # redirects_to() checks a redirecting response's Location header.
        redirect = mock({"status_code": 301, "headers": {"Location": "https://brunni.ng/sausages"}})
        assert_that(redirect, redirects_to(is_url().with_path("/sausages")))
