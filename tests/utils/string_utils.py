# encoding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function


def repr_no_unicode_prefix(o):
    return repr(o).lstrip("u")
