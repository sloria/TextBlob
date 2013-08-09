# -*- coding: utf-8 -*-
'''Various tokenizer implementations.'''

from .packages import nltk
from .utils import strip_punc


class BaseTokenizer(nltk.tokenize.api.TokenizerI):

    '''Abstract base class from which all Tokenizer classes inherit.

    Descendant classes should implement an API like so: ::

        >>> from text.tokenizers import MyTokenizer
        >>> tokenizer = MyTokenizer()
        >>> text = "I am a sentence."
        >>> tokenizer.tokenize(text)
        ['I', 'am', 'a', 'sentence.']

    In other words, descendant classes must implement a ``tokenize(text)`` method
    that returns a list of noun phrases as strings.
    '''

    def tokenize(self, text):
        '''Return a list of tokens (strings) for a body of text.'''
        raise NotImplementedError('Must implement a tokenize(text) method')


class WordTokenizer(BaseTokenizer):

    '''NLTK's recommended word tokenizer (currently the TreeBankTokenizer).
    Uses regular expressions to tokenize text. Assumes text has already been
    segmented into sentences.

    Performs the following steps:

    * split standard contractions, e.g. don't -> do n't
    * treat most punctuation characters as separate tokens
    * split commas and single quotes
    * separate periods that appear at the end of line
    '''

    def tokenize(self, text, include_punc=True):
        '''Return a list of word tokens.

        :param text: string of text.
        :param include_punc: (optional) whether to include punctuation as separate tokens. Default to True.
        '''
        tokens = nltk.tokenize.word_tokenize(text)
        if include_punc:
            return tokens
        else:
            return [strip_punc(word) for word in tokens if strip_punc(word)]

class SentenceTokenizer(BaseTokenizer):

    '''NLTK's sentence tokenizer (currently PunkSentenceTokenizer).
    Uses an unsupervised algorithm to build a model for abbreviation owrds,
    collocations, and words, collocations, and words, that start sentences,
    then uses that to find sentence boundaries.
    '''

    def tokenize(self, text):
        return nltk.tokenize.sent_tokenize(text)
