#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 14:49:20 2020

@author: lisacao
"""


import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="notebookmanipulation-pkg-LISANCAO", # Replace with your own username
    version="0.0.1",
    author="Lisa Cao, David Hays, with Contributions from Cybera",
    author_email="lisa.cao@cybera.ca",
    description="A simple package made by Callysto containing various functions to maintain and update Jupyter Notebooks. Written with educators in mind.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lisancao/notebook-manipulation/tree/package_development",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
