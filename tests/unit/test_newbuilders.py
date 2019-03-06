# encoding=utf-8
import logging
import random

from furl import furl
from hamcrest import has_properties, assert_that, instance_of, not_

from brunns.matchers.object import has_identical_properties_to
from tests.utils.builders import a_domain
from tests.utils.newbuilders import Builder, a_string, an_integer

logger = logging.getLogger(__name__)


def test_all_defaults():
    # Given
    class SomeClass:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    class SomeClassBuilder(Builder):
        target = SomeClass
        a = lambda: 4
        b = a_string

    builder = SomeClassBuilder()

    # When
    actual = builder.build()

    # Then
    assert_that(actual, instance_of(SomeClass))
    assert_that(actual, has_properties(a=4))


def test_with_method():
    # Given
    class SomeClass:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    class SomeClassBuilder(Builder):
        target = SomeClass
        a = lambda: 4
        b = a_string

    builder = SomeClassBuilder()

    # When
    actual = builder.with_a(99).build()

    # Then
    assert_that(actual, instance_of(SomeClass))
    assert_that(actual, has_properties(a=99))


def test_multiple_builders():
    # Given
    class SomeClass:
        def __init__(self, a, b, c=None):
            self.a = a
            self.b = b
            self.c = c

    class SomeClassBuilder(Builder):
        target = SomeClass
        a = lambda: 4
        b = a_string

    builder1 = SomeClassBuilder()
    builder2 = SomeClassBuilder()

    # When
    actual1 = builder1.with_a(99).build()
    actual2 = builder2.build()

    # Then
    assert_that(actual1, not_(has_identical_properties_to(actual2)))


def test_furl_builder():
    # Given
    class FurlBuilder(Builder):
        target = furl

        scheme = lambda: random.choice(["http", "https", "tcp", None])
        username = a_string
        password = a_string
        host = a_domain
        port = lambda: an_integer(1, 65535)
        path = lambda: [a_string(), a_string()]
        query = lambda: {a_string(): a_string(), a_string(): a_string()}
        fragment = a_string

    builder = FurlBuilder()

    # When
    actual = builder.build()

    # Then
    assert_that(actual, instance_of(furl))
