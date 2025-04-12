from datetime import datetime, timezone
from xml.etree import ElementTree as ET

import feedparser
import pytest
from hamcrest import assert_that, has_string, not_
from yarl import URL

from brunns.matchers.matcher import matches_with, mismatches_with
from brunns.matchers.rss import is_rss_entry


@pytest.fixture(scope="session")
def rss_string() -> str:
    rss_root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss_root, "channel")
    ET.SubElement(channel, "title").text = "Test channel"
    ET.SubElement(channel, "description").text = "Test channel"
    ET.SubElement(channel, "link").text = "https:/example.com"
    ET.SubElement(channel, "pubDate").text = "Sun, 6 Sep 2009 16:20:00 +0000"

    for i in range(3):
        item = ET.Element("item")
        ET.SubElement(item, "title").text = f"Test article {i}"
        ET.SubElement(item, "description").text = f"Test article {i}"
        ET.SubElement(item, "link").text = f"https:/example.com/article{i}"
        ET.SubElement(item, "guid").text = f"guid-{i}"
        ET.SubElement(item, "pubDate").text = f"Sun, 6 Sep 2009 {i + 12}:20:00 +0000"

        channel.append(item)

    return ET.tostring(rss_root, encoding="unicode")


@pytest.fixture(scope="session")
def empty_rss_string() -> str:
    rss_root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss_root, "channel")
    ET.SubElement(channel, "title").text = "Test channel"
    ET.SubElement(channel, "description").text = "Test channel"
    ET.SubElement(channel, "link").text = "https:/example.com"
    ET.SubElement(channel, "pubDate").text = "Sun, 6 Sep 2009 16:20:00 +0000"

    return ET.tostring(rss_root, encoding="unicode")


def test_entry_matcher():
    entry = feedparser.FeedParserDict(
        dict(
            title="An article",
            link="https://example.com/article",
            description="An article description",
            published="Sun, 6 Sep 2009 16:20:00 +0000",
        )
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
