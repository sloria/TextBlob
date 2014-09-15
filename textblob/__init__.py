import os

__version__ = '0.9.0'
__license__ = 'MIT'
__author__ = 'Steven Loria'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

from .blob import TextBlob, Word, Sentence, Blobber, WordList

__all__ = [
    'TextBlob',
    'Word',
    'Sentence',
    'Blobber',
    'WordList',
]
