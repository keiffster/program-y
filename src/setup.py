#!/usr/bin/env python


"""
Setup script for programy
"""


import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as f:
    readme_content = f.read().strip()


version = None
author = None
email = None
source = None

with open(os.path.join('programy', '__init__.py')) as f:
    for line in f:
        if line.strip().startswith('__version__'):
            version = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__author__'):
            author = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__email__'):
            email = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif line.strip().startswith('__source__'):
            source = line.split('=')[1].strip().replace('"', '').replace("'", '')
        elif None not in (version, author, email, source):
            break

setup(
    name='programy',
    author=author,
    author_email=email,
    license='BSD License',
    keywords=["programy python3 aiml interpreter "],
    description="AIML Interpreter for Python 3.x",
    long_description=readme_content,
    classifiers=[
        'Development Status :: 3 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: BSD License',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Chat',
    ],
    include_package_data=True,
    packages=['programy'],
    install_requires=[
        'requests',
        'flask',
        'python-dateutil',
        'beautifulsoup4',
        'lxml',
        'wikipedia',
        'pyyaml',
        'tweepy',
        'sleekxmpp',
        'fbmessenger'
    ],
    url=source,
    version=version,
    zip_safe=True,
)
