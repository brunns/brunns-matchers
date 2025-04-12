import logging
from datetime import datetime
from typing import Optional, Union

import feedparser
import httpx
from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher, T
from hamcrest.core.description import Description
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from hamcrest.core.matcher import Matcher
from yarl import URL

from brunns.matchers.utils import append_matcher_description, describe_field_match, describe_field_mismatch

logger = logging.getLogger(__name__)
ANYTHING = anything()


class RssFeedMatcher(BaseMatcher[str]):
    def __init__(self):
        self.title: Matcher[str] = ANYTHING
        self.link: Matcher[URL] = ANYTHING
        self.description: Matcher[str] = ANYTHING
        self.published: Matcher[datetime] = ANYTHING
        self.entries: Matcher[list[feedparser.FeedParserDict]] = ANYTHING

    def _matches(self, item: Union[str, URL]) -> bool:
        try:
            actual = feedparser.parse(item)
        except (ValueError, httpx.HTTPError):
            return False
        else:
            published = self._get_published_date(actual.feed)
            return (
                self.title.matches(actual.feed.title)
                and self.link.matches(URL(actual.feed.link))
                and self.description.matches(actual.feed.description)
                and self.published.matches(published)
                and self.entries.matches(actual.entries)
            )

    def describe_to(self, description: Description) -> None:
        description.append_text("RSS feed with")
        append_matcher_description(self.title, "title", description)
        append_matcher_description(self.link, "link", description)
        append_matcher_description(self.description, "description", description)
        append_matcher_description(self.published, "published", description)
        append_matcher_description(self.entries, "entries", description)

    def describe_mismatch(self, item: str, mismatch_description: Description) -> None:
        try:
            actual = feedparser.parse(item)
        except ValueError as e:
            mismatch_description.append_text(f"RSS parsing failed with '{e}'\nfor value {item}")
        except httpx.HTTPError:
            return False
        else:
            mismatch_description.append_text("was RSS feed with")
            describe_field_mismatch(self.title, "title", actual.feed.title, mismatch_description)
            describe_field_mismatch(self.link, "link", URL(actual.feed.link), mismatch_description)
            describe_field_mismatch(self.description, "description", actual.feed.description, mismatch_description)
            published = self._get_published_date(actual.feed)
            describe_field_mismatch(self.published, "published", published, mismatch_description)
            describe_field_mismatch(self.entries, "entries", self.entries, mismatch_description)

    def describe_match(self, item: T, match_description: Description) -> None:
        actual = feedparser.parse(item)
        match_description.append_text("was RSS feed with")
        describe_field_match(self.title, "title", actual.feed.title, match_description)
        describe_field_match(self.link, "link", URL(actual.feed.link), match_description)
        describe_field_match(self.description, "description", actual.feed.description, match_description)
        published = self._get_published_date(actual.feed)
        describe_field_match(self.published, "published", published, match_description)
        describe_field_match(self.entries, "entries", self.entries, match_description)

    def _get_published_date(self, feed) -> Optional[datetime]:
        return datetime.strptime(feed.published, "%a, %d %b %Y %H:%M:%S %z") if "published" in feed else None

    def with_title(self, title: Union[str, Matcher[str]]):
        self.title = wrap_matcher(title)
        return self

    def and_title(self, title: Union[str, Matcher[str]]):
        return self.with_title(title)

    def with_link(self, link: Union[URL, Matcher[URL]]):
        self.link = wrap_matcher(link)
        return self

    def and_link(self, link: Union[URL, Matcher[URL]]):
        return self.with_link(link)

    def with_description(self, description: Union[str, Matcher[str]]):
        self.description = wrap_matcher(description)
        return self

    def and_description(self, description: Union[str, Matcher[str]]):
        return self.with_description(description)

    def with_published(self, published: Union[datetime, Matcher[datetime]]):
        self.published = wrap_matcher(published)
        return self

    def and_published(self, published: Union[datetime, Matcher[datetime]]):
        return self.with_published(published)

    def with_entries(self, entries: Union[list[feedparser.FeedParserDict], Matcher[list[feedparser.FeedParserDict]]]):
        self.entries = wrap_matcher(entries)
        return self

    def and_entries(self, entries: Union[list[feedparser.FeedParserDict], Matcher[list[feedparser.FeedParserDict]]]):
        return self.with_entries(entries)


class RssFeedEntryMatcher(BaseMatcher[feedparser.FeedParserDict]):
    def __init__(self):
        self.title: Matcher[str] = ANYTHING
        self.link: Matcher[URL] = ANYTHING
        self.description: Matcher[str] = ANYTHING
        self.published: Matcher[datetime] = ANYTHING

    def _matches(self, item: feedparser.FeedParserDict) -> bool:
        try:
            published = self._get_published_date(item)
            return (
                self.title.matches(item.get("title", ""))
                and self.link.matches(URL(item.get("link", "")))
                and self.description.matches(item.get("description", ""))
                and self.published.matches(published)
            )
        except Exception:
            return False

    def describe_to(self, description: Description) -> None:
        description.append_text("RSS feed entry with")
        append_matcher_description(self.title, "title", description)
        append_matcher_description(self.link, "link", description)
        append_matcher_description(self.description, "description", description)
        append_matcher_description(self.published, "published", description)

    def describe_match(self, item: feedparser.FeedParserDict, match_description: Description) -> None:
        match_description.append_text("was RSS feed entry with")
        describe_field_match(self.title, "title", item.get("title", ""), match_description)
        describe_field_match(self.link, "link", URL(item.get("link", "")), match_description)
        describe_field_match(self.description, "description", item.get("description", ""), match_description)
        published = self._get_published_date(item)
        describe_field_match(self.published, "published", published, match_description)

    def describe_mismatch(self, item: feedparser.FeedParserDict, mismatch_description: Description) -> None:
        mismatch_description.append_text("was RSS feed entry with")
        describe_field_mismatch(self.title, "title", item.get("title", ""), mismatch_description)
        describe_field_mismatch(self.link, "link", URL(item.get("link", "")), mismatch_description)
        describe_field_mismatch(self.description, "description", item.get("description", ""), mismatch_description)
        published = self._get_published_date(item)
        describe_field_mismatch(self.published, "published", published, mismatch_description)

    def _get_published_date(self, entry: feedparser.FeedParserDict) -> Optional[datetime]:
        return datetime.strptime(entry["published"], "%a, %d %b %Y %H:%M:%S %z") if "published" in entry else None

    def with_title(self, title: Union[str, Matcher[str]]):
        self.title = wrap_matcher(title)
        return self

    def and_title(self, title: Union[str, Matcher[str]]):
        return self.with_title(title)

    def with_link(self, link: Union[URL, Matcher[URL]]):
        self.link = wrap_matcher(link)
        return self

    def and_link(self, link: Union[URL, Matcher[URL]]):
        return self.with_link(link)

    def with_description(self, description: Union[str, Matcher[str]]):
        self.description = wrap_matcher(description)
        return self

    def and_description(self, description: Union[str, Matcher[str]]):
        return self.with_description(description)

    def with_published(self, published: Union[datetime, Matcher[datetime]]):
        self.published = wrap_matcher(published)
        return self

    def and_published(self, published: Union[datetime, Matcher[datetime]]):
        return self.with_published(published)


def is_rss_feed() -> RssFeedMatcher:
    return RssFeedMatcher()


def is_rss_entry() -> RssFeedEntryMatcher:
    return RssFeedEntryMatcher()
