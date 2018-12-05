# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sys

import pytest
from hamcrest import assert_that, contains, calling, raises

from brunns.utils.db.rowwrapper import row_wrapper, Row

logger = logging.getLogger(__name__)


def test_row_equality():
    assert Row([("kind", "cumberland"), ("rating", 10)]) == Row([("kind", "cumberland"), ("rating", 10)])
    assert not Row([("kind", "cumberland"), ("rating", 10)]) == "Random object"
    assert Row([("kind", "cumberland"), ("rating", 10)]) != Row([("rating", 10), ("kind", "cumberland")])
    assert Row([("kind", "cumberland"), ("rating", 10)]) != Row(kind="tofu", rating=-10)
    assert Row([("kind", "cumberland"), ("rating", 10)]) != Row(somekey="somevalue")
    assert Row([("kind", "cumberland"), ("rating", 10)]) != "Random object"


def test_row_ordering(db):
    # Given
    cursor = db.cursor()
    cursor.execute("SELECT kind, rating FROM sausages;")

    # When
    wrapper = row_wrapper(cursor.description)
    rows = sorted(wrapper.wrap(row) for row in cursor.fetchall())

    # Then
    assert rows[0] == Row([("kind", "cumberland"), ("rating", 10)])
    assert_that(
        rows,
        contains(
            Row([("kind", "cumberland"), ("rating", 10)]),
            Row([("kind", "lincolnshire"), ("rating", 9)]),
            Row([("kind", "vegetarian"), ("rating", 0)]),
        ),
    )


@pytest.mark.skipif(sys.version_info < (3, 0), reason="Python 2 allows sorting differing types")
def test_no_ordering_with_differing_types():
    # Given
    given = ["Random object", Row([("kind", "cumberland"), ("rating", 10)]), 99]

    # When
    assert_that(calling(sorted).with_args(given), raises(TypeError))
