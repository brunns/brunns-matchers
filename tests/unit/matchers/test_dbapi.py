# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sqlite3

from hamcrest import assert_that, has_string, not_, contains, has_properties

from brunns.matchers.dbapi import has_table, has_table_with_rows
from brunns.matchers.matcher import mismatches_with

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def db():
    conn = sqlite3.connect(":memory:")

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE sausages (kind VARCHAR NOT NULL PRIMARY KEY);")
    cursor.execute("INSERT INTO sausages VALUES (?);", ("cumberland",))
    cursor.execute("INSERT INTO sausages VALUES (?);", ("lincolnshire",))
    conn.commit()

    yield conn
    conn.close()


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
            "sausages", contains(has_properties(kind="cumberland"), has_properties(kind="lincolnshire"))
        ),
    )
    assert_that(db, not_(has_table_with_rows("sausages", contains(has_properties(kind="vegetarian")))))
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
        has_table_with_rows("sausages", contains(has_properties(kind="vegetarian"))),
        mismatches_with(
            db, "item 0: an object with a property 'kind' matching 'vegetarian' property 'kind' was 'cumberland'"
        ),
    )
    assert_that(
        has_table_with_rows("bacon", contains(has_properties(kind="smoked"), has_properties(kind="unsmoked"))),
        mismatches_with(db, "SQL statement 'SELECT * FROM bacon;' gives 'OperationalError' <no such table: bacon>"),
    )
