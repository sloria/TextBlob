# -*- coding: utf-8 -*-
'''Abstract base classes for models (taggers, noun phrase extractors, etc.)
which define the interface for descendant classes.
'''
from __future__ import absolute_import
from text.packages import nltk

##### POS TAGGERS #####

class BaseTagger(object):

    '''Abstract tagger class from which all taggers
    inherit from. All descendants must implement a
    `tag()` method.
    '''

    def tag(self, sentence, tokenize=True):
        '''Return a list of tuples of the form (word, tag)
        for a given set of text.
        '''
        raise NotImplementedError('Must implement a tag() method')

##### NOUN PHRASE EXTRACTORS #####

class BaseNPExtractor(object):

    '''Abstract base class from which all NPExtractor classes inherit.

    Descendant classes should implement an API, like so: ::

        >>> from text.np_extractor import MyExtractor
        >>> extractor = MyExtractor()
        >>> text = "Python is a high-level scripting language."
        >>> extractor.extract(text)
        ['Python', 'scripting language']

    In other words, descendant classes must implement an ``extract(text)`` method
    that returns a list of noun phrases as strings.
    '''

    def extract(self, text):
        '''Return a list of noun phrases (strings) for a body of text.'''
        raise NotImplementedError('Must implement an extract(text) method')

##### TOKENIZERS #####

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
        '''Return a list of tokens (strings) for a body of text.

        :rtype: list
        '''
        raise NotImplementedError('Must implement a tokenize(text) method')

    def itokenize(self, text, *args, **kwargs):
        '''Return a generator that generates tokens "on-demand".

        .. versionadded:: 0.6.0

        :rtype: generator
        '''
        return (t for t in self.tokenize(text, *args, **kwargs))

##### SENTIMENT ANALYZERS ####

DISCRETE = 'ds'
CONTINUOUS = 'co'


class BaseSentimentAnalyzer(object):

    '''Abstract base class from which all sentiment analyzers inherit.
    Should implement an ``analyze(text)`` method which returns either the
    results of analysis.
    '''

    kind = DISCRETE

    def __init__(self):
        self._trained = False

    def train(self):
        # Train me
        self._trained = True

    def analyze(self, text):
        '''Return the result of of analysis. Typically returns either a
        tuple, float, or dictionary.'''
        # Lazily train the classifier
        if not self._trained:
            self.train()
        # Analyze text
        return None

##### PARSERS #####

class BaseParser(object):

    '''Abstract parser class from which all parsers inherit from. All
    descendants must implement a `parse()` method.
    '''

    def parse(self, text):
        '''Parses the text.'''
        raise NotImplementedError("Must implement a parse() method.")
