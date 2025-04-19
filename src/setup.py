#!/usr/bin/env python
from distutils.core import setup

from setuptools import find_packages

setup(
    name='badi_users',
    version='2.4.5',
    author='Mohammad Shekari Badi',
    author_email='Ad.BadiDesign@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/BadiDesign/badi_utils',
    license='LICENSE',
    description='Python Django Users',
    long_description=open('README.md').read(),
    install_requires=[
    ],
)
