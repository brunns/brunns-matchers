# encoding=utf-8
import abc
import email
import random
import string
from email.mime.text import MIMEText

from furl import furl


def a_string(length=10, characters=string.ascii_letters + string.digits):
    return "".join(random.choice(characters) for _ in range(length))


def an_integer(a=None, b=None):
    return random.randint(a, b)


def a_boolean():
    return random.choice([True, False])


class TestObjectBuilder(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def value(self):
        raise NotImplementedError()

    def __getattr__(self, item):
        """Dynamic 'with_x' methods."""
        target = item.partition("with_")[2]
        if target:

            def with_(value):
                setattr(self, target, value)
                return self

            return with_
        else:
            return getattr(self.value, item)

    def __getitem__(self, item):
        return self.value[item]


def an_email_message():
    return email_message_builder().value


def email_message_builder():
    return EmailMessageBuilder()


class EmailMessageBuilder(TestObjectBuilder):
    def __init__(self):
        self.to_name = a_string()
        self.to_email_address = an_email_address()
        self.from_name = a_string()
        self.from_email_address = an_email_address()
        self.subject = a_string()
        self.body_text = a_string()

    @property
    def value(self):
        message = MIMEText(self.body_text)
        message["To"] = email.utils.formataddr((self.to_name, self.to_email_address))
        message["From"] = email.utils.formataddr((self.from_name, self.from_email_address))
        message["Subject"] = self.subject
        return message


def a_url():
    return url_builder().value


def url_builder():
    return FurlBuilder()


class FurlBuilder(TestObjectBuilder):
    def __init__(self):
        self.scheme = random.choice(["http", "https", "tcp", None])
        self.username = a_string()
        self.password = a_string()
        self.host = a_domain()
        self.port = an_integer(1, 65535)
        self.path = [a_string(), a_string()]
        self.query = {a_string(): a_string(), a_string(): a_string()}
        self.fragment = a_string()

    @property
    def value(self):
        return furl(
            scheme=self.scheme,
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.path,
            query=self.query,
            fragment=self.fragment,
        )


def a_domain():
    return domain_builder().value


def domain_builder():
    return DomainBuilder()


class DomainBuilder(TestObjectBuilder):
    def __init__(self):
        self.subdomain = a_string(characters=string.ascii_lowercase)
        self.tld = random.choice(["com", "net", "dev", "co.uk"])

    @property
    def value(self):
        return "{0}.{1}".format(self.subdomain, self.tld)


def an_email_address():
    return email_address_builder().value


def email_address_builder():
    return EmaiAddressBuilder()


class EmaiAddressBuilder(TestObjectBuilder):
    def __init__(self):
        self.username = a_string()
        self.domain = a_domain()

    @property
    def value(self):
        return "{0}@{1}".format(self.username, self.domain)
