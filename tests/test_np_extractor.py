from __future__ import unicode_literals
import unittest
from nose.tools import *  # PEP8 asserts
from nose.plugins.attrib import attr

import nltk

from textblob.base import BaseNPExtractor
from textblob.np_extractors import ConllExtractor
from textblob.utils import filter_insignificant


class TestConllExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = ConllExtractor()
        self.text = '''
Python is a widely used general-purpose,
high-level programming language. Its design philosophy emphasizes code
readability, and its syntax allows programmers to express concepts in fewer lines
of code than would be possible in other languages. The language provides
constructs intended to enable clear programs on both a small and large scale.
'''
        self.sentence = "Python is a widely used general-purpose, high-level programming language"

    @attr('slow')
    def test_extract(self):
        noun_phrases = self.extractor.extract(self.text)
        assert_true("Python" in noun_phrases)
        assert_true("design philosophy" in noun_phrases)
        assert_true("code readability" in noun_phrases)

    @attr('slow')
    def test_parse_sentence(self):
        parsed = self.extractor._parse_sentence(self.sentence)
        assert_true(isinstance(parsed, nltk.tree.Tree))

    @attr('slow')
    def test_filter_insignificant(self):
        chunk = self.extractor._parse_sentence(self.sentence)
        tags = [tag for word, tag in chunk.leaves()]
        assert_true('DT' in tags)
        filtered = filter_insignificant(chunk.leaves())
        tags = [tag for word, tag in filtered]
        assert_true("DT" not in tags)


class BadExtractor(BaseNPExtractor):
    '''An extractor without an extract method. How useless.'''
    pass


def test_cannot_instantiate_incomplete_extractor():
    assert_raises(TypeError,
        lambda: BadExtractor())

if __name__ == '__main__':
    unittest.main()
