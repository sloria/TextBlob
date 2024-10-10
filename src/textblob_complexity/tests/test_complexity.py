import unittest
import nltk
# from textblob_complexity import TextComplexityScorer
from textblob_complexity.complexity import TextComplexityScorer

# nltk.data.path.append('/Users/rahulkailasa/Documents/GitHub/TextBlob/env/nltk_data/')
nltk.data.path.append('/Users/rahulkailasa/nltk_data')

class TestTextComplexityScorer(unittest.TestCase):
    def setUp(self):
        self.text = "This is a simple sentence. It is easy to understand."
        self.scorer = TextComplexityScorer(self.text)

    def test_flesch_kincaid_grade(self):
        score = self.scorer.flesch_kincaid_grade()
        self.assertTrue(score > 0)

    def test_gunning_fog(self):
        score = self.scorer.gunning_fog()
        self.assertTrue(score > 0)

    def test_smog_index(self):
        score = self.scorer.smog_index()
        self.assertTrue(score > 0)

    def test_ari(self):
        score = self.scorer.ari()
        self.assertTrue(score > 0)

    def test_compute_scores(self):
        scores = self.scorer.compute_scores()
        self.assertTrue("Flesch-Kincaid Grade Level" in scores)

if __name__ == "__main__":
    unittest.main()
