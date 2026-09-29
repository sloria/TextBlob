"""Parts-of-speech tagger implementations."""

import nltk

import textblob as tb
from textblob.base import BaseTagger
from textblob.decorators import requires_nltk_corpus
from textblob.en import tag as pattern_tag


class PatternTagger(BaseTagger):
    """Tagger that uses the implementation in
    Tom de Smedt's pattern library
    (http://www.clips.ua.ac.be/pattern).
    """

    def tag(self, text, tokenize=True):
        """Tag a string or BaseBlob."""
        if not isinstance(text, str):
            text = text.raw
        return pattern_tag(text, tokenize)


class NLTKTagger(BaseTagger):
    """Tagger that uses NLTK's standard TreeBank tagger.
    NOTE: Requires numpy. Not yet supported with PyPy.
    """

    @requires_nltk_corpus
    def tag(self, text):
        """Tag a string or BaseBlob."""
        if isinstance(text, str):
            text = tb.TextBlob(text)

        return nltk.tag.pos_tag(text.tokens)
