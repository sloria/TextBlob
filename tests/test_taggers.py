# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import unittest
from nose.tools import *  # PEP8 asserts
from nose.plugins.attrib import attr

from textblob.exceptions import DeprecationError
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
            [('Simple', 'NN'), ('is', 'VBZ'), ('better', 'JJR'),
            ('than', 'IN'), ('complex', 'NN'), ('.', '.'),
            ('Complex', 'NNP'), ('is', 'VBZ'), ('better', 'RBR'),
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
        print(tags)
        assert_equal(tags,
            [('Simple', 'NNP'), ('is', 'VBZ'),
            ('better', 'JJR'), ('than', 'IN'),
            ('complex.', 'NNP'), ('Complex', 'NNP'),
            ('is', 'VBZ'), ('better', 'JJR'),
            ('than', 'IN'), ('complicated', 'JJ'), ('.', '.')])


class TestPerceptronTagger(unittest.TestCase):

    @attr("py27_only")
    def test_init_raises_deprecation_error(self):
        with assert_raises(DeprecationError):
            textblob.taggers.PerceptronTagger(load=False)

class BadTagger(BaseTagger):
    '''A tagger without a tag method. How useless.'''
    pass


@attr("py27_only")
def test_cannot_instantiate_incomplete_tagger():
    with assert_raises(TypeError):
        BadTagger()


def _read_tagged(text, sep='|'):
    sentences = []
    for sent in text.split('\n'):
        tokens = []
        tags = []
        for token in sent.split():
            word, pos = token.split(sep)
            tokens.append(word)
            tags.append(pos)
        sentences.append((tokens, tags))
    return sentences

_wsj_train = ("Pierre|NNP Vinken|NNP ,|, 61|CD years|NNS old|JJ ,|, will|MD "
              "join|VB the|DT board|NN as|IN a|DT nonexecutive|JJ director|NN "
              "Nov.|NNP 29|CD .|.\nMr.|NNP Vinken|NNP is|VBZ chairman|NN of|IN "
              "Elsevier|NNP N.V.|NNP ,|, the|DT Dutch|NNP publishing|VBG "
              "group|NN .|. Rudolph|NNP Agnew|NNP ,|, 55|CD years|NNS old|JJ "
              "and|CC former|JJ chairman|NN of|IN Consolidated|NNP Gold|NNP "
              "Fields|NNP PLC|NNP ,|, was|VBD named|VBN a|DT nonexecutive|JJ "
              "director|NN of|IN this|DT British|JJ industrial|JJ conglomerate|NN "
              ".|.\nA|DT form|NN of|IN asbestos|NN once|RB used|VBN to|TO make|VB "
              "Kent|NNP cigarette|NN filters|NNS has|VBZ caused|VBN a|DT high|JJ "
              "percentage|NN of|IN cancer|NN deaths|NNS among|IN a|DT group|NN "
              "of|IN workers|NNS exposed|VBN to|TO it|PRP more|RBR than|IN "
              "30|CD years|NNS ago|IN ,|, researchers|NNS reported|VBD .|.")


if __name__ == '__main__':
    unittest.main()
