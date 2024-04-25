# encoding=utf-8
import logging
import os
import platform
import sqlite3

import pytest
from yarl import URL

logger = logging.getLogger(__name__)
LOCAL = os.getenv("GITHUB_ACTIONS") != "true"
LINUX = platform.system() == "Linux"
HTTPBIN_CONTAINERISED = LINUX or LOCAL


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
def httpbin(docker_ip, docker_services) -> URL:
    if HTTPBIN_CONTAINERISED:
        docker_services.start("httpbin")
        port = docker_services.wait_for_service("httpbin", 80)
        return URL(f"http://{docker_ip}:{port}")
    return URL("https://httpbin.org")
