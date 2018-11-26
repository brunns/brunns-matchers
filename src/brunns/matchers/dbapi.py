# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from hamcrest.core.base_matcher import BaseMatcher

from brunns.utils import dtuple

logger = logging.getLogger(__name__)


def has_table(table):
    return HasTable(table)


def has_table_with_rows(table, row_matcher):
    return HasTableWithRows(table, row_matcher)


class HasTable(BaseMatcher):
    def __init__(self, table):
        self.table = table

    def _matches(self, conn):
        select = "SELECT * FROM {0};".format(self.table)  # nosec
        try:
            cursor = conn.cursor()
            return cursor.execute(select)
        except Exception:
            return False

    def describe_to(self, description):
        description.append_text("DB connection has table named ").append_description_of(self.table)

    def describe_mismatch(self, conn, mismatch_description):
        select = "SELECT * FROM {0};".format(self.table)  # nosec
        try:
            cursor = conn.cursor()
            cursor.execute(select)
        except Exception as e:
            return (
                mismatch_description.append_text("SQL statement ")
                .append_description_of(select)
                .append_text(" gives ")
                .append_description_of(type(e).__name__)
                .append_text(" ")
                .append_description_of(e)
            )


class HasTableWithRows(BaseMatcher):
    def __init__(self, table, row_matcher):
        self.table = table
        self.row_matcher = row_matcher

    def _matches(self, conn):
        select = "SELECT * FROM {0};".format(self.table)  # nosec
        try:
            rows = self._get_rows(conn, select)
            return self.row_matcher.matches(rows)
        except Exception:
            return False

    def _get_rows(self, conn, select):
        cursor = conn.cursor()
        cursor.execute(select)
        descriptor = dtuple.TupleDescriptor(cursor.description)
        rows = [dtuple.DatabaseTuple(descriptor, row) for row in cursor.fetchall()]
        return rows

    def describe_to(self, description):
        description.append_text("DB connection with table ").append_description_of(self.table).append_text(
            " with rows matching "
        ).append_description_of(self.row_matcher)

    def describe_mismatch(self, conn, mismatch_description):
        select = "SELECT * FROM {0};".format(self.table)  # nosec
        try:
            rows = self._get_rows(conn, select)
            self.row_matcher.describe_mismatch(rows, mismatch_description)
        except Exception as e:
            return (
                mismatch_description.append_text("SQL statement ")
                .append_description_of(select)
                .append_text(" gives ")
                .append_description_of(type(e).__name__)
                .append_text(" ")
                .append_description_of(e)
            )
