# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sqlite3

from hamcrest import assert_that, has_string, not_

from brunns.matchers.dbapi import has_table
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
