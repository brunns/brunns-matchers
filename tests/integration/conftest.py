import logging
import os
import platform
import sqlite3
from urllib.error import HTTPError

import pytest
import requests
from mbtest.server import MountebankServer
from requests.exceptions import ConnectionError as RequestsConnectionError
from yarl import URL

logger = logging.getLogger(__name__)
LOCAL = os.getenv("GITHUB_ACTIONS") != "true"
LINUX = platform.system() == "Linux"
HTTPBIN_CONTAINERISED = LINUX or LOCAL


@pytest.fixture(scope="session")
def db():
    conn = sqlite3.connect(":memory:")

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE sausages (kind VARCHAR NOT NULL PRIMARY KEY, rating INT NOT NULL);")
    cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("cumberland", 10))
    cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("vegetarian", 0))
    cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("lincolnshire", 9))
    conn.commit()

    yield conn
    conn.close()


@pytest.fixture(scope="session")
def httpbin(docker_ip, docker_services) -> URL:
    if HTTPBIN_CONTAINERISED:
        port = docker_services.port_for("httpbin", 80)
        url = URL(f"http://{docker_ip}:{port}")
        docker_services.wait_until_responsive(timeout=30.0, pause=0.1, check=lambda: is_responsive(url))
        return url
    return URL("https://httpbin.org")


@pytest.fixture(scope="session")
def mountebank_instance(docker_ip, docker_services) -> URL:
    port = docker_services.port_for("mountebank", 2525)
    url = URL(f"http://{docker_ip}:{port}")
    docker_services.wait_until_responsive(timeout=30.0, pause=0.1, check=lambda: is_responsive(url))
    return url


@pytest.fixture(scope="session")
def mock_server(mountebank_instance: URL) -> MountebankServer:
    return MountebankServer(host=mountebank_instance.host, port=mountebank_instance.port)


def is_responsive(url: URL) -> bool:
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except (RequestsConnectionError, HTTPError):
        return False
    else:
        return True
