import email.message
from dataclasses import dataclass, field

from hamcrest import assert_that, has_string, not_

from brunns.matchers.matcher import matches_with, mismatches_with
from brunns.matchers.smtp import is_email


def test_email_matcher():
    # Given
    message = str(
        EmailMessageBuilder()
        .with_to("simon@brunni.ng", "simon")
        .and_from("fred@beardy.dev", "fred")
        .and_subject("chips")
        .and_body_text("bananas")
    )

    # When

    # Then
    assert_that(message, is_email().with_to_name("simon"))
    assert_that(message, not_(is_email().with_to_address("banana@example.com").and_to_name("Banana")))
    assert_that(
        is_email()
        .with_to_name("Jenny")
        .and_to_address("jenny@example.com")
        .and_from_name("Fred")
        .and_from_address("fred@example.com")
        .and_subject("Foo")
        .and_body_text("Bar"),
        has_string(
            "email with to_name: 'Jenny' "
            "to_address: 'jenny@example.com' "
            "from_name: 'Fred' "
            "from_address: 'fred@example.com' "
            "subject: 'Foo' "
            "body_text: 'Bar'",
        ),
    )
    assert_that(
        is_email().with_to_address("banana@example.com").and_to_name("Banana"),
        mismatches_with(message, "was email with to_name: was 'simon' to_address: was 'simon@brunni.ng'"),
    )
    assert_that(
        is_email().with_to_address("simon@brunni.ng").and_to_name("simon"),
        matches_with(message, "was email with to_name: was 'simon' to_address: was 'simon@brunni.ng'"),
    )


@dataclass
class EmailMessageBuilder:
    to_address: str = field(default="")
    to_name: str = field(default="")
    from_address: str = field(default="")
    from_name: str = field(default="")
    subject: str = field(default="")
    body_text: str = field(default="")

    def with_to(self, address: str, name: str) -> "EmailMessageBuilder":
        self.to_address = address
        self.to_name = name
        return self

    def and_from(self, address: str, name: str) -> "EmailMessageBuilder":
        self.from_address = address
        self.from_name = name
        return self

    def and_subject(self, subject: str) -> "EmailMessageBuilder":
        self.subject = subject
        return self

    def and_body_text(self, body_text: str) -> "EmailMessageBuilder":
        self.body_text = body_text
        return self

    def __str__(self) -> str:
        msg = email.message.Message()
        msg["To"] = f"{self.to_name} <{self.to_address}>"
        msg["From"] = f"{self.from_name} <{self.from_address}>"
        msg["Subject"] = self.subject
        msg.set_payload(self.body_text)
        return msg.as_string()
