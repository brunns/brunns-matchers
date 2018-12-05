# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import functools
import logging

from box import Box

logger = logging.getLogger(__name__)


def row_wrapper(cursor_description):
    return RowWrapper(cursor_description)


class RowWrapper(object):
    """
    Build lightweight wrappers for DB API rows, using https://pypi.org/project/python-box/.

    Inspired by Greg Stein's dtuple module,
    https://code.activestate.com/recipes/81252-using-dtuple-for-flexible-query-result-access/,
    which I can't find online any longer, certainly isn't on pypi, and doesn't support Python 3 without fixes in any
    case.
    """

    def __init__(self, cursor_description):
        self.names = [col[0] for col in cursor_description]

    def wrap(self, row):
        return Row(zip(self.names, row))


@functools.total_ordering
class Row(Box):
    def __init__(self, *args, **kwargs):
        super(Row, self).__init__(*args, ordered_box=True, frozen_box=True, **kwargs)

    def __eq__(self, other):
        if not isinstance(other, Row):
            return NotImplemented
        return self.keys() == other.keys() and [self[k] for k in self.keys()] == [other[k] for k in self.keys()]

    def __ne__(self, other):
        if not isinstance(other, Row):
            return NotImplemented
        return not self.__eq__(other)

    def __lt__(self, other):
        if not (isinstance(other, Row) and self.keys() == other.keys()):
            return NotImplemented
        return [self[k] for k in self.keys()] < [other[k] for k in self.keys()]

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            ", ".join("{0}={1!r}".format(attribute, value) for (attribute, value) in self.items()),
        )
