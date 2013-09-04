import os
import unittest
from nose.tools import *  # PEP8 asserts
from nose.plugins.attrib import attr

from text.tokenizers import WordTokenizer
from text.classifiers import NaiveBayesClassifier, DecisionTreeClassifier, basic_extractor
from text.compat import unicode

HERE = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(HERE, 'data.csv')
JSON_FILE = os.path.join(HERE, "data.json")
TSV_FILE = os.path.join(HERE, "data.tsv")

train_set =  [
      ('I love this car', 'positive'),
      ('This view is amazing', 'positive'),
      ('I feel great this morning', 'positive'),
      ('I am so excited about the concert', 'positive'),
      ('He is my best friend', 'positive'),
      ('I do not like this car', 'negative'),
      ('This view is horrible', 'negative'),
      ('I feel tired this morning', 'negative'),
      ('I am not looking forward to the concert', 'negative'),
      ('He is my enemy', 'negative')
]

test_set = [('I feel happy this morning', 'positive'),
                ('Larry is my friend.', 'positive'),
                ('I do not like that man.', 'negative'),
                ('My house is not great.', 'negative'),
                ('Your song is annoying.', 'negative')]

class TestNaiveBayesClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = NaiveBayesClassifier(train_set)

    def test_basic_extractor(self):
        text = "I feel happy this morning."
        feats = basic_extractor(text, train_set)
        assert_true(feats["contains(feel)"])
        assert_true(feats['contains(morning)'])
        assert_false(feats["contains(amazing)"])

    def test_default_extractor(self):
        text = "I feel happy this morning."
        assert_equal(self.classifier.extract_features(text), basic_extractor(text, train_set))

    def test_classify(self):
        res = self.classifier.classify("I feel happy this morning")
        assert_equal(res, 'positive')
        assert_equal(len(self.classifier.train_set), len(train_set))

    def test_prob_classify(self):
        res = self.classifier.prob_classify("I feel happy this morning")
        assert_equal(res.max(), "positive")
        assert_true(res.prob("positive") > res.prob("negative"))

    def test_accuracy(self):
        acc = self.classifier.accuracy(test_set)
        assert_true(isinstance(acc, float))

    def test_update(self):
        res1 = self.classifier.prob_classify("lorem ipsum")
        original_length = len(self.classifier.train_set)
        self.classifier.update([("lorem ipsum", "positive")])
        new_length = len(self.classifier.train_set)
        res2 = self.classifier.prob_classify("lorem ipsum")
        assert_true(res2.prob("positive") > res1.prob("positive"))
        assert_equal(original_length + 1, new_length)

    def test_show_informative_features(self):
        feats = self.classifier.show_informative_features()

    def test_informative_features(self):
        feats = self.classifier.informative_features(3)
        assert_true(isinstance(feats, list))
        assert_true(isinstance(feats[0], tuple))

    def test_custom_feature_extractor(self):
        cl = NaiveBayesClassifier(train_set, custom_extractor)
        cl.classify("Yay! I'm so happy it works.")
        assert_equal(cl.train_features[0][1], 'positive')

    def test_init_with_csv_file(self):
        cl = NaiveBayesClassifier(CSV_FILE, format="csv")
        assert_equal(cl.classify("I feel happy this morning"), 'pos')
        training_sentence = cl.train_set[0][0]
        assert_true(isinstance(training_sentence, unicode))

    def test_init_with_csv_file_without_format_specifier(self):
        cl = NaiveBayesClassifier(CSV_FILE)
        assert_equal(cl.classify("I feel happy this morning"), 'pos')
        training_sentence = cl.train_set[0][0]
        assert_true(isinstance(training_sentence, unicode))

    def test_init_with_json_file(self):
        cl = NaiveBayesClassifier(JSON_FILE, format="json")
        assert_equal(cl.classify("I feel happy this morning"), 'pos')
        training_sentence = cl.train_set[0][0]
        assert_true(isinstance(training_sentence, unicode))

    def test_init_with_json_file_without_format_specifier(self):
        cl = NaiveBayesClassifier(JSON_FILE)
        assert_equal(cl.classify("I feel happy this morning"), 'pos')
        training_sentence = cl.train_set[0][0]
        assert_true(isinstance(training_sentence, unicode))

    def test_accuracy_on_a_csv_file(self):
        a = self.classifier.accuracy(CSV_FILE)
        assert_true(isinstance(a, float))

    def test_accuracy_on_json_file(self):
        a = self.classifier.accuracy(JSON_FILE)
        assert_true(isinstance(a, float))

    def test_init_with_tsv_file(self):
        cl = NaiveBayesClassifier(TSV_FILE)
        assert_equal(cl.classify("I feel happy this morning"), 'pos')
        training_sentence = cl.train_set[0][0]
        assert_true(isinstance(training_sentence, unicode))

    @attr("py27_only")
    def test_init_with_bad_format_specifier(self):
        with assert_raises(ValueError):
            NaiveBayesClassifier(CSV_FILE, format='unknown')

class TestDecisionTreeClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = DecisionTreeClassifier(train_set)

    def test_classify(self):
        res = self.classifier.classify("I feel happy this morning")
        assert_equal(res, 'positive')
        assert_equal(len(self.classifier.train_set), len(train_set))

    def test_accuracy(self):
        acc = self.classifier.accuracy(test_set)
        assert_true(isinstance(acc, float))

    def test_update(self):
        original_length = len(self.classifier.train_set)
        self.classifier.update([("lorem ipsum", "positive")])
        new_length = len(self.classifier.train_set)
        assert_equal(original_length + 1, new_length)

    def test_custom_feature_extractor(self):
        cl = DecisionTreeClassifier(train_set, custom_extractor)
        cl.classify("Yay! I'm so happy it works.")
        assert_equal(cl.train_features[0][1], 'positive')

    def test_pseudocode(self):
        code = self.classifier.pseudocode()
        assert_true("if" in code)

    def test_pp(self):
        pp = self.classifier.pprint(width=60)
        assert_true(isinstance(pp, unicode))

def custom_extractor(document):
    feats = {}
    tokens = document.split()
    for tok in tokens:
        feat_name = "last_letter({0})".format(tok[-1])
        feats[feat_name] = True
    return feats

if __name__ == '__main__':
    unittest.main()
