#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages

REQUIREMENTS = ['nltk>=3.0']
TEST_REQUIREMENTS = ['nose', 'mock']


def find_version(fname):
    """Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version

__version__ = find_version("textblob/__init__.py")


def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    name='textblob',
    version=__version__,
    description='Simple, Pythonic text processing. Sentiment analysis, '
                'part-of-speech tagging, noun phrase parsing, and more.',
    long_description=read("README.rst"),
    license=read("LICENSE"),
    author='Steven Loria',
    author_email='sloria1@gmail.com',
    url='https://github.com/sloria/TextBlob',
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=('test*', )),
    include_package_data=True,
    zip_safe=False,
    package_data={
        "textblob.en": ["*.txt", "*.xml"]
    },
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        "Topic :: Text Processing :: Linguistic",
    ),
    tests_require=TEST_REQUIREMENTS,
    keywords=["textblob", "nlp", 'linguistics', 'nltk', 'pattern']
)
