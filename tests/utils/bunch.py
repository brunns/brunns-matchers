import logging

logger = logging.getLogger(__name__)


class ReprFromDict:
    """Mix-in implementing repr() from instance's __dict__vars()"""

    def __repr__(self) -> str:  # pragma: no cover
        state = ", ".join(f"{attr:s}={val!r:s}" for (attr, val) in vars(self).items())
        return f"{self.__class__.__module__:s}.{self.__class__.__name__:s}({state:s})"
