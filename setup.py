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
    long_description = open(readme).read()
except OSError:
    logger.warning("README file not found or unreadable.")
    long_description = "See https://github.com/brunns/brunns-matchers/"

setup(
    name="brunns-matchers",
    zip_safe=False,
    version="2.9.0",
    description="Custom PyHamcrest matchers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Simon Brunning",
    author_email="simon@brunningonline.net",
    url="https://github.com/brunns/brunns-matchers/",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={"": ["README.md"], "brunns": ["py.typed"]},
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.9",
    install_requires=[
        "pyhamcrest>=2.0",
        "Deprecated>=1.2",
        "brunns-row>=2.0",
        "beautifulsoup4==4.13.4",
        "requests>=2.0",
        "httpx>=0.28",
        "yarl>=1.9",
        "furl>=2.0",
        "Werkzeug>=2.0",
    ],
)
