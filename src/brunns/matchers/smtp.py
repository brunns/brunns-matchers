# encoding=utf-8
import email
import re
from typing import Union

from brunns.matchers.base import GenericMatcher
from brunns.utils.bunch import Bunch
from hamcrest import anything
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher

ANYTHING = anything()


def email_with(
    to_name: Union[str, Matcher] = ANYTHING,
    to_address: Union[str, Matcher] = ANYTHING,
    from_name: Union[str, Matcher] = ANYTHING,
    from_address: Union[str, Matcher] = ANYTHING,
    subject: Union[str, Matcher] = ANYTHING,
    body_text: Union[str, Matcher] = ANYTHING,
) -> Matcher:
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


class EmailWith(GenericMatcher[str]):
    def __init__(
        self,
        to_name: Union[str, Matcher] = ANYTHING,
        to_address: Union[str, Matcher] = ANYTHING,
        from_name: Union[str, Matcher] = ANYTHING,
        from_address: Union[str, Matcher] = ANYTHING,
        subject: Union[str, Matcher] = ANYTHING,
        body_text: Union[str, Matcher] = ANYTHING,
    ) -> None:
        self.to_name = wrap_matcher(to_name)
        self.to_address = wrap_matcher(to_address)
        self.from_name = wrap_matcher(from_name)
        self.from_address = wrap_matcher(from_address)
        self.subject = wrap_matcher(subject)
        self.body_text = wrap_matcher(body_text)

    def _matches(self, actual_email: str) -> bool:
        email = self._parse_email(actual_email)
        return (
            self.to_name.matches(email.actual_to_name)
            and self.to_address.matches(email.actual_to_address)
            and self.from_name.matches(email.actual_from_name)
            and self.from_address.matches(email.actual_from_address)
            and self.subject.matches(email.actual_subject)
            and self.body_text.matches(email.actual_body_text)
        )

    @staticmethod
    def _parse_email(actual_email: str) -> Bunch:
        parsed = email.message_from_string(actual_email)
        actual_to_name, actual_to_address = re.match("(.*) <(.*)>", parsed["To"]).groups()
        actual_from_name, actual_from_address = re.match("(.*) <(.*)>", parsed["From"]).groups()
        actual_subject = parsed["Subject"]
        actual_body_text = parsed.get_payload()
        return Bunch(
            actual_to_name=actual_to_name,
            actual_to_address=actual_to_address,
            actual_from_name=actual_from_name,
            actual_from_address=actual_from_address,
            actual_subject=actual_subject,
            actual_body_text=actual_body_text,
        )

    def describe_to(self, description: Description) -> None:
        description.append_text(
            "email with to_name {0} to_address {1} from_name {2} from_address {3} subject {4} body_text {5}".format(
                self.to_name,
                self.to_address,
                self.from_name,
                self.from_address,
                self.subject,
                self.body_text,
            )
        )

    def describe_mismatch(self, actual_email: str, mismatch_description: Description) -> None:
        email = self._parse_email(actual_email)
        mismatch_description.append_text("was to_name ").append_description_of(
            email.actual_to_name
        ).append_text(" to_address ").append_description_of(email.actual_to_address).append_text(
            " from_name "
        ).append_description_of(
            email.actual_from_name
        ).append_text(
            " from_address "
        ).append_description_of(
            email.actual_from_address
        ).append_text(
            " subject "
        ).append_description_of(
            email.actual_subject
        ).append_text(
            " body_text "
        ).append_description_of(
            email.actual_body_text
        )
