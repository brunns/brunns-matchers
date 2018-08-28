# brunns-matchers

Various custom [PyHamcrest](https://pyhamcrest.readthedocs.io) matchers.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.org/brunns/brunns-matchers.svg?branch=master)](https://travis-ci.org/brunns/brunns-matchers)
[![PyPi Version](https://img.shields.io/pypi/v/brunns-matchers.svg)](https://pypi.org/project/brunns-matchers/releases/)
[![Licence](https://img.shields.io/github/license/brunns/brunns-matchers.svg)](https://pypi.org/project/brunns-matchers/)
[![Wheel](https://img.shields.io/pypi/wheel/brunns-matchers.svg)](https://pypi.org/project/brunns-matchers/)
[![Python Versions](https://img.shields.io/pypi/pyversions/brunns-matchers.svg)](https://pypi.org/project/brunns-matchers/)
[![Github all releases](https://img.shields.io/github/downloads/brunns/brunns-matchers/total.svg)](https://GitHub.com/brunns/brunns-matchers/releases/)
[![GitHub forks](https://img.shields.io/github/forks/brunns/brunns-matchers.svg?style=social&label=Fork&maxAge=2592000)](https://GitHub.com/brunns/brunns-matchers/network/)
[![GitHub stars](https://img.shields.io/github/stars/brunns/brunns-matchers.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/brunns/brunns-matchers/stargazers/)
[![GitHub watchers](https://img.shields.io/github/watchers/brunns/brunns-matchers.svg?style=social&label=Watch&maxAge=2592000)](https://GitHub.com/brunns/brunns-matchers/watchers/)
[![GitHub contributors](https://img.shields.io/github/contributors/brunns/brunns-matchers.svg)](https://GitHub.com/brunns/brunns-matchers/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/brunns/brunns-matchers.svg)](https://GitHub.com/brunns/brunns-matchers/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/brunns/brunns-matchers.svg)](https://GitHub.com/brunns/brunns-matchers/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/brunns/brunns-matchers.svg)](https://GitHub.com/brunns/brunns-matchers/pull/)
[![GitHub pull-requests closed](https://img.shields.io/github/issues-pr-closed/brunns/brunns-matchers.svg)](https://GitHub.com/brunns/brunns-matchers/pull/)


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
