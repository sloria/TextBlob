from __future__ import unicode_literals
import unittest
from nose.tools import *  # PEP8 asserts
from nose.plugins.attrib import attr

from textblob.sentiments import PatternAnalyzer, NaiveBayesAnalyzer, DISCRETE, CONTINUOUS


class TestPatternSentiment(unittest.TestCase):

    def setUp(self):
        self.analyzer = PatternAnalyzer()

    def test_kind(self):
        assert_equal(self.analyzer.kind, CONTINUOUS)

    def test_analyze(self):
        p1 = "I feel great this morning."
        n1 = "This is a terrible car."
        p1_result = self.analyzer.analyze(p1)
        n1_result = self.analyzer.analyze(n1)
        assert_true(p1_result[0] > 0)
        assert_true(n1_result[0] < 0)
        assert_equal(p1_result.polarity, p1_result[0])
        assert_equal(p1_result.subjectivity, p1_result[1])


class TestNaiveBayesAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = NaiveBayesAnalyzer()

    def test_kind(self):
        assert_equal(self.analyzer.kind, DISCRETE)

    @attr('slow')
    def test_analyze(self):
        p1 = 'I feel great this morning.'
        n1 = 'This is a terrible car.'
        p1_result = self.analyzer.analyze(p1)
        assert_equal(p1_result[0], 'pos')
        assert_equal(self.analyzer.analyze(n1)[0], 'neg')
        # The 2nd item should be the probability that it is positive
        assert_true(isinstance(p1_result[1], float))
        # 3rd item is probability that it is negative
        assert_true(isinstance(p1_result[2], float))
        assert_about_equal(p1_result[1] + p1_result[2], 1)
        assert_equal(p1_result.classification, p1_result[0])
        assert_equal(p1_result.p_pos, p1_result[1])
        assert_equal(p1_result.p_neg, p1_result[2])


def assert_about_equal(first, second, places=4):
    return assert_equal(round(first, places), second)

if __name__ == '__main__':
    unittest.main()
