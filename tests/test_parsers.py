# -*- coding: utf-8 -*-
import unittest
from nose.tools import *  # PEP8 asserts

from textblob.parsers import PatternParser
from textblob.en import parse as pattern_parse


class TestPatternParser(unittest.TestCase):

    def setUp(self):
        self.parser = PatternParser()
        self.text = "And now for something completely different."

    def test_parse(self):
        assert_equal(self.parser.parse(self.text), pattern_parse(self.text))


if __name__ == '__main__':
    unittest.main()
