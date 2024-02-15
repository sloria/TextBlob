import unittest

import pytest

from textblob.tokenizers import (
    SentenceTokenizer,
    WordTokenizer,
    sent_tokenize,
    word_tokenize,
)


def is_generator(obj):
    return hasattr(obj, "__next__")


class TestWordTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = WordTokenizer()
        self.text = "Python is a high-level programming language."

    def tearDown(self):
        pass

    def test_tokenize(self):
        assert self.tokenizer.tokenize(self.text) == [
            "Python",
            "is",
            "a",
            "high-level",
            "programming",
            "language",
            ".",
        ]

    def test_exclude_punc(self):
        assert self.tokenizer.tokenize(self.text, include_punc=False) == [
            "Python",
            "is",
            "a",
            "high-level",
            "programming",
            "language",
        ]

    def test_itokenize(self):
        gen = self.tokenizer.itokenize(self.text)
        assert next(gen) == "Python"
        assert next(gen) == "is"

    def test_word_tokenize(self):
        tokens = word_tokenize(self.text)
        assert is_generator(tokens)
        assert list(tokens) == self.tokenizer.tokenize(self.text)


class TestSentenceTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = SentenceTokenizer()
        self.text = "Beautiful is better than ugly. Simple is better than complex."

    def test_tokenize(self):
        assert self.tokenizer.tokenize(self.text) == [
            "Beautiful is better than ugly.",
            "Simple is better than complex.",
        ]

    @pytest.mark.skip  # This is a known problem with the sentence tokenizer.
    def test_tokenize_with_multiple_punctuation(self):
        text = "Hello world. How do you do?! My name's Steve..."
        assert self.tokenizer.tokenize(text) == [
            "Hello world.",
            "How do you do?!",
            "My name's Steve...",
        ]
        text2 = "OMG! I am soooo LOL!!!"
        tokens = self.tokenizer.tokenize(text2)
        assert len(tokens) == 2
        assert tokens == ["OMG!", "I am soooo LOL!!!"]

    def test_itokenize(self):
        gen = self.tokenizer.itokenize(self.text)
        assert next(gen) == "Beautiful is better than ugly."
        assert next(gen) == "Simple is better than complex."

    def test_sent_tokenize(self):
        tokens = sent_tokenize(self.text)
        assert is_generator(tokens)  # It's a generator
        assert list(tokens) == self.tokenizer.tokenize(self.text)


if __name__ == "__main__":
    unittest.main()
