#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='odentify',
    author='ygreenc',
    version='0.0.1',
    packages=find_packages(exclude=['tests']),
    test_suite="tests"
)
