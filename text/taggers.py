# -*- coding: utf-8 -*-
'''Parts-of-speech tagger implementations.'''
from .packages import nltk
from .en import tag as pattern_tag
from .exceptions import MissingCorpusException

class BaseTagger(object):

    '''Abstract tagger class from which all taggers
    inherit from. All descendants must implement a
    `tag()` method.
    '''

    def tag(self, sentence):
        '''Return a list of tuples of the form (word, tag)
        for a given set of text.
        '''
        raise NotImplementedError('Must implement a tag() method')


class PatternTagger(BaseTagger):

    '''Tagger that uses the implementation in
    Tom de Smedt's pattern library
    (http://www.clips.ua.ac.be/pattern).
    '''

    def tag(self, sentence, tokenize=True):
        return pattern_tag(sentence, tokenize)

class NLTKTagger(BaseTagger):

    '''Tagger that uses NLTK's standard TreeBank tagger.
    NOTE: Currently supported on Python 2 only, and requires numpy.
    '''

    def tag(self, sentence, tokenize=True):
        if tokenize:
            sentence = nltk.tokenize.word_tokenize(sentence)
        try:
            tagged = nltk.tag.pos_tag(sentence)
        except LookupError as e:
            print(e)
            raise MissingCorpusException()
        return tagged


