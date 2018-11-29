# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from box import SBox

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
        self.names = tuple(col[0] for col in cursor_description)

    def wrap(self, row):
        return SBox(zip(self.names, row), frozen_box=True, ordered_box=True)
