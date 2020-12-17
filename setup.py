#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
import os
from setuptools import find_packages

try:
    with open("README.md") as f:
        readme = f.read()
except IOError:
    readme = ""


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setup(
    name="pyzzle",
    version="0.0.1",
    url="https://github.com/MakePuzz/pyzzle",
    author="The MakePuzz team",
    author_email="puzzle.hokkaido@gmail.com",
    maintainer="The MakePuzz team",
    maintainer_email="puzzle.hokkaido@gmail.com",
    description="A Python library to automatically generate intelligent and beautifull puzzles",
    long_description=readme,
    packages=find_packages(),
    install_requires=_requires_from_file("requirements.txt"),
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      pyzzle = pyzzle.script.command:main
    """,
)
