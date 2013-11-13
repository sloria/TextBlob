# -*- coding: utf-8 -*-
import unittest
from nose.tools import *  # PEP8 asserts

from textblob.tokenizers import WordTokenizer, SentenceTokenizer

class TestWordTokenizer(unittest.TestCase):

    '''An example unit test case.'''

    def setUp(self):
        self.tokenizer = WordTokenizer()
        self.text = "Python is a high-level programming language."

    def tearDown(self):
        pass

    def test_tokenize(self):
        assert_equal(self.tokenizer.tokenize(self.text),
            ['Python', 'is', 'a', 'high-level', 'programming',
            'language', '.'])

    def test_exclude_punc(self):
        assert_equal(self.tokenizer.tokenize(self.text, include_punc=False),
            ['Python', 'is', 'a', 'high-level', 'programming',
            'language'])

    def test_itokenize(self):
        gen = self.tokenizer.itokenize(self.text)
        assert_equal(next(gen), "Python")
        assert_equal(next(gen), "is")


class TestSentenceTokenizer(unittest.TestCase):

    def setUp(self):
        self.tokenizer = SentenceTokenizer()
        self.text = "Beautiful is better than ugly. Simple is better than complex."

    def test_tokenize(self):
        assert_equal(self.tokenizer.tokenize(self.text),
            ["Beautiful is better than ugly.", "Simple is better than complex."])

    @unittest.skip("This is a known problem with the sentence tokenizer. Skipping for now.")
    def test_tokenize_with_multiple_punctuation(self):
        text = "Hello world. How do you do?! My name's Steve..."
        assert_equal(self.tokenizer.tokenize(text),
            ["Hello world.", "How do you do?!", "My name's Steve..."])
        text2 = 'OMG! I am soooo LOL!!!'
        tokens = self.tokenizer.tokenize(text2)
        assert_equal(len(tokens), 2)
        assert_equal(tokens,
            ["OMG!", "I am soooo LOL!!!"])

    def test_itokenize(self):
        gen = self.tokenizer.itokenize(self.text)
        assert_equal(next(gen), "Beautiful is better than ugly.")
        assert_equal(next(gen), "Simple is better than complex.")

if __name__ == '__main__':
    unittest.main()
