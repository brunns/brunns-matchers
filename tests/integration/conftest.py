# encoding=utf-8
import logging
import sqlite3
import sys

import pytest
from furl import furl

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def db():
    conn = sqlite3.connect(":memory:")

    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE sausages (kind VARCHAR NOT NULL PRIMARY KEY, rating INT NOT NULL);"
    )
    cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("cumberland", 10))
    cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("vegetarian", 0))
    cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("lincolnshire", 9))
    conn.commit()

    yield conn
    conn.close()


@pytest.fixture(scope="session")
def httpbin(docker_ip, docker_services) -> furl:
    if not sys.platform.startswith("win"):
        docker_services.start("httpbin")
        port = docker_services.wait_for_service("httpbin", 80)
        return furl(f"http://{docker_ip}:{port}")
    return furl("https://httpbin.org")
