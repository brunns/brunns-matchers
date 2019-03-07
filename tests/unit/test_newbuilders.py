# encoding=utf-8
import email
import logging
import random
import string
from email.mime.text import MIMEText

from furl import furl
from hamcrest import has_properties, assert_that, instance_of, not_

from brunns.matchers.object import has_identical_properties_to, equal_vars
from brunns.matchers.smtp import email_with
from tests.utils.newbuilders import Builder, a_string, an_integer, one_of

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


def test_kwargs():
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

    # When
    actual = SomeClassBuilder(a=99).build()

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
    class DomainBuilder(Builder):
        subdomain = lambda: a_string(characters=string.ascii_lowercase)
        tld = lambda: one_of("com", "net", "dev", "co.uk", "gov.uk", "ng")

        def build(self):
            return "{0}.{1}".format(self.subdomain, self.tld)

    class FurlBuilder(Builder):
        target = furl

        scheme = lambda: one_of("http", "https", "tcp", None)
        username = a_string
        password = a_string
        host = DomainBuilder
        port = lambda: an_integer(1, 65535)
        path = lambda: [a_string(), a_string()]
        query = lambda: {a_string(): a_string(), a_string(): a_string()}
        fragment = a_string

    builder = FurlBuilder()

    # When
    url1 = builder.build()
    url2 = builder.build()
    url3 = builder.with_host("example.com").build()
    url4 = FurlBuilder().build()

    # Then
    assert_that(url1, instance_of(furl))
    assert equal_vars(url1, url2)
    assert not equal_vars(url1, url3)
    assert not equal_vars(url1, url4)


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
    actual = builder.with_to_name("simon").build()

    # Then
    assert_that(actual, instance_of(MIMEText))
    assert_that(actual.as_string(), email_with(to_name="simon"))
