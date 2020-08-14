#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-oura",
    version="0.1.0",
    description="Singer.io tap for extracting data",
    author="Al Whatmough",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_oura"],
    install_requires=[
        "singer-python>=5.0.12",
        "requests"
    ],
    entry_points="""
    [console_scripts]
    tap-oura=tap_oura:main
    """,
    packages=["tap_oura"],
    package_dir={'tap_oura': 'tap_oura'}
    #package_data = {
    #    "schemas": ["{{cookiecutter.package_name}}/schemas/*.json"]
    #},
#    include_package_data=True,
)
