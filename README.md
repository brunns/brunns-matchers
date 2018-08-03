# brunns-matchers

Various custom [PyHamcrest](https://pyhamcrest.readthedocs.io) matchers.

[![Build Status](https://travis-ci.org/brunns/brunns-matchers.svg?branch=master)](https://travis-ci.org/brunns/brunns-matchers)

## Setup

Install with pip:

    pip install brunns-matchers

(As usual, use of a [venv](https://docs.python.org/3/library/venv.html) or [virtualenv](https://virtualenv.pypa.io) is recommended.)

## Developing

Requires [tox](https://tox.readthedocs.io). Run `make precommit` tells you if you're OK to commit. For more options, run:

    make help

## Releasing

Requires [hub](https://hub.github.com/), [setuptools](https://setuptools.readthedocs.io) and [twine](https://twine.readthedocs.io). To release `n.n.n`:

    version="n.n.n"
    git commit -am"Release $version" && git push # If not already all pushed, which it should be.
    hub release create $version -m"Release $version"
    python setup.py sdist
    twine upload dist/`ls -t dist/ | head -n1`
