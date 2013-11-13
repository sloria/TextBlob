# -*- coding: utf-8 -*-
'''Parts-of-speech tagger implementations.'''
from __future__ import absolute_import

from textblob.packages import nltk
from textblob.en import tag as pattern_tag
from textblob.decorators import requires_nltk_corpus
from textblob.exceptions import DeprecationError
from textblob.base import BaseTagger


class PatternTagger(BaseTagger):

    '''Tagger that uses the implementation in
    Tom de Smedt's pattern library
    (http://www.clips.ua.ac.be/pattern).
    '''

    def tag(self, sentence, tokenize=True):
        '''Tag a string `sentence`.'''
        return pattern_tag(sentence, tokenize)


class NLTKTagger(BaseTagger):

    '''Tagger that uses NLTK's standard TreeBank tagger.
    NOTE: Requires numpy. Not yet supported with PyPy.
    '''

    @requires_nltk_corpus
    def tag(self, sentence, tokenize=True):
        '''Tag a string `sentence`.'''
        if tokenize:
            sentence = nltk.tokenize.word_tokenize(sentence)
        tagged = nltk.tag.pos_tag(sentence)
        return tagged


class PerceptronTagger(BaseTagger):

    '''Greedy Averaged Perceptron tagger, as implemented by Matthew Honnibal.
    Requires that ``trontagger.pickle`` exists in the text/en package directory.
    The pickle file can be obtained from the Github Releases page for TextBlob.

    .. note::
        This class is deprecated as of version ``0.7.0``. It is now maintained
        as a TextBlob extension, ``textblob-aptagger``.

    .. deprecated:: 0.7.0
        Install the ``textblob-aptagger`` extension instead.
    '''

    def __init__(self, load=True):
        raise DeprecationError("PerceptronTagger is deprecated. Use "
                        " the textblob-aptagger extension instead")

    def tag(self, sentence, tokenize=True):
        pass
