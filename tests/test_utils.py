# -*- coding: utf-8 -*-

from unittest import TestCase
import os

from nose.tools import *  # PEP8 asserts

from textblob.utils import lowerstrip, strip_punc, is_filelike

HERE = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(HERE, 'data.csv')

class UtilsTests(TestCase):
    def setUp(self):
        self.text = "this. Has. Punctuation?! "

    def test_strip_punc(self):
        assert_equal(strip_punc(self.text),
                    'this. Has. Punctuation')

    def test_strip_punc_all(self):
        assert_equal(strip_punc(self.text, all=True),
                    'this Has Punctuation')

    def test_lowerstrip(self):
        assert_equal(lowerstrip(self.text),
                    'this. has. punctuation')


def test_is_filelike():
    with open(CSV_FILE) as fp:
        assert_true(is_filelike(fp))
    assert_false(is_filelike('notafile'))
    assert_false(is_filelike(12.3))
