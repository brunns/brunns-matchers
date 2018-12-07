# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import collections
import logging

import six

logger = logging.getLogger(__name__)


class RowWrapper(object):
    """
    Build lightweight wrappers for DB API and csv.DictReader rows.

    Inspired by Greg Stein's lovely dtuple module,
    https://code.activestate.com/recipes/81252-using-dtuple-for-flexible-query-result-access,
    which I can't find online any longer, isn't on pypi, and doesn't support Python 3 without some fixes.

    Initializer takes a sequence of column descriptions, either names, or tuples of names and other metadata which will
    be ignored. Happy to take a DB API cursor description, or a csv.DictReader's fieldnames property. Provides a wrap
    method for wrapping rows.

    >>> cursor = conn.cursor()
    >>> cursor.execute("SELECT kind, rating FROM sausages ORDER BY rating DESC;")
    >>> wrapper = RowWrapper(cursor.description)
    >>> rows = [wrapper.wrap(row) for row in cursor.fetchall()]

    >>> reader = csv.DictReader(csv_file)
    >>> wrapper = RowWrapper(reader.fieldnames)
    >>> rows = [wrapper.wrap(row) for row in reader]
    """

    def __init__(self, description):
        self.names = (
            [col for col in description]
            if isinstance(description[0], six.string_types)
            else [col[0] for col in description]
        )
        self.namedtuple = collections.namedtuple("Row", [self._id_fix(n) for n in self.names], rename=True)

    @staticmethod
    def _id_fix(name):
        for f, t in [("-", "_")]:
            name = name.replace(f, t)
        return name

    def wrap(self, row):
        return (
            self.namedtuple(**{self._id_fix(k): row[k] for k in self.names})
            if isinstance(row, collections.Mapping)
            else self.namedtuple(**{self._id_fix(n): r for n, r in zip(self.names, row)})
        )

    def __call__(self, row):
        return self.wrap(row)
