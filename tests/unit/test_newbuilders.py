# encoding=utf-8
import email
import logging
import random
import string
from email.mime.text import MIMEText

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


def test_nested_builders():
    # Given
    class DomainBuilder(Builder):
        subdomain = lambda: a_string(characters=string.ascii_lowercase)
        tld = lambda: random.choice(["com", "net", "dev", "co.uk"])

        def build(self):
            return "{0}.{1}".format(self.subdomain, self.tld)

    class EmailBuilder(Builder):
        username = a_string
        domain = DomainBuilder

        def build(self):
            return "{0}@{1}".format(self.username, self.domain)

    class EmailMessageBuilder(Builder):
        to_name = a_string
        to_email_address = EmailBuilder
        from_name = a_string
        from_email_address = EmailBuilder
        subject = a_string
        body_text = a_string

        def build(self):
            message = MIMEText(self.body_text)
            message["To"] = email.utils.formataddr((self.to_name, self.to_email_address))
            message["From"] = email.utils.formataddr((self.from_name, self.from_email_address))
            message["Subject"] = self.subject
            return message

    builder = EmailMessageBuilder()

    # When
    actual = builder.build()

    # Then
    assert_that(actual, instance_of(MIMEText))
