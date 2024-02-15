import unittest

import nltk
import pytest

from textblob.base import BaseNPExtractor
from textblob.np_extractors import ConllExtractor
from textblob.utils import filter_insignificant


class TestConllExtractor(unittest.TestCase):
    def setUp(self):
        self.extractor = ConllExtractor()
        self.text = """
Python is a widely used general-purpose,
high-level programming language. Its design philosophy emphasizes code
readability, and its syntax allows programmers to express concepts in fewer lines
of code than would be possible in other languages. The language provides
constructs intended to enable clear programs on both a small and large scale.
"""
        self.sentence = (
            "Python is a widely used general-purpose, high-level programming language"
        )

    @pytest.mark.slow
    def test_extract(self):
        noun_phrases = self.extractor.extract(self.text)
        assert "Python" in noun_phrases
        assert "design philosophy" in noun_phrases
        assert "code readability" in noun_phrases

    @pytest.mark.slow
    def test_parse_sentence(self):
        parsed = self.extractor._parse_sentence(self.sentence)
        assert isinstance(parsed, nltk.tree.Tree)

    @pytest.mark.slow
    def test_filter_insignificant(self):
        chunk = self.extractor._parse_sentence(self.sentence)
        tags = [tag for word, tag in chunk.leaves()]
        assert "DT" in tags
        filtered = filter_insignificant(chunk.leaves())
        tags = [tag for word, tag in filtered]
        assert "DT" not in tags


class BadExtractor(BaseNPExtractor):
    """An extractor without an extract method. How useless."""

    pass


def test_cannot_instantiate_incomplete_extractor():
    with pytest.raises(TypeError):
        BadExtractor()


if __name__ == "__main__":
    unittest.main()
