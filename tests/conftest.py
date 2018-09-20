# encoding=utf-8
from __future__ import unicode_literals, absolute_import, division, print_function

import logging

import six

logger = logging.getLogger(__name__)

six.add_move(six.MovedModule("mock", "mock", "unittest.mock"))
