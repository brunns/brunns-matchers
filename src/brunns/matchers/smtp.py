# encoding=utf-8
import email
import re
from typing import Match, NamedTuple, Union, cast

from deprecated import deprecated
from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

from brunns.matchers.utils import (
    append_matcher_description,
    describe_field_match,
    describe_field_mismatch,
)

ANYTHING = anything()

Email = NamedTuple(
    "Email",
    [
        ("to_name", str),
        ("to_address", str),
        ("from_name", str),
        ("from_address", str),
        ("subject", str),
        ("body_text", str),
    ],
)


def is_email():
    """"""
    return EmailWith()


class EmailWith(BaseMatcher[str]):
    def __init__(
        self,
        to_name: Union[str, Matcher[str]] = ANYTHING,
        to_address: Union[str, Matcher[str]] = ANYTHING,
        from_name: Union[str, Matcher[str]] = ANYTHING,
        from_address: Union[str, Matcher[str]] = ANYTHING,
        subject: Union[str, Matcher[str]] = ANYTHING,
        body_text: Union[str, Matcher[str]] = ANYTHING,
    ) -> None:
        self.to_name: Matcher[str] = wrap_matcher(to_name)
        self.to_address: Matcher[str] = wrap_matcher(to_address)
        self.from_name: Matcher[str] = wrap_matcher(from_name)
        self.from_address: Matcher[str] = wrap_matcher(from_address)
        self.subject: Matcher[str] = wrap_matcher(subject)
        self.body_text: Matcher[str] = wrap_matcher(body_text)

    def _matches(self, actual_email: str) -> bool:
        email = self._parse_email(actual_email)
        return (
            self.to_name.matches(email.to_name)
            and self.to_address.matches(email.to_address)
            and self.from_name.matches(email.from_name)
            and self.from_address.matches(email.from_address)
            and self.subject.matches(email.subject)
            and self.body_text.matches(email.body_text)
        )

    @staticmethod
    def _parse_email(actual_email: str) -> Email:
        parsed = email.message_from_string(actual_email)
        actual_to_name, actual_to_address = cast(
            Match, re.match("(.*) <(.*)>", parsed["To"])
        ).groups()
        actual_from_name, actual_from_address = cast(
            Match, re.match("(.*) <(.*)>", parsed["From"])
        ).groups()
        actual_subject = parsed["Subject"]
        actual_body_text = parsed.get_payload()
        return Email(
            to_name=actual_to_name,
            to_address=actual_to_address,
            from_name=actual_from_name,
            from_address=actual_from_address,
            subject=actual_subject,
            body_text=actual_body_text,
        )

    def describe_to(self, description: Description) -> None:
        description.append_text("email with")
        append_matcher_description(self.to_name, "to_name", description)
        append_matcher_description(self.to_address, "to_address", description)
        append_matcher_description(self.from_name, "from_name", description)
        append_matcher_description(self.from_address, "from_address", description)
        append_matcher_description(self.subject, "subject", description)
        append_matcher_description(self.body_text, "body_text", description)

    def describe_mismatch(self, actual_email: str, mismatch_description: Description) -> None:
        email = self._parse_email(actual_email)
        mismatch_description.append_text("was email with")
        describe_field_mismatch(self.to_name, "to_name", email.to_name, mismatch_description)
        describe_field_mismatch(
            self.to_address, "to_address", email.to_address, mismatch_description
        )
        describe_field_mismatch(self.from_name, "from_name", email.from_name, mismatch_description)
        describe_field_mismatch(
            self.from_address, "from_address", email.from_address, mismatch_description
        )
        describe_field_mismatch(self.subject, "subject", email.subject, mismatch_description)
        describe_field_mismatch(self.body_text, "body", email.body_text, mismatch_description)

    def describe_match(self, actual_email: str, match_description: Description) -> None:
        email = self._parse_email(actual_email)
        match_description.append_text("was email with")
        describe_field_match(self.to_name, "to_name", email.to_name, match_description)
        describe_field_match(self.to_address, "to_address", email.to_address, match_description)
        describe_field_match(self.from_name, "from_name", email.from_name, match_description)
        describe_field_match(
            self.from_address, "from_address", email.from_address, match_description
        )
        describe_field_match(self.subject, "subject", email.subject, match_description)
        describe_field_match(self.body_text, "body", email.body_text, match_description)

    def with_to_name(self, to_name: Union[str, Matcher[str]]):
        self.to_name = wrap_matcher(to_name)
        return self

    def and_to_name(self, to_name: Union[str, Matcher[str]]):
        return self.with_to_name(to_name)

    def with_to_address(self, to_address: Union[str, Matcher[str]]):
        self.to_address = wrap_matcher(to_address)
        return self

    def and_to_address(self, to_address: Union[str, Matcher[str]]):
        return self.with_to_address(to_address)

    def with_from_name(self, from_name: Union[str, Matcher[str]]):
        self.from_name = wrap_matcher(from_name)
        return self

    def and_from_name(self, from_name: Union[str, Matcher[str]]):
        return self.with_from_name(from_name)

    def with_from_address(self, from_address: Union[str, Matcher[str]]):
        self.from_address = wrap_matcher(from_address)
        return self

    def and_from_address(self, from_address: Union[str, Matcher[str]]):
        return self.with_from_address(from_address)

    def with_subject(self, subject: Union[str, Matcher[str]]):
        self.subject = wrap_matcher(subject)
        return self

    def and_subject(self, subject: Union[str, Matcher[str]]):
        return self.with_subject(subject)

    def with_body_text(self, body_text: Union[str, Matcher[str]]):
        self.body_text = wrap_matcher(body_text)
        return self

    def and_body_text(self, body_text: Union[str, Matcher[str]]):
        return self.with_body_text(body_text)


@deprecated(version="2.3.0", reason="Use builder style is_email()")
def email_with(
    to_name: Union[str, Matcher[str]] = ANYTHING,
    to_address: Union[str, Matcher[str]] = ANYTHING,
    from_name: Union[str, Matcher[str]] = ANYTHING,
    from_address: Union[str, Matcher[str]] = ANYTHING,
    subject: Union[str, Matcher[str]] = ANYTHING,
    body_text: Union[str, Matcher[str]] = ANYTHING,
) -> Matcher:  # pragma: no cover
    """Match email with
    :param to_name:
    :param to_address:
    :param from_name:
    :param from_address:
    :param subject:
    :param body_text:
    :return: Matcher
    """
    return EmailWith(
        to_name=to_name,
        to_address=to_address,
        from_name=from_name,
        from_address=from_address,
        subject=subject,
        body_text=body_text,
    )
