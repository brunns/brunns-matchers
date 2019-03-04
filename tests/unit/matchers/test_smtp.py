# encoding=utf-8
from hamcrest import assert_that, not_, has_string

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.smtp import email_with
from tests.utils.builders import email_message_builder


def test_email_matcher():
    # Given
    m = (
        email_message_builder()
        .with_to_name("fred")
        .with_to_email_address("simon@brunni.ng")
        .with_subject("chips")
        .with_body_text("bananas")
        .as_string()
    )

    # When

    # Then
    assert_that(m, email_with(to_name="fred"))
    assert_that(m, not_(email_with(to_name="Banana")))
    assert_that(
        email_with(body_text="Foobar"),
        has_string(
            "email with to_name ANYTHING to_address ANYTHING subject ANYTHING body_text 'Foobar'"
        ),
    )
    assert_that(
        email_with(to_name="Banana"),
        mismatches_with(
            m, "was to_name 'fred' to_address 'simon@brunni.ng' subject 'chips' body_text 'bananas'"
        ),
    )
