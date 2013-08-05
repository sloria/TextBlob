import unittest
from nose.tools import *  # PEP8 asserts
from text.tokenizers import WordTokenizer, SentenceTokenizer

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

class TestSentenceTokenizer(unittest.TestCase):

    def setUp(self):
        self.tokenizer = SentenceTokenizer()
        self.text = "Beautiful is better than ugly. Simple is better than complex."

    def test_tokenize(self):
        assert_equal(self.tokenizer.tokenize(self.text),
            ["Beautiful is better than ugly.", "Simple is better than complex."])


if __name__ == '__main__':
    unittest.main()