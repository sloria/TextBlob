# -*- coding: utf-8 -*-
"""Parts-of-speech tagger implementations."""
from __future__ import absolute_import

import nltk

from textblob.en import tag as pattern_tag
from textblob.decorators import requires_nltk_corpus
from textblob.tokenizers import word_tokenize
from textblob.base import BaseTagger


class PatternTagger(BaseTagger):
    """Tagger that uses the implementation in
    Tom de Smedt's pattern library
    (http://www.clips.ua.ac.be/pattern).
    """

    def tag(self, text, tokenize=True):
        """Tag a string `text`."""
        return pattern_tag(text, tokenize)


class NLTKTagger(BaseTagger):
    """Tagger that uses NLTK's standard TreeBank tagger.
    NOTE: Requires numpy. Not yet supported with PyPy.
    """

    @requires_nltk_corpus
    def tag(self, text, tokenize=True):
        """Tag a string `text`."""
        if tokenize:
            text = list(word_tokenize(text))
        tagged = nltk.tag.pos_tag(text)
        return tagged
