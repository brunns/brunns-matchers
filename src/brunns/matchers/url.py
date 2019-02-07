# encoding=utf-8
import logging

import furl
from hamcrest import anything, equal_to
from hamcrest.core.base_matcher import BaseMatcher
from hamcrest.core.matcher import Matcher

logger = logging.getLogger(__name__)
ANYTHING = anything()


def to_host(matcher):
    return UrlWith(host=matcher)


def with_path(matcher):
    return UrlWith(path=matcher)


class UrlWith(BaseMatcher):
    def __init__(self, host=ANYTHING, path=ANYTHING, query=ANYTHING):
        super(UrlWith, self).__init__()
        self.host = host if isinstance(host, Matcher) else equal_to(host)
        self.path = path if isinstance(path, Matcher) else equal_to(path)
        self.query = query if isinstance(query, Matcher) else equal_to(query)

    def _matches(self, url):
        url = url if isinstance(url, furl.furl) else furl.furl(url)
        return self.host.matches(url.host) and self.path.matches(url.path) and self.query.matches(url.query)

    def describe_to(self, description):
        description.append_text("URL with")
        if self.host != ANYTHING:
            description.append_text(" host ").append_description_of(self.host)
        if self.path != ANYTHING:
            description.append_text(" path ").append_description_of(self.path)

    def describe_mismatch(self, url, mismatch_description):
        url = url if isinstance(url, furl.furl) else furl.furl(url)
        if self.host != ANYTHING and not self.host.matches(url.host):
            mismatch_description.append_text("host ")
            self.host.describe_mismatch(url.host, mismatch_description)
        if self.path != ANYTHING and not self.path.matches(url.path):
            mismatch_description.append_text("path ")
            self.host.describe_mismatch(url.path, mismatch_description)
