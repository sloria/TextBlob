import unittest

import pytest

from textblob.decorators import requires_nltk_corpus
from textblob.exceptions import MissingCorpusError


class Tokenizer:
    @requires_nltk_corpus
    def tag(self, text):
        raise LookupError


def test_decorator_raises_missing_corpus_exception():
    t = Tokenizer()
    with pytest.raises(MissingCorpusError):
        t.tag("hello world")


if __name__ == "__main__":
    unittest.main()
