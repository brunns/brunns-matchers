import logging
import os

from setuptools import find_packages, setup

logger = logging.getLogger(__name__)

# Get the base directory
here = os.path.dirname(__file__)
if not here:
    here = os.path.curdir
here = os.path.abspath(here)

try:
    readme = os.path.join(here, "README.md")
    long_description = open(readme, "r").read()
except IOError:
    logger.warning("README file not found or unreadable.")
    long_description = "See https://github.com/brunns/brunns-matchers/"

setup(
    name="brunns-matchers",
    zip_safe=False,
    version="1.6.1",
    description="Custom PyHamcrest matchers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Simon Brunning",
    author_email="simon@brunningonline.net",
    url="https://github.com/brunns/brunns-matchers/",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["README.md"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=2.7",
    install_requires=[
        "furl~=2.0",
        # "attrs~=18.0",
        # "more_itertools~=4.0",
        "pyhamcrest~=1.9",
        "pytest~=3.0",
        # 'enum34~=1.0;python_version<"3.4"',
        "six~=1.0",
        # "pendulum~=2.0",
        "beautifulsoup4~=4.0",
        # "python-box~=3.2",
        # 'singledispatch~=3.4;python_version<"3.4"',
        # 'pathlib~=1.0;python_version<"3.4"',
        # 'functools32~=3.2;python_version<"3.2"',
        "brunns-row~=1.0",
    ],
)
