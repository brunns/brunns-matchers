# encoding=utf-8
import logging

from brunns.matchers.dbapi import given_select_returns_rows_matching, has_table, has_table_with_rows
from brunns.matchers.matcher import mismatches_with
from hamcrest import (
    all_of,
    assert_that,
    contains,
    contains_inanyorder,
    contains_string,
    has_item,
    has_length,
    has_properties,
    has_string,
    matches_regexp,
    not_,
)

logger = logging.getLogger(__name__)


def test_has_table(db):
    assert_that(db, has_table("sausages"))
    assert_that(db, not_(has_table("bacon")))
    assert_that(has_table("sausages"), has_string("DB connection has table named 'sausages'"))
    assert_that(
        has_table("bacon"),
        mismatches_with(
            db,
            "SQL statement 'SELECT * FROM bacon;' gives 'OperationalError' <no such table: bacon>",
        ),
    )


def test_has_rows(db):
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
    assert_that(db, not_(has_table_with_rows("sausages", has_item(has_properties(kind="vegan")))))
    assert_that(
        db,
        not_(
            has_table_with_rows(
                "bacon", contains(has_properties(kind="smoked"), has_properties(kind="unsmoked"))
            )
        ),
    )
    assert_that(
        has_table_with_rows(
            "sausages",
            contains(has_properties(kind="cumberland"), has_properties(kind="lincolnshire")),
        ),
        has_string(
            matches_regexp(
                r"DB connection with table 'sausages' with rows matching a sequence containing \["
                r"\(?an object with a property 'kind' matching 'cumberland'\)?, "
                r"\(?an object with a property 'kind' matching 'lincolnshire'\)?"
                r"\]"
            )
        ),
    )
    assert_that(
        has_table_with_rows("sausages", has_item(has_properties(kind="vegan"))),
        mismatches_with(
            db,
            all_of(
                contains_string("was <["), contains_string("RowTuple(kind='vegetarian', rating=0)")
            ),
        ),
    )
    assert_that(
        has_table_with_rows(
            "bacon", contains(has_properties(kind="smoked"), has_properties(kind="unsmoked"))
        ),
        mismatches_with(
            db,
            "SQL statement 'SELECT * FROM bacon;' gives 'OperationalError' <no such table: bacon>",
        ),
    )


def test_select_returns_rows(db):
    assert_that(
        db,
        given_select_returns_rows_matching(
            "SELECT * FROM sausages WHERE rating > 5;", has_length(2)
        ),
    )
    assert_that(
        db,
        not_(
            given_select_returns_rows_matching(
                "SELECT * FROM sausages WHERE rating > 5;", has_length(99)
            )
        ),
    )
    assert_that(
        given_select_returns_rows_matching(
            "SELECT * FROM sausages WHERE rating > 5;", has_length(2)
        ),
        has_string(
            "DB connection for which statement "
            "'SELECT * FROM sausages WHERE rating > 5;' "
            "returns rows matching an object with length of <2>"
        ),
    )
    assert_that(
        given_select_returns_rows_matching(
            "SELECT * FROM sausages WHERE rating > 5;", has_length(99)
        ),
        mismatches_with(db, contains_string("with length of <2>")),
    )
