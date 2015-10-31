# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import unittest
from nose.tools import *  # PEP8 asserts
from nose.plugins.attrib import attr

from textblob.base import BaseTagger
import textblob.taggers

HERE = os.path.abspath(os.path.dirname(__file__))
AP_MODEL_LOC = os.path.join(HERE, 'trontagger.pickle')


class TestPatternTagger(unittest.TestCase):

    def setUp(self):
        self.text = ("Simple is better than complex. "
                    "Complex is better than complicated.")
        self.tagger = textblob.taggers.PatternTagger()

    def test_init(self):
        tagger = textblob.taggers.PatternTagger()
        assert_true(isinstance(tagger, textblob.taggers.BaseTagger))

    def test_tag(self):
        tags = self.tagger.tag(self.text)
        assert_equal(tags,
            [('Simple', 'JJ'), ('is', 'VBZ'), ('better', 'JJR'),
            ('than', 'IN'), ('complex', 'JJ'), ('.', '.'),
            ('Complex', 'NNP'), ('is', 'VBZ'), ('better', 'JJR'),
            ('than', 'IN'), ('complicated', 'VBN'), ('.', '.')])


@attr("slow")
@attr("no_pypy")
@attr("requires_numpy")
class TestNLTKTagger(unittest.TestCase):

    def setUp(self):
        self.text = ("Simple is better than complex. "
                    "Complex is better than complicated.")
        self.tagger = textblob.taggers.NLTKTagger()

    def test_tag(self):
        tags = self.tagger.tag(self.text)
        assert_equal(tags,
            [('Simple', 'NN'), ('is', 'VBZ'),
            ('better', 'JJR'), ('than', 'IN'),
            ('complex', 'JJ'), ('.', '.'), ('Complex', 'NNP'),
            ('is', 'VBZ'), ('better', 'JJR'),
            ('than', 'IN'), ('complicated', 'VBN'), ('.', '.')])


def test_cannot_instantiate_incomplete_tagger():
    class BadTagger(BaseTagger):
        '''A tagger without a tag method. How useless.'''
        pass
    assert_raises(TypeError, lambda: BadTagger())

if __name__ == '__main__':
    unittest.main()
