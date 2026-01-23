from datetime import datetime, timezone

import pytest
from hamcrest import assert_that, not_
from mbtest.imposters import Imposter, Predicate, Response, Stub
from mbtest.server import MountebankServer
from yarl import URL

from brunns.matchers.matcher import matches_with, mismatches_with
from brunns.matchers.rss import is_rss_feed
from tests.integration.conftest import CONTAINERS_AVAILABLE


@pytest.mark.skipif(not CONTAINERS_AVAILABLE, reason="Docker is not available or compatible on this runner")
def test_rss_feed_from_url(mock_server: MountebankServer, rss_string: str):
    # Given
    imposter = Imposter(stubs=[Stub(Predicate(path="/rss"), Response(body=rss_string))], port=4545)
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

    with mock_server(imposter):
        # Test reading a list of feeds
        rss_url = imposter.url / "rss"

        assert_that(rss_url, should_match)
        assert_that(rss_url, not_(should_not_match))

        assert_that(
            should_not_match,
            mismatches_with(
                rss_url,
                "was RSS feed with title: was 'Test channel' "
                "link: was <https://example.com> "
                "description: was 'Test channel' "
                "published: was <2009-09-06 16:20:00+00:00>",
            ),
        )
        assert_that(
            should_match,
            matches_with(
                rss_url,
                "was RSS feed with title: was 'Test channel' "
                "link: was <https://example.com> "
                "description: was 'Test channel' "
                "published: was <2009-09-06 16:20:00+00:00>",
            ),
        )
