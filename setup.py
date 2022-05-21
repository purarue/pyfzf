#!/usr/bin/env python

import os
from setuptools import setup

prjdir = os.path.dirname(__file__)


def read(filename):
    return open(os.path.join(prjdir, filename)).read()


def main() -> None:
    setup(
        name="pyfzf_iter",
        include_package_data=True,
        version="0.0.1",
        description="Python wrapper for junegunn's fuzzyfinder (fzf)",
        long_description=read("README.md"),
        long_description_content_type="text/markdown",
        author="Sean Breckenridge",
        license="MIT",
        url="https://github.com/seanbreckenridge/pyfzf",
        install_requires=[],
        py_modules=["pyfzf"],
        packages=["pyfzf"],
        package_data={"pyfzf": ["py.typed"]},
        python_requires=">=3.6",
        classifiers=[
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Terminals",
        ],
    )


if __name__ == "__main__":
    main()
