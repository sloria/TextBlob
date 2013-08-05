# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
from nose.tools import *  # PEP8 asserts
from nose.plugins.attrib import attr

import text.taggers

class TestPatternTagger(unittest.TestCase):

    def setUp(self):
        self.text = ("Simple is better than complex. "
                    "Complex is better than complicated.")
        self.tagger = text.taggers.PatternTagger()

    def test_init(self):
        tagger = text.taggers.PatternTagger()
        assert_true(isinstance(tagger, text.taggers.BaseTagger))

    def test_tag(self):
        tags = self.tagger.tag(self.text)
        print(tags)
        assert_equal(tags,
            [('Simple', 'NN'), ('is', 'VBZ'), ('better', 'JJR'),
            ('than', 'IN'), ('complex', 'NN'), ('.', '.'),
            ('Complex', 'NNP'), ('is', 'VBZ'), ('better', 'RBR'),
            ('than', 'IN'), ('complicated', 'VBN'), ('.', '.')])

@attr("py2_only")
@attr("slow")
@attr("requires_numpy")
class TestNLTKTagger(unittest.TestCase):

    def setUp(self):
        self.text = ("Simple is better than complex. "
                    "Complex is better than complicated.")
        self.tagger = text.taggers.NLTKTagger()

    def test_tag(self):
        tags = self.tagger.tag(self.text)
        print(tags)
        assert_equal(tags,
            [('Simple', 'NNP'), ('is', 'VBZ'),
            ('better', 'JJR'), ('than', 'IN'),
            ('complex.', 'NNP'), ('Complex', 'NNP'),
            ('is', 'VBZ'), ('better', 'JJR'),
            ('than', 'IN'), ('complicated', 'JJ'), ('.', '.')])


if __name__ == '__main__':
    unittest.main()