#!/usr/bin/python
# -*- coding: utf-8 -*-

"""setup.py for trivector"""

import codecs
import re
import sys
import os
from setuptools import setup, find_packages
from setuptools.command.test import test


def find_version(*file_paths):
    with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)), *file_paths), 'r') as fp:
        version_file = fp.read()
    m = re.search(r"^__version__ = \((\d+), ?(\d+), ?(\d+)\)", version_file, re.M)
    if m:
        return "{}.{}.{}".format(*m.groups())
    raise RuntimeError("Unable to find a valid version")


NAME = "trivector"
SAFE_NAME = NAME.replace("-", "_")
VERSION = find_version(SAFE_NAME, "__init__.py")
DESCRIPTION = "Convert an image into a ``.svg`` vector image composed of triangles"


class Sphinx(test):
    def run_tests(self):
        from sphinx.ext.apidoc import main as apidoc
        from sphinx.cmd.build import build_main

        # generate api docs
        apidoc(["--module-first", "--separate", "--output-dir", "doc/api",
                "--implicit-namespaces", SAFE_NAME])

        # build sphinx
        build_main(
            [
                "doc", "build/sphinx", "-E",
                "-D", "version={}".format(VERSION[:3]),
                "-D", "release={}".format(VERSION),
                "-D", "project={}".format(NAME)
            ]
        )


class Pylint(test):
    def run_tests(self):
        from pylint.lint import Run
        Run(["trivector", "--persistent", "y"])


class PyTest(test):
    user_options = [('pytest-args=', 'a', "Arguments to pass to pytest")]

    def initialize_options(self):
        test.initialize_options(self)
        self.pytest_args = "-v --cov={}".format(SAFE_NAME)

    def run_tests(self):
        import shlex
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(shlex.split(self.pytest_args))
        sys.exit(errno)


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=readme(),
    author="Nathan Klapstein",
    author_email="nklapste@ualberta.ca",
    url="https://github.com/nklapste/trivector",
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    package_data={
        "": ["README.rst"],
    },
    entry_points={
        "console_scripts": [
            "trivector = trivector.__main__:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Multimedia :: Graphics :: Editors :: Vector-Based",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],
    install_requires=[
        "svgwrite>=1.1.12,<2.0.0",
        "opencv-python>=3.4.1.15,<4.0.0.0",
        "numpy>=1.14.3,<2.0.0",
        "progressbar2>=3.37.1,<4.0.0",
    ],
    extras_require={
        "docs": [
            "sphinx>=1.7.5,<2.0.0",
            "sphinx_rtd_theme>=0.3.1,<1.0.0",
            "sphinx-autodoc-typehints>=1.3.0,<2.0.0",
            "sphinx-argparse>=0.2.2,<1.0.0",
        ]
    },
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-timeout",
        "pylint>=1.9.1,<2.0.0",
    ],
    cmdclass={"build_sphinx": Sphinx, "test": PyTest, "lint": Pylint},
)
