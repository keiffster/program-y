#!/usr/bin/env python
from distutils.core import setup

setup(
    name='MetOffer',
    version='1.3.2',
    author='Stephen B Murray',
    author_email='sbm199@gmail.com',
    py_modules=['metoffer'],
    url='http://pypi.python.org/pypi/MetOffer/',
    license='LICENSE.txt',
    description='Simple wrapper for the Met Office DataPoint API.',
    long_description=open('README.rst').read(),
)
