import unittest

import pytest

from textblob.sentiments import (
    CONTINUOUS,
    DISCRETE,
    NaiveBayesAnalyzer,
    PatternAnalyzer,
)


class TestPatternSentiment(unittest.TestCase):
    def setUp(self):
        self.analyzer = PatternAnalyzer()

    def test_kind(self):
        assert self.analyzer.kind == CONTINUOUS

    def test_analyze(self):
        p1 = "I feel great this morning."
        n1 = "This is a terrible car."
        p1_result = self.analyzer.analyze(p1)
        n1_result = self.analyzer.analyze(n1)
        assert p1_result[0] > 0
        assert n1_result[0] < 0
        assert p1_result.polarity == p1_result[0]
        assert p1_result.subjectivity == p1_result[1]

    def test_analyze_assessments(self):
        p1 = "I feel great this morning."
        n1 = "This is a terrible car."
        p1_result = self.analyzer.analyze(p1, keep_assessments=True)
        n1_result = self.analyzer.analyze(n1, keep_assessments=True)
        p1_assessment = p1_result.assessments[0]
        n1_assessment = n1_result.assessments[0]
        assert p1_assessment[1] > 0
        assert n1_assessment[1] < 0
        assert p1_result.polarity == p1_assessment[1]
        assert p1_result.subjectivity == p1_assessment[2]


class TestNaiveBayesAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = NaiveBayesAnalyzer()

    def test_kind(self):
        assert self.analyzer.kind == DISCRETE

    @pytest.mark.slow
    def test_analyze(self):
        p1 = "I feel great this morning."
        n1 = "This is a terrible car."
        p1_result = self.analyzer.analyze(p1)
        assert p1_result[0] == "pos"
        assert self.analyzer.analyze(n1)[0] == "neg"
        # The 2nd item should be the probability that it is positive
        assert isinstance(p1_result[1], float)
        # 3rd item is probability that it is negative
        assert isinstance(p1_result[2], float)
        assert_about_equal(p1_result[1] + p1_result[2], 1)
        assert p1_result.classification == p1_result[0]
        assert p1_result.p_pos == p1_result[1]
        assert p1_result.p_neg == p1_result[2]


def assert_about_equal(first, second, places=4):
    assert round(first, places) == second


if __name__ == "__main__":
    unittest.main()
