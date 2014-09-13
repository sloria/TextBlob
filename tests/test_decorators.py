# -*- coding: utf-8 -*-
import unittest
from nose.plugins.attrib import attr
from nose.tools import *  # PEP8 asserts

from textblob.decorators import requires_nltk_corpus
from textblob.exceptions import MissingCorpusError


class Tokenizer(object):

    @requires_nltk_corpus
    def tag(self, text):
        raise LookupError


def test_decorator_raises_missing_corpus_exception():
    t = Tokenizer()
    assert_raises(MissingCorpusError, lambda: t.tag('hello world'))

if __name__ == '__main__':
    unittest.main()
