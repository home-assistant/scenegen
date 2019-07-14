#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scenegen",
    version="0.0.2",
    author="Andrew Cockburn",
    author_email="andrew@acockburn.com",
    description="Generate scenes for Home Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/home-assistant/scenegen",
    py_modules=["scenegen"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",

        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Home Automation",
        "Topic :: Utilities",
    ],

    entry_points={
        'console_scripts': [
            'scenegen=scenegen:main',
        ],
},)
