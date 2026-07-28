# Copyright 2018-2026 Simon Brunning
import logging
import sys
from xml.etree import ElementTree as ET

import pytest

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s %(module)s.py:%(funcName)s():%(lineno)d %(message)s",
    stream=sys.stdout,
)


@pytest.fixture(scope="session")
def rss_string() -> bytes:
    rss_root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss_root, "channel")
    ET.SubElement(channel, "title").text = "Test channel"
    ET.SubElement(channel, "description").text = "Test channel"
    ET.SubElement(channel, "link").text = "https://example.com"
    ET.SubElement(channel, "pubDate").text = "Sun, 6 Sep 2009 16:20:00 +0000"

    for i in range(3):
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = f"Test article {i}"
        ET.SubElement(item, "link").text = f"https://example.com/article{i}"
        ET.SubElement(item, "description").text = f"Test article {i}"
        for a in range(3):
            ET.SubElement(item, "author").text = f"Author {a} of article {i}"
        for c in range(3):
            category = ET.SubElement(item, "category")
            category.text = f"Category {c}"
            category.set("domain", f"https://example.com/category{c}")
        ET.SubElement(item, "guid").text = f"guid-{i}"
        ET.SubElement(item, "pubDate").text = f"Sun, 6 Sep 2009 {i + 12}:20:00 +0000"
        source = ET.SubElement(item, "source")
        source.text = "Test channel"
        source.set("url", "https://example.com")

    return ET.tostring(rss_root, encoding="unicode")


@pytest.fixture(scope="session")
def empty_rss_string() -> bytes:
    rss_root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss_root, "channel")
    ET.SubElement(channel, "title").text = "Test channel"
    ET.SubElement(channel, "link").text = "https:/example.com"
    ET.SubElement(channel, "description").text = "Test channel"
    ET.SubElement(channel, "pubDate").text = "Sun, 6 Sep 2009 16:20:00 +0000"

    return ET.tostring(rss_root, encoding="unicode")


@pytest.fixture(scope="session")
def rss_item_string() -> bytes:
    item = ET.Element("item")
    ET.SubElement(item, "title").text = "An article"
    ET.SubElement(item, "link").text = "https://example.com/article"
    ET.SubElement(item, "description").text = "An article description"
    for a in range(3):
        ET.SubElement(item, "author").text = f"Author {a}"
    for c in range(3):
        category = ET.SubElement(item, "category")
        category.text = f"Category {c}"
        category.set("domain", f"https://example.com/category{c}")
    ET.SubElement(item, "guid").text = "guid"
    ET.SubElement(item, "pubDate").text = "Sun, 6 Sep 2009 16:20:00 +0000"
    source = ET.SubElement(item, "source")
    source.text = "Test channel"
    source.set("url", "https://example.com")

    return ET.tostring(item, encoding="unicode")
