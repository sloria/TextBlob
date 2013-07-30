# -*- coding: utf-8 -*-

import nltk
from nltk.tag import pos_tag as nltk_tag
from .en import tag as pattern_tag

class BaseTagger(object):

    '''Abstract tagger class from which all taggers
    inherit from. All descendants must implement a
    `tag()` method.
    '''

    def tag(self, sentence):
        '''Return a list of tuples of the form (word, tag)
        for a given set of text.
        '''
        raise(NotImplementedError, 'Must implement a tag() method')


class PatternTagger(BaseTagger):

    '''Tagger that uses the implementation in
    Tom de Smedt's pattern library
    (http://www.clips.ua.ac.be/pattern).
    '''

    def tag(self, sentence, tokenize=True):
        return pattern_tag(sentence, tokenize)

class NLTKTagger(BaseTagger):

    '''Tagger that uses NLTK's standard TreeBank tagger.
    NOTE: Requires numpy.
    '''

    def tag(self, sentence, tokenize=True):
        if tokenize:
            sentence = nltk.tokenize.word_tokenize(sentence)
        return nltk_tag(sentence)


