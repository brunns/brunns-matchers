from datetime import datetime, timezone

import feedparser
import httpx
from hamcrest import anything, assert_that, contains_string, equal_to, has_item, has_string, not_
from mockito import mock, patch
from yarl import URL

from brunns.matchers.matcher import matches_with, mismatches_with
from brunns.matchers.rss import is_rss_entry, is_rss_feed


def test_rss_feed(rss_string: str):
    should_match = (
        is_rss_feed()
        .with_title("Test channel")
        .and_link(URL("https://example.com"))
        .and_description("Test channel")
        .and_published(datetime(2009, 9, 6, 16, 20, 0, tzinfo=timezone.utc))
    )
    should_not_match = (
        is_rss_feed()
        .with_title("Another channel")
        .and_link(URL("https://example.com/another"))
        .and_description("Another channel")
        .and_published(datetime(2009, 6, 6, 16, 20, 0, tzinfo=timezone.utc))
    )

    assert_that(rss_string, should_match)
    assert_that(rss_string, not_(should_not_match))

    assert_that(
        should_match,
        has_string(
            "RSS feed with title: 'Test channel' "
            "link: <https://example.com> "
            "description: 'Test channel' "
            "published: <2009-09-06 16:20:00+00:00>"
        ),
    )
    assert_that(
        should_not_match,
        mismatches_with(
            rss_string,
            "was RSS feed with title: was 'Test channel' "
            "link: was <https://example.com> "
            "description: was 'Test channel' "
            "published: was <2009-09-06 16:20:00+00:00>",
        ),
    )
    assert_that(
        should_match,
        matches_with(
            rss_string,
            "was RSS feed with title: was 'Test channel' "
            "link: was <https://example.com> "
            "description: was 'Test channel' "
            "published: was <2009-09-06 16:20:00+00:00>",
        ),
    )


def test_entry_matcher():
    entry = feedparser.FeedParserDict(
        {
            "title": "An article",
            "link": "https://example.com/article",
            "description": "An article description",
            "published": "Sun, 6 Sep 2009 16:20:00 +0000",
        }
    )

    should_match = (
        is_rss_entry()
        .with_title("An article")
        .and_link(URL("https://example.com/article"))
        .and_description("An article description")
        .and_published(datetime(2009, 9, 6, 16, 20, 0, tzinfo=timezone.utc))
    )
    should_not_match = (
        is_rss_entry()
        .with_title("Another article")
        .and_link(URL("https://example.com/another_article"))
        .and_description("Another article description")
        .and_published(datetime(2009, 6, 6, 16, 20, 0, tzinfo=timezone.utc))
    )

    assert_that(entry, should_match)
    assert_that(entry, not_(should_not_match))

    assert_that(
        should_match,
        has_string(
            "RSS feed entry with title: 'An article' "
            "link: <https://example.com/article> "
            "description: 'An article description' "
            "published: <2009-09-06 16:20:00+00:00>"
        ),
    )
    assert_that(
        should_not_match,
        mismatches_with(
            entry,
            "was RSS feed entry with title: was 'An article' "
            "link: was <https://example.com/article> "
            "description: was 'An article description' "
            "published: was <2009-09-06 16:20:00+00:00>",
        ),
    )
    assert_that(
        should_match,
        matches_with(
            entry,
            "was RSS feed entry with title: was 'An article' "
            "link: was <https://example.com/article> "
            "description: was 'An article description' "
            "published: was <2009-09-06 16:20:00+00:00>",
        ),
    )


def test_rss_http_error():
    with patch(feedparser.parse, lambda *_args, **_kwargs: (_ for _ in ()).throw(httpx.HTTPError("404!"))):
        matcher = is_rss_feed()
        invalid_input = "irrelevant"

        assert_that(invalid_input, not_(matcher))

        assert_that(matcher, mismatches_with(invalid_input, contains_string("HTTP error '404!'")))


def test_rss_feed_parsing_failure():
    with patch(feedparser.parse, lambda *_args, **_kwargs: (_ for _ in ()).throw(ValueError("Boom"))):
        matcher = is_rss_feed()
        invalid_input = "invalid"

        assert_that(invalid_input, not_(matcher))

        assert_that(matcher, mismatches_with(invalid_input, contains_string("RSS parsing failed with 'Boom'")))


def test_rss_feed_empty_xml():
    mock_result = mock({"feed": {}})
    with patch(feedparser.parse, lambda *_args, **_kwargs: mock_result):
        matcher = is_rss_feed()
        dummy_input = "irrelevant"

        assert_that(dummy_input, not_(matcher))

        assert_that(
            matcher,
            mismatches_with(dummy_input, contains_string("RSS feed was empty/invalid")),
        )


def test_rss_feed_with_entries(rss_string):
    matcher = is_rss_feed().with_entries(has_item(is_rss_entry().with_title("Test article 0")))

    assert_that(rss_string, matcher)

    assert_that(matcher, matches_with(rss_string, contains_string("entries: was <[")))


def test_entry_matcher_missing_published():
    entry = feedparser.FeedParserDict(
        {
            "title": "An article",
            "link": "https://example.com/article",
        }
    )

    matcher = is_rss_entry().with_title("An article").with_published(equal_to(None))

    assert_that(entry, matcher)

    assert_that(matcher, matches_with(entry, contains_string("published: was <None>")))


def test_matcher_aliases():
    # Exercise .and_title() and .and_entries() on FeedMatcher
    feed_matcher = is_rss_feed().and_title("title").and_entries(anything())
    assert_that(feed_matcher.title, anything())
    assert_that(feed_matcher.entries, anything())

    # Exercise .and_title() on EntryMatcher
    entry_matcher = is_rss_entry().and_title("title")
    assert_that(entry_matcher.title, anything())
