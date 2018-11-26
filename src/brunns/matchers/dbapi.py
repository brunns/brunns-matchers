# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from hamcrest.core.base_matcher import BaseMatcher

logger = logging.getLogger(__name__)


def has_table(named):
    return HasTable(named)


class HasTable(BaseMatcher):
    def __init__(self, named):
        self.named = named

    def _matches(self, conn):
        select = "SELECT * FROM {0};".format(self.named)  # nosec
        try:
            cursor = conn.cursor()
            return cursor.execute(select)
        except Exception:
            return False

    def describe_to(self, description):
        description.append_text("DB connection has table named ").append_description_of(self.named)

    def describe_mismatch(self, conn, mismatch_description):
        select = "SELECT * FROM {0};".format(self.named)  # nosec
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
