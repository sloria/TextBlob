import os
import unittest

import pytest

import textblob.taggers
from textblob.base import BaseTagger

HERE = os.path.abspath(os.path.dirname(__file__))
AP_MODEL_LOC = os.path.join(HERE, "trontagger.pickle")


class TestPatternTagger(unittest.TestCase):
    def setUp(self):
        self.text = (
            "Simple is better than complex. " "Complex is better than complicated."
        )
        self.tagger = textblob.taggers.PatternTagger()

    def test_init(self):
        tagger = textblob.taggers.PatternTagger()
        assert isinstance(tagger, textblob.taggers.BaseTagger)

    def test_tag(self):
        tags = self.tagger.tag(self.text)
        assert tags == [
            ("Simple", "JJ"),
            ("is", "VBZ"),
            ("better", "JJR"),
            ("than", "IN"),
            ("complex", "JJ"),
            (".", "."),
            ("Complex", "NNP"),
            ("is", "VBZ"),
            ("better", "JJR"),
            ("than", "IN"),
            ("complicated", "VBN"),
            (".", "."),
        ]


@pytest.mark.slow
@pytest.mark.numpy
class TestNLTKTagger(unittest.TestCase):
    def setUp(self):
        self.text = (
            "Simple is better than complex. " "Complex is better than complicated."
        )
        self.tagger = textblob.taggers.NLTKTagger()

    def test_tag(self):
        tags = self.tagger.tag(self.text)
        assert tags == [
            ("Simple", "NN"),
            ("is", "VBZ"),
            ("better", "JJR"),
            ("than", "IN"),
            ("complex", "JJ"),
            (".", "."),
            ("Complex", "NNP"),
            ("is", "VBZ"),
            ("better", "JJR"),
            ("than", "IN"),
            ("complicated", "VBN"),
            (".", "."),
        ]


def test_cannot_instantiate_incomplete_tagger():
    class BadTagger(BaseTagger):
        """A tagger without a tag method. How useless."""

        pass

    with pytest.raises(TypeError):
        BadTagger()


if __name__ == "__main__":
    unittest.main()
