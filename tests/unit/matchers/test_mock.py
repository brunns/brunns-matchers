# encoding=utf-8
from unittest import mock

from brunns.matchers.matcher import mismatches_with
from brunns.matchers.mock import call_has_arg, call_has_args, has_call
from hamcrest import assert_that, contains_string, has_string, not_


def test_call_has_positional_arg():
    # Given
    m = mock.MagicMock()

    # When
    m("first", "second", "third")
    call = m.mock_calls[0]

    # Then
    assert_that(call, call_has_arg(1, "second"))
    assert_that(call, call_has_arg(2, "third"))
    assert_that(call, not_(call_has_arg(4, "nope")))
    assert_that(call, call_has_arg(1, contains_string("eco")))
    assert_that(
        call_has_arg(1, contains_string("eco")),
        has_string("mock.call with argument index <1> matching a string containing 'eco'"),
    )
    assert_that(
        call_has_arg(1, "fifth"),
        mismatches_with(call, "got mock.call with argument index <1> with value 'second'"),
    )
    assert_that(
        call_has_arg(4, "nope"),
        mismatches_with(call, "got mock.call with without argument index <4>"),
    )


def test_call_has_keyword_arg():
    # Given
    m = mock.MagicMock()

    # When
    m(f="first", s="second", t="third")
    call = m.mock_calls[0]

    # Then
    assert_that(call, call_has_arg("s", "second"))
    assert_that(call, not_(call_has_arg("s", "nope")))
    assert_that(call, not_(call_has_arg("w", "nope")))
    assert_that(call, call_has_arg("s", contains_string("eco")))
    assert_that(
        call_has_arg("s", contains_string("eco")),
        has_string("mock.call with keyword argument 's' matching a string containing 'eco'"),
    )
    assert_that(
        call_has_arg("s", "fifth"),
        mismatches_with(call, "got mock.call with keyword argument 's' with value 'second'"),
    )
    assert_that(
        call_has_arg("n", "nope"),
        mismatches_with(call, "got mock.call with without keyword argument 'n'"),
    )


def test_call_has_args():
    # Given
    m = mock.MagicMock()

    # When
    m("first", "second", "third", key="forth")
    call = m.mock_calls[0]

    # Then
    assert_that(call, call_has_args("first", "second", "third", key="forth"))
    assert_that(call, not_(call_has_args("first", "second", "third", key="banana")))
    assert_that(call, not_(call_has_args("first", "second", "third", "sam", key="banana")))
    assert_that(call, not_(call_has_args("first", "second", "third", key="forth", another="fred")))
    assert_that(
        call, call_has_args("first", contains_string("eco"), "third", key=contains_string("ort"))
    )
    assert_that(
        call_has_args("first", "second", key="banana"),
        has_string("mock.call with arguments ('first', 'second', key='banana')"),
    )
    assert_that(
        call_has_args("first", "second", "third", key="banana"),
        mismatches_with(
            call, contains_string("got arguments ('first', 'second', 'third', key='forth')")
        ),
    )


def test_call_has_exactly_args():
    # TODO
    pass


def test_has_call():
    # Given
    m = mock.MagicMock()
    method = m.m

    # When
    method("first")

    # Then
    assert_that(method, has_call(call_has_args("first")))
    assert_that(method, not_(has_call(call_has_args("chips"))))
    assert_that(
        has_call(call_has_args("first")),
        has_string("has call matching mock.call with arguments ('first')"),
    )
    assert_that(
        has_call(call_has_args("chips")),
        mismatches_with(method, contains_string("""got calls ["call('first'""")),
    )
