# encoding=utf-8
import json

from brunns.matchers.data import json_matching
from brunns.matchers.matcher import mismatches_with
from hamcrest import assert_that, contains, has_string, matches_regexp, not_


def test_json_matching():
    # Given
    j = json.dumps([1, 2, 3])

    # When

    # Then
    assert_that(j, json_matching([1, 2, 3]))
    assert_that(j, json_matching(contains(1, 2, 3)))
    assert_that(j, not_(json_matching([1, 2, 5])))
    assert_that(json_matching([1, 2, 3]), has_string("JSON structure matching <[1, 2, 3]>"))
    assert_that(
        json_matching([]),
        mismatches_with("WTF is this?", matches_regexp(r"Got invalid JSON ['<]WTF is this\?['>]")),
    )
    assert_that(json_matching([]), mismatches_with("[1]", "was <[1]>"))
