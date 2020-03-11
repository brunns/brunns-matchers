# encoding=utf-8
import logging

from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description

logger = logging.getLogger(__name__)


class ContainsBytestring(BaseMatcher[bytes]):
    """Matches if object is a bytestring containing a given bytestring.

    :param bytestring: The string to search for.
    """

    def __init__(self, bytestring: bytes) -> None:
        super().__init__()
        self.bytestring = bytestring

    def _matches(self, item: bytes) -> bool:
        return self.bytestring in item

    def describe_to(self, description: Description) -> None:
        description.append_text("bytestring containing ").append_description_of(self.bytestring)


def contains_bytestring(bytestring: bytes) -> ContainsBytestring:
    """Matches if object is a bytestring containing a given bytestring.

    :param bytestring: The string to search for.
    """
    return ContainsBytestring(bytestring)
