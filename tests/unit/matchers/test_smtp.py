# encoding=utf-8
from brunns.builder.email import EmailMessageBuilder
from hamcrest import assert_that, has_string, not_

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.smtp import is_email


def test_email_matcher():
    # Given
    message = (
        EmailMessageBuilder()
        .with_to("simon@brunni.ng", "simon")
        .and_from("fred@beardy.dev", "fred")
        .and_subject("chips")
        .and_body_text("bananas")
        .as_string()
    )

    # When

    # Then
    assert_that(message, is_email().with_to_name("simon"))
    assert_that(
        message, not_(is_email().with_to_address("banana@example.com").and_to_name("Banana"))
    )
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
            "body_text: 'Bar'"
        ),
    )
    assert_that(
        is_email().with_to_address("banana@example.com").and_to_name("Banana"),
        mismatches_with(
            message, "was email with to_name: was 'simon' to_address: was 'simon@brunni.ng'"
        ),
    )
