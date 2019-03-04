# encoding=utf-8
import email
import re

from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher

ANYTHING = anything()


def email_with(
    to_name=ANYTHING,
    to_address=ANYTHING,
    from_name=ANYTHING,
    from_address=ANYTHING,
    subject=ANYTHING,
    body_text=ANYTHING,
):
    """Match email with
    :param to_name:
    :type to_name: Matcher(str) or str
    :param to_address:
    :type to_address: Matcher(str) or str
    :param from_name:
    :type from_name: Matcher(str) or str
    :param from_address:
    :type from_address: Matcher(str) or str
    :param subject:
    :type subject: Matcher(str) or str
    :param body_text:
    :type body_text: Matcher(str) or str
    :return: Matcher
    :rtype: Matcher(str)
    """
    return EmailWith(
        to_name=to_name,
        to_address=to_address,
        from_name=from_name,
        from_address=from_address,
        subject=subject,
        body_text=body_text,
    )


class EmailWith(BaseMatcher):
    def __init__(
        self,
        to_name=ANYTHING,
        to_address=ANYTHING,
        from_name=ANYTHING,
        from_address=ANYTHING,
        subject=ANYTHING,
        body_text=ANYTHING,
    ):
        self.to_name = wrap_matcher(to_name)
        self.to_address = wrap_matcher(to_address)
        self.from_name = wrap_matcher(from_name)
        self.from_address = wrap_matcher(from_address)
        self.subject = wrap_matcher(subject)
        self.body_text = wrap_matcher(body_text)

    def _matches(self, actual_email):
        actual_to_name, actual_to_address, actual_from_name, actual_from_address, actual_subject, actual_body_text = self._parse_email(
            actual_email
        )
        return (
            self.to_name.matches(actual_to_name)
            and self.to_address.matches(actual_to_address)
            and self.from_name.matches(actual_from_name)
            and self.from_address.matches(actual_from_address)
            and self.subject.matches(actual_subject)
            and self.body_text.matches(actual_body_text)
        )

    @staticmethod
    def _parse_email(actual_email):
        parsed = email.message_from_string(actual_email)
        actual_to_name, actual_to_address = re.match("(.*) <(.*)>", parsed["To"]).groups()
        actual_from_name, actual_from_address = re.match("(.*) <(.*)>", parsed["From"]).groups()
        actual_subject = parsed["Subject"]
        actual_body_text = parsed.get_payload()
        return (
            actual_to_name,
            actual_to_address,
            actual_from_name,
            actual_from_address,
            actual_subject,
            actual_body_text,
        )

    def describe_to(self, description):
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

    def describe_mismatch(self, actual_email, mismatch_description):
        actual_to_name, actual_to_address, actual_from_name, actual_from_address, actual_subject, actual_body_text = self._parse_email(
            actual_email
        )
        mismatch_description.append_text("was to_name ").append_description_of(
            actual_to_name
        ).append_text(" to_address ").append_description_of(actual_to_address).append_text(
            " from_name "
        ).append_description_of(
            actual_from_name
        ).append_text(
            " from_address "
        ).append_description_of(
            actual_from_address
        ).append_text(
            " subject "
        ).append_description_of(
            actual_subject
        ).append_text(
            " body_text "
        ).append_description_of(
            actual_body_text
        )
