# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
from nose.tools import *  # PEP8 asserts
from nose.plugins.attrib import attr
from collections import defaultdict

import text.taggers



class TestPerceptronTagger(unittest.TestCase):
    def setUp(self):
        self.text = ("Simple is better than complex. "
                     "Complex is better than complicated.")
        self.tagger = text.taggers.PerceptronTagger(load=False)

    def test_init(self):
        tagger = text.taggers.PerceptronTagger()
        assert_true(isinstance(tagger, text.taggers.BaseTagger))

    def test_train(self):
        sentences = _read_tagged(_wsj_train)
        nr_iter = 5
        self.tagger.train(sentences, nr_iter=nr_iter, quiet=True)
        nr_words = sum(len(words) for words, tags in sentences)
        # Check that the model has 'ticked over' once per instance
        assert_equal(nr_words * nr_iter, self.tagger.model.i)
        # Check that the tagger has a class for every seen tag
        tag_set = set()
        for _, tags in sentences:
            tag_set.update(tags)
        assert_equal(len(tag_set), len(self.tagger.model.classes))
        for tag in tag_set:
            assert_true(tag in self.tagger.model.classes)
        
    def test_tag(self):
        self.tagger.load('/tmp/model')
        tokens = self.tagger.tag(self.text)
        assert_equal([w for w, t in tokens],
            ['Simple', 'is', 'better', 'than', 'complex', '.', 'Complex', 'is',
             'better', 'than', 'complicated', '.'])


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
