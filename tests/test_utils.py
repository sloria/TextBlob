import os
from unittest import TestCase

from textblob.utils import is_filelike, lowerstrip, strip_punc

HERE = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(HERE, "data.csv")


class UtilsTests(TestCase):
    def setUp(self):
        self.text = "this. Has. Punctuation?! "

    def test_strip_punc(self):
        assert strip_punc(self.text) == "this. Has. Punctuation"

    def test_strip_punc_all(self):
        assert strip_punc(self.text, all=True) == "this Has Punctuation"

    def test_lowerstrip(self):
        assert lowerstrip(self.text) == "this. has. punctuation"


def test_is_filelike():
    with open(CSV_FILE) as fp:
        assert is_filelike(fp)
    assert not is_filelike("notafile")
    assert not is_filelike(12.3)
