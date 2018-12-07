# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import csv
import logging

from hamcrest import assert_that, contains, has_properties

from brunns.utils.db.rowwrapper import RowWrapper

logger = logging.getLogger(__name__)


def test_dbapi_row_wrapping(db):
    # Given
    cursor = db.cursor()
    cursor.execute("SELECT kind, rating FROM sausages ORDER BY rating DESC;")

    # When
    wrapper = RowWrapper(cursor.description)
    rows = [wrapper.wrap(row) for row in cursor.fetchall()]

    # Then
    assert_that(
        rows,
        contains(
            has_properties(kind="cumberland", rating=10),
            has_properties(kind="lincolnshire", rating=9),
            has_properties(kind="vegetarian", rating=0),
        ),
    )


def test_identifiers_fixed_for_mapping_row():
    # Given
    wrapper = RowWrapper(["column-name"])

    # When
    row = wrapper({"column-name": "value"})

    # Then
    assert_that(row, has_properties(column_name="value"))


def test_identifiers_fixed_for_positional_row():
    # Given
    wrapper = RowWrapper(["column-name"])

    # When
    row = wrapper(["value"])

    # Then
    assert_that(row, has_properties(column_name="value"))


def test_csv_wrapping(csv_file):
    # Given
    reader = csv.DictReader(csv_file)

    # When
    wrapper = RowWrapper(reader.fieldnames)
    rows = [wrapper.wrap(row) for row in reader]

    # Then
    assert_that(
        rows,
        contains(
            has_properties(kind="cumberland", rating="10"),
            has_properties(kind="lincolnshire", rating="9"),
            has_properties(kind="vegetarian", rating="0"),
        ),
    )
