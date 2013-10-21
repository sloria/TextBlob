# -*- coding: utf-8 -*-

from unittest import TestCase
from nose.tools import *  # PEP8 asserts

from textblob.utils import lowerstrip, strip_punc

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

