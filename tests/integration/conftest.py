# encoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import sqlite3

import pytest
from six import StringIO

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


@pytest.fixture(scope="function")
def csv_file():
    data = "kind,rating\n" "vegetarian,0\n" "lincolnshire,9\n" "cumberland,10\n"
    return StringIO(data)
