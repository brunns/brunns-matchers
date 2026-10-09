Examples of usage
=================

The "brunns.matchers" package
-----------------------------

The "brunns.matchers.bytestring" module
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Code under test:

.. code:: python

    def my_function(a_string: str) -> bytes:
        return a_string.upper().encode("utf-8")

Test:

.. code:: python

    from hamcrest import assert_that
    from brunns.matchers.bytestring import contains_bytestring

    def test_bytestrings():
        # Given
        a_string = "hello"

        # When
        actual = my_function(a_string)

        # Then
        assert_that(actual, contains_bytestring(b"ELL"))
