# encoding=utf-8


def repr_no_unicode_prefix(o):
    return repr(o).lstrip("u")
