# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sqlite3

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture(scope="package")
def db():
    conn = sqlite3.connect(":memory:")

    cursor = conn.cursor()
    cursor.execute("CREATE TABLE sausages (kind VARCHAR NOT NULL PRIMARY KEY, rating INT NOT NULL);")
    cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("vegetarian", 0))
    cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("lincolnshire", 9))
    cursor.execute("INSERT INTO sausages VALUES (?, ?);", ("cumberland", 10))
    conn.commit()

    yield conn
    conn.close()
