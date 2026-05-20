from __future__ import annotations

import logging
from datetime import datetime
from typing import TYPE_CHECKING, cast

import feedparser
import httpx
from hamcrest import anything
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.helpers.wrap_matcher import wrap_matcher
from yarl import URL

from brunns.matchers.url import UrlProtocol
from brunns.matchers.utils import append_matcher_description, describe_field_match, describe_field_mismatch

if TYPE_CHECKING:
    from hamcrest.core.description import Description
    from hamcrest.core.matcher import Matcher

logger = logging.getLogger(__name__)
ANYTHING = anything()


class RssFeedMatcher(BaseMatcher[UrlProtocol]):
    def __init__(self):
        self.title: Matcher[str] = ANYTHING
        self.link: Matcher[UrlProtocol] = ANYTHING
        self.description: Matcher[str] = ANYTHING
        self.published: Matcher[datetime | None] = ANYTHING
        self.entries: Matcher[list[feedparser.FeedParserDict]] = ANYTHING

    def _matches(self, item: UrlProtocol) -> bool:
        try:
            actual = feedparser.parse(str(item))
        except (ValueError, httpx.HTTPError):
            return False
        else:
            if not actual.feed:
                return False

            feed = cast("feedparser.FeedParserDict", actual.feed)
            published = self._get_published_date(feed)
            return (
                self.title.matches(cast("str", feed.get("title", "")))
                and self.link.matches(cast("UrlProtocol", URL(cast("str", feed.get("link", "")))))
                and self.description.matches(cast("str", feed.get("description", "")))
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

    def describe_mismatch(self, item: UrlProtocol, mismatch_description: Description) -> None:
        try:
            actual = feedparser.parse(str(item))
        except ValueError as e:
            mismatch_description.append_text(f"RSS parsing failed with '{e}'\nfor value {item}")
        except httpx.HTTPError as e:
            mismatch_description.append_text(f"HTTP error '{e}'\nfor URL {item}")
        else:
            if not actual.feed:
                mismatch_description.append_text(f"RSS feed was empty/invalid for value {item}")
                return
            feed = cast("feedparser.FeedParserDict", actual.feed)
            mismatch_description.append_text("was RSS feed with")
            describe_field_mismatch(self.title, "title", cast("str", feed.get("title", "")), mismatch_description)
            describe_field_mismatch(
                self.link, "link", cast("UrlProtocol", URL(cast("str", feed.get("link", "")))), mismatch_description
            )
            describe_field_mismatch(
                self.description, "description", cast("str", feed.get("description", "")), mismatch_description
            )
            published = self._get_published_date(feed)
            describe_field_mismatch(self.published, "published", published, mismatch_description)
            describe_field_mismatch(self.entries, "entries", actual.entries, mismatch_description)

    def describe_match(self, item: UrlProtocol, match_description: Description) -> None:
        actual = feedparser.parse(str(item))
        feed = cast("feedparser.FeedParserDict", actual.feed)
        match_description.append_text("was RSS feed with")
        describe_field_match(self.title, "title", cast("str", feed.get("title", "")), match_description)
        describe_field_match(
            self.link, "link", cast("UrlProtocol", URL(cast("str", feed.get("link", "")))), match_description
        )
        describe_field_match(
            self.description, "description", cast("str", feed.get("description", "")), match_description
        )
        published = self._get_published_date(feed)
        describe_field_match(self.published, "published", published, match_description)
        describe_field_match(self.entries, "entries", actual.entries, match_description)

    def _get_published_date(self, feed) -> datetime | None:
        return datetime.strptime(feed.published, "%a, %d %b %Y %H:%M:%S %z") if "published" in feed else None

    def with_title(self, title: str | Matcher[str]):
        self.title = wrap_matcher(title)
        return self

    def and_title(self, title: str | Matcher[str]):
        return self.with_title(title)

    def with_link(self, link: UrlProtocol | Matcher[UrlProtocol]):
        self.link = wrap_matcher(link)
        return self

    def and_link(self, link: UrlProtocol | Matcher[UrlProtocol]):
        return self.with_link(link)

    def with_description(self, description: str | Matcher[str]):
        self.description = wrap_matcher(description)
        return self

    def and_description(self, description: str | Matcher[str]):
        return self.with_description(description)

    def with_published(self, published: datetime | None | Matcher[datetime | None]):
        self.published = wrap_matcher(published)
        return self

    def and_published(self, published: datetime | None | Matcher[datetime | None]):
        return self.with_published(published)

    def with_entries(self, entries: list[feedparser.FeedParserDict] | Matcher[list[feedparser.FeedParserDict]]):
        self.entries = wrap_matcher(entries)
        return self

    def and_entries(self, entries: list[feedparser.FeedParserDict] | Matcher[list[feedparser.FeedParserDict]]):
        return self.with_entries(entries)


class RssFeedEntryMatcher(BaseMatcher[feedparser.FeedParserDict]):
    def __init__(self):
        self.title: Matcher[str] = ANYTHING
        self.link: Matcher[URL] = ANYTHING
        self.description: Matcher[str] = ANYTHING
        self.published: Matcher[datetime | None] = ANYTHING

    def _matches(self, item: feedparser.FeedParserDict) -> bool:
        published = self._get_published_date(item)
        return (
            self.title.matches(cast("str", item.get("title", "")))
            and self.link.matches(URL(cast("str", item.get("link", ""))))
            and self.description.matches(cast("str", item.get("description", "")))
            and self.published.matches(published)
        )

    def describe_to(self, description: Description) -> None:
        description.append_text("RSS feed entry with")
        append_matcher_description(self.title, "title", description)
        append_matcher_description(self.link, "link", description)
        append_matcher_description(self.description, "description", description)
        append_matcher_description(self.published, "published", description)

    def describe_match(self, item: feedparser.FeedParserDict, match_description: Description) -> None:
        match_description.append_text("was RSS feed entry with")
        describe_field_match(self.title, "title", cast("str", item.get("title", "")), match_description)
        describe_field_match(self.link, "link", URL(cast("str", item.get("link", ""))), match_description)
        describe_field_match(
            self.description, "description", cast("str", item.get("description", "")), match_description
        )
        published = self._get_published_date(item)
        describe_field_match(self.published, "published", published, match_description)

    def describe_mismatch(self, item: feedparser.FeedParserDict, mismatch_description: Description) -> None:
        mismatch_description.append_text("was RSS feed entry with")
        describe_field_mismatch(self.title, "title", cast("str", item.get("title", "")), mismatch_description)
        describe_field_mismatch(self.link, "link", URL(cast("str", item.get("link", ""))), mismatch_description)
        describe_field_mismatch(
            self.description, "description", cast("str", item.get("description", "")), mismatch_description
        )
        published = self._get_published_date(item)
        describe_field_mismatch(self.published, "published", published, mismatch_description)

    def _get_published_date(self, entry: feedparser.FeedParserDict) -> datetime | None:
        return (
            datetime.strptime(cast("str", entry["published"]), "%a, %d %b %Y %H:%M:%S %z")
            if "published" in entry
            else None
        )

    def with_title(self, title: str | Matcher[str]):
        self.title = wrap_matcher(title)
        return self

    def and_title(self, title: str | Matcher[str]):
        return self.with_title(title)

    def with_link(self, link: URL | Matcher[URL]):
        self.link = wrap_matcher(link)
        return self

    def and_link(self, link: URL | Matcher[URL]):
        return self.with_link(link)

    def with_description(self, description: str | Matcher[str]):
        self.description = wrap_matcher(description)
        return self

    def and_description(self, description: str | Matcher[str]):
        return self.with_description(description)

    def with_published(self, published: datetime | None | Matcher[datetime | None]):
        self.published = wrap_matcher(published)
        return self

    def and_published(self, published: datetime | None | Matcher[datetime | None]):
        return self.with_published(published)


def is_rss_feed() -> RssFeedMatcher:
    """Matches a string (or URL-like object) as an RSS feed using ``feedparser``.

    The string is parsed as an RSS feed, and the resulting structure is checked.
    This matcher uses a builder pattern (e.g., ``.with_title(...)``) to refine the match.

    Requires brunns-matchers to have been installed with the `rss` extra.

    :return: A matcher for RSS feed content.
    """
    return RssFeedMatcher()


def is_rss_entry() -> RssFeedEntryMatcher:
    """Matches a single RSS feed entry (item) within an RSS feed.

    This matcher operates on ``feedparser.FeedParserDict`` objects, typically found in
    the ``entries`` list of a parsed feed.

    Requires brunns-matchers to have been installed with the `rss` extra.

    :return: A matcher for an RSS feed entry.
    """
    return RssFeedEntryMatcher()
