# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from hamcrest import (
    assert_that,
    has_string,
    not_,
    contains,
    has_properties,
    has_length,
    contains_string,
    contains_inanyorder,
    has_item,
    all_of,
    matches_regexp,
)

from brunns.matchers.dbapi import has_table, has_table_with_rows, given_select_returns_rows_matching
from brunns.matchers.matcher import mismatches_with

logger = logging.getLogger(__name__)


def test_has_table(db):
    assert_that(db, has_table("sausages"))
    assert_that(db, not_(has_table("bacon")))
    assert_that(has_table("sausages"), has_string("DB connection has table named 'sausages'"))
    assert_that(
        has_table("bacon"),
        mismatches_with(db, "SQL statement 'SELECT * FROM bacon;' gives 'OperationalError' <no such table: bacon>"),
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
        db, not_(has_table_with_rows("bacon", contains(has_properties(kind="smoked"), has_properties(kind="unsmoked"))))
    )
    assert_that(
        has_table_with_rows(
            "sausages", contains(has_properties(kind="cumberland"), has_properties(kind="lincolnshire"))
        ),
        has_string(
            "DB connection with table 'sausages' with rows matching a sequence containing ["
            "(an object with a property 'kind' matching 'cumberland'), "
            "(an object with a property 'kind' matching 'lincolnshire')"
            "]"
        ),
    )
    assert_that(
        has_table_with_rows("sausages", has_item(has_properties(kind="vegan"))),
        mismatches_with(
            db, all_of(matches_regexp(r"was <\["), matches_regexp(r"Row\(kind=u?'vegetarian', rating=0\)"))
        ),
    )
    assert_that(
        has_table_with_rows("bacon", contains(has_properties(kind="smoked"), has_properties(kind="unsmoked"))),
        mismatches_with(db, "SQL statement 'SELECT * FROM bacon;' gives 'OperationalError' <no such table: bacon>"),
    )


def test_select_returns_rows(db):
    assert_that(db, given_select_returns_rows_matching("SELECT * FROM sausages WHERE rating > 5;", has_length(2)))
    assert_that(
        db, not_(given_select_returns_rows_matching("SELECT * FROM sausages WHERE rating > 5;", has_length(99)))
    )
    assert_that(
        given_select_returns_rows_matching("SELECT * FROM sausages WHERE rating > 5;", has_length(2)),
        has_string(
            "DB connection for which statement "
            "'SELECT * FROM sausages WHERE rating > 5;' "
            "returns rows matching an object with length of <2>"
        ),
    )
    assert_that(
        given_select_returns_rows_matching("SELECT * FROM sausages WHERE rating > 5;", has_length(99)),
        mismatches_with(db, contains_string("with length of <2>")),
    )
