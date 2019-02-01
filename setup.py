#! /usr/bin/env python3

from setuptools import setup

with open("README.md") as readme:
    long_desc = readme.read()

version = "0.1"

setup(
    name="argstore",
    version=version,
    author="Ivan Rusinov",
    author_email="isrusin.devel@gmail.com",
    description="Argparse wrapper for dumping of execution options",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/isrusin/argstore",
    py_modules=["argstore"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)

