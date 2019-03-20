# encoding=utf-8
import logging

logger = logging.getLogger(__name__)


class EqualityFromDict(object):
    """Mix-in allowing equality checking from instance's vars()"""

    def __eq__(self, other: object) -> bool:
        return self.__class__ is other.__class__ and vars(self) == vars(other)

    def __hash__(self):
        return sum(hash(i) for i in vars(self).items())


class ReprFromDict(object):
    """Mix-in implementing repr() from instance's __dict__vars()"""

    def __repr__(self):  # pragma: no cover
        state = ", ".join(("{0:s}={1!r:s}".format(attr, val) for (attr, val) in vars(self).items()))
        return "{0:s}.{1:s}({2:s})".format(
            self.__class__.__module__, self.__class__.__name__, state
        )


class Bunch(ReprFromDict):
    """General purpose container.
    See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52308
    """

    def __init__(self, **kwds):
        vars(self).update(kwds)

    def __contains__(self, key):
        return key in vars(self)

    def __getitem__(self, key):
        return vars(self)[key]
