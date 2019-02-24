import os
from .blob import TextBlob, Word, Sentence, Blobber, WordList

__version__ = '0.15.3'
__license__ = 'MIT'
__author__ = 'Steven Loria'

PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))

__all__ = [
    'TextBlob',
    'Word',
    'Sentence',
    'Blobber',
    'WordList',
]
