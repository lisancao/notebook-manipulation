#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notebookmanipulation-pkg-ALPHA", # Replace with your own username
    version="0.0.1",
    author="Lisa Cao, David Hays, with Contributions from Cybera",
    author_email="lisa.cao@cybera.ca",
    description="A simple package made by Callysto containing various functions to maintain and update Jupyter Notebooks. Written with educators in mind.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lisancao/notebook-manipulation/tree/package_development",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Jupyter",
        "Programming Language :: Python :: 3",
        "License :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
