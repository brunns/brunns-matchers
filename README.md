# brunns-matchers

Various custom [PyHamcrest](https://pyhamcrest.readthedocs.io) matchers. See [the documentation](https://brunns-matchers.readthedocs.io/) for details.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.org/brunns/brunns-matchers.svg?branch=master&logo=travis)](https://travis-ci.org/brunns/brunns-matchers)
[![PyPi Version](https://img.shields.io/pypi/v/brunns-matchers.svg?logo=pypi)](https://pypi.org/project/brunns-matchers/#history)
[![Python Versions](https://img.shields.io/pypi/pyversions/brunns-matchers.svg?logo=python)](https://pypi.org/project/brunns-matchers/)
[![Licence](https://img.shields.io/github/license/brunns/brunns-matchers.svg)](https://github.com/brunns/brunns-matchers/blob/master/LICENSE)
[![GitHub all releases](https://img.shields.io/github/downloads/brunns/brunns-matchers/total.svg?logo=github)](https://github.com/brunns/brunns-matchers/releases/)
[![GitHub forks](https://img.shields.io/github/forks/brunns/brunns-matchers.svg?label=Fork&logo=github)](https://github.com/brunns/brunns-matchers/network/members)
[![GitHub stars](https://img.shields.io/github/stars/brunns/brunns-matchers.svg?label=Star&logo=github)](https://github.com/brunns/brunns-matchers/stargazers/)
[![GitHub watchers](https://img.shields.io/github/watchers/brunns/brunns-matchers.svg?label=Watch&logo=github)](https://github.com/brunns/brunns-matchers/watchers/)
[![GitHub contributors](https://img.shields.io/github/contributors/brunns/brunns-matchers.svg?logo=github)](https://github.com/brunns/brunns-matchers/graphs/contributors/)
[![GitHub issues](https://img.shields.io/github/issues/brunns/brunns-matchers.svg?logo=github)](https://github.com/brunns/brunns-matchers/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/brunns/brunns-matchers.svg?logo=github)](https://github.com/brunns/brunns-matchers/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/brunns/brunns-matchers.svg?logo=github)](https://github.com/brunns/brunns-matchers/pulls)
[![GitHub pull-requests closed](https://img.shields.io/github/issues-pr-closed/brunns/brunns-matchers.svg?logo=github)](https://github.com/brunns/brunns-matchers/pulls?utf8=%E2%9C%93&q=is%3Apr+is%3Aclosed)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/0b22e28c2ebe4722899a07c4cfa5bc69)](https://www.codacy.com/app/brunns/brunns-matchers)
[![Codacy Coverage](https://api.codacy.com/project/badge/coverage/0b22e28c2ebe4722899a07c4cfa5bc69)](https://www.codacy.com/app/brunns/brunns-matchers)
[![Lines of Code](https://tokei.rs/b1/github/brunns/brunns-matchers)](https://github.com/brunns/brunns-matchers)

## Setup

Install with pip:

    pip install brunns-matchers

(As usual, use of a [venv](https://docs.python.org/3/library/venv.html) or [virtualenv](https://virtualenv.pypa.io) is recommended.)

## Developing

Requires [tox](https://tox.readthedocs.io). Run `make precommit` tells you if you're OK to commit. For more options, run:

    make help

## Releasing

Requires [gh](https://cli.github.com/), [setuptools](https://setuptools.readthedocs.io), [wheel](https://pypi.org/project/wheel/) and [twine](https://twine.readthedocs.io). 

```shell
pip install --upgrade setuptools twine wheel --isolated
```

To release `n.n.n`:

```sh
version="n.n.n" # Needs to match new version number in setup.py.
git checkout -b "release-$version"
make precommit && git commit -am"Release $version" && git push --set-upstream origin "release-$version" # If not already all pushed, which it should be.
gh release create "v$version" --target "release-$version" --generate-notes
python setup.py sdist bdist_wheel && twine upload dist/*$version*
git checkout master && git merge "release-$version"
git push
```
