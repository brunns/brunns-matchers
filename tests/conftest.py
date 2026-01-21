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
def rss_string() -> str:
    rss_root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss_root, "channel")
    ET.SubElement(channel, "title").text = "Test channel"
    ET.SubElement(channel, "description").text = "Test channel"
    ET.SubElement(channel, "link").text = "https://example.com"
    ET.SubElement(channel, "pubDate").text = "Sun, 6 Sep 2009 16:20:00 +0000"

    for i in range(3):
        item = ET.Element("item")
        ET.SubElement(item, "title").text = f"Test article {i}"
        ET.SubElement(item, "description").text = f"Test article {i}"
        ET.SubElement(item, "link").text = f"https://example.com/article{i}"
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
