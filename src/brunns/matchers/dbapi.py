# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from hamcrest import anything, described_as
from hamcrest.core.base_matcher import BaseMatcher

from brunns.row.rowwrapper import RowWrapper

logger = logging.getLogger(__name__)


def has_table(table):
    select = "SELECT * FROM {0};".format(table)  # nosec
    return described_as(
        "DB connection has table named %0", given_select_returns_rows_matching(select, anything()), table
    )


def has_table_with_rows(table, row_matcher):
    select = "SELECT * FROM {0};".format(table)  # nosec
    return described_as(
        "DB connection with table %0 with rows matching %1",
        given_select_returns_rows_matching(select, row_matcher),
        table,
        row_matcher,
    )


def given_select_returns_rows_matching(select, row_matcher):
    return SelectReturnsRowsMatching(select, row_matcher)


class SelectReturnsRowsMatching(BaseMatcher):
    def __init__(self, select, row_matcher):
        self.select = select
        self.row_matcher = row_matcher

    def _matches(self, conn):
        try:
            rows = self._get_rows(conn, self.select)
            return self.row_matcher.matches(rows)
        except Exception:
            return False

    def _get_rows(self, conn, select):
        cursor = conn.cursor()
        cursor.execute(select)
        wrapper = RowWrapper(cursor.description)
        rows = [wrapper.wrap(row) for row in cursor.fetchall()]
        return rows

    def describe_to(self, description):
        description.append_text("DB connection for which statement ").append_description_of(self.select).append_text(
            " returns rows matching "
        ).append_description_of(self.row_matcher)

    def describe_mismatch(self, conn, mismatch_description):
        try:
            rows = self._get_rows(conn, self.select)
            self.row_matcher.describe_mismatch(rows, mismatch_description)
        except Exception as e:
            return (
                mismatch_description.append_text("SQL statement ")
                .append_description_of(self.select)
                .append_text(" gives ")
                .append_description_of(type(e).__name__)
                .append_text(" ")
                .append_description_of(e)
            )
