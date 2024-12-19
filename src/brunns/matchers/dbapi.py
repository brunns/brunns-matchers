import logging
from collections.abc import Iterable
from typing import (
    Any,
    Optional,
    Protocol,  # type: ignore[attr-defined]
)

from hamcrest import anything, described_as
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.matcher import Matcher

from brunns.row.rowwrapper import RowWrapper  # type: ignore[attr-defined]

logger = logging.getLogger(__name__)


class Cursor(Protocol):
    def fetchall(self) -> Iterable[tuple[Any, ...]]:  # pragma: no cover
        ...

    def execute(self, statement: str):  # pragma: no cover
        ...

    @property
    def description(self) -> Optional[tuple[tuple[str, str]]]:  # pragma: no cover
        ...


class Connection(Protocol):
    def cursor(self) -> Cursor:  # pragma: no cover
        ...


class SelectReturnsRowsMatching(BaseMatcher[Connection]):
    def __init__(self, select: str, row_matcher: Matcher) -> None:
        self.select = select
        self.row_matcher = row_matcher

    def _matches(self, conn: Connection) -> bool:
        try:
            rows = self._get_rows(conn, self.select)
            return self.row_matcher.matches(rows)
        except Exception:
            return False

    @staticmethod
    def _get_rows(conn: Connection, select: str):
        cursor = conn.cursor()
        cursor.execute(select)
        wrapper = RowWrapper(cursor.description)
        return [wrapper.wrap(row) for row in cursor.fetchall()]

    def describe_to(self, description: Description) -> None:
        description.append_text("DB connection for which statement ").append_description_of(self.select).append_text(
            " returns rows matching ",
        ).append_description_of(self.row_matcher)

    def describe_mismatch(self, conn: Connection, mismatch_description: Description) -> None:
        try:
            rows = self._get_rows(conn, self.select)
            self.row_matcher.describe_mismatch(rows, mismatch_description)
        except Exception as e:
            mismatch_description.append_text("SQL statement ").append_description_of(self.select).append_text(
                " gives ",
            ).append_description_of(type(e).__name__).append_text(" ").append_description_of(e)


def has_table(table: str) -> Matcher:
    """TODO"""
    select = f"SELECT * FROM {table};"  # nosec
    return described_as(
        "DB connection has table named %0",
        given_select_returns_rows_matching(select, anything()),
        table,
    )


def has_table_with_rows(table: str, row_matcher: Matcher) -> Matcher:
    """TODO"""
    select = f"SELECT * FROM {table};"  # nosec
    return described_as(
        "DB connection with table %0 with rows matching %1",
        given_select_returns_rows_matching(select, row_matcher),
        table,
        row_matcher,
    )


def given_select_returns_rows_matching(select: str, row_matcher: Matcher) -> SelectReturnsRowsMatching:
    """TODO"""
    return SelectReturnsRowsMatching(select, row_matcher)
