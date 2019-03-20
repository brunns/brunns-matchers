# encoding=utf-8
import logging
from abc import ABCMeta, abstractmethod
from typing import Generic, TypeVar

from hamcrest.core.base_matcher import BaseMatcher

logger = logging.getLogger(__name__)

T = TypeVar("T")


class GenericMatcher(BaseMatcher, Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def _matches(self, item: T) -> bool:  # pragma: no cover
        ...
