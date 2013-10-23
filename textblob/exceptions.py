# -*- coding: utf-8 -*-

MISSING_CORPUS_MESSAGE = """
Looks like you are missing some required data for this feature.

To download the necessary data, simply run

    curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python

Or use the NLTK downloader to download the missing data: http://nltk.org/data.html
If this doesn't fix the problem, file an issue at https://github.com/sloria/TextBlob/issues.
"""

class TextBlobException(Exception):
    '''A TextBlob-related exception.'''

class MissingCorpusException(TextBlobException):

    '''Exception thrown when a user tries to use a feature that requires a
    dataset or model that the user does not have on their system.
    '''

    def __init__(self, message=MISSING_CORPUS_MESSAGE, *args, **kwargs):
        super(MissingCorpusException, self).__init__(message, *args, **kwargs)

class DeprecationError(TextBlobException):
    '''Raised when user uses a deprecated feature.'''
    pass
