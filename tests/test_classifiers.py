# -*- coding: utf-8 -*-
import os
import unittest

import mock
from nose.tools import *  # PEP8 asserts
from nose.plugins.attrib import attr
import nltk

from textblob.tokenizers import WordTokenizer
from textblob.classifiers import (NaiveBayesClassifier, DecisionTreeClassifier,
                              basic_extractor, contains_extractor, NLTKClassifier,
                              PositiveNaiveBayesClassifier, _get_words_from_dataset,
                              MaxEntClassifier)
from textblob import formats
from textblob.compat import unicode
from textblob.exceptions import FormatError

HERE = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(HERE, 'data.csv')
JSON_FILE = os.path.join(HERE, "data.json")
TSV_FILE = os.path.join(HERE, "data.tsv")

train_set = [
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

class BadNLTKClassifier(NLTKClassifier):

    '''An NLTK classifier without ``nltk_class`` defined. Oops!'''
    pass

class TestNLTKClassifier(unittest.TestCase):

    def setUp(self):
        self.bad_classifier = BadNLTKClassifier(train_set)

    def test_raises_value_error_without_nltk_class(self):
        assert_raises(ValueError,
            lambda: self.bad_classifier.classifier)

        assert_raises(ValueError,
            lambda: self.bad_classifier.train(train_set))

        assert_raises(ValueError,
            lambda: self.bad_classifier.update([("This is no good.", 'negative')]))


class TestNaiveBayesClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = NaiveBayesClassifier(train_set)

    def test_default_extractor(self):
        text = "I feel happy this morning."
        assert_equal(self.classifier.extract_features(text), basic_extractor(text, train_set))

    def test_classify(self):
        res = self.classifier.classify("I feel happy this morning")
        assert_equal(res, 'positive')
        assert_equal(len(self.classifier.train_set), len(train_set))

    def test_classify_a_list_of_words(self):
        res = self.classifier.classify(["I", "feel", "happy", "this", "morning"])
        assert_equal(res, "positive")

    def test_train_from_lists_of_words(self):
        # classifier can be trained on lists of words instead of strings
        train = [(doc.split(), label) for doc, label in train_set]
        classifier = NaiveBayesClassifier(train)
        assert_equal(classifier.accuracy(test_set),
                        self.classifier.accuracy(test_set))

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

    def test_labels(self):
        labels = self.classifier.labels()
        assert_true("positive" in labels)
        assert_true("negative" in labels)

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
        with open(CSV_FILE) as fp:
            cl = NaiveBayesClassifier(fp, format="csv")
        assert_equal(cl.classify("I feel happy this morning"), 'pos')
        training_sentence = cl.train_set[0][0]
        assert_true(isinstance(training_sentence, unicode))

    def test_init_with_csv_file_without_format_specifier(self):
        with open(CSV_FILE) as fp:
            cl = NaiveBayesClassifier(fp)
        assert_equal(cl.classify("I feel happy this morning"), 'pos')
        training_sentence = cl.train_set[0][0]
        assert_true(isinstance(training_sentence, unicode))

    def test_init_with_json_file(self):
        with open(JSON_FILE) as fp:
            cl = NaiveBayesClassifier(fp, format="json")
        assert_equal(cl.classify("I feel happy this morning"), 'pos')
        training_sentence = cl.train_set[0][0]
        assert_true(isinstance(training_sentence, unicode))

    def test_init_with_json_file_without_format_specifier(self):
        with open(JSON_FILE) as fp:
            cl = NaiveBayesClassifier(fp)
        assert_equal(cl.classify("I feel happy this morning"), 'pos')
        training_sentence = cl.train_set[0][0]
        assert_true(isinstance(training_sentence, unicode))

    def test_init_with_custom_format(self):
        redis_train = [('I like turtles', 'pos'), ('I hate turtles', 'neg')]

        class MockRedisFormat(formats.BaseFormat):
            def __init__(self, client, port):
                self.client = client
                self.port = port

            @classmethod
            def detect(cls, stream):
                return True

            def to_iterable(self):
                return redis_train

        formats.register('redis', MockRedisFormat)
        mock_redis = mock.Mock()
        cl = NaiveBayesClassifier(mock_redis, format='redis', port=1234)
        assert_equal(cl.train_set, redis_train)

    def test_data_with_no_available_format(self):
        mock_fp = mock.Mock()
        mock_fp.read.return_value = ''

        assert_raises(FormatError, lambda: NaiveBayesClassifier(mock_fp))

    def test_accuracy_on_a_csv_file(self):
        with open(CSV_FILE) as fp:
            a = self.classifier.accuracy(fp)
        assert_equal(type(a), float)

    def test_accuracy_on_json_file(self):
        with open(CSV_FILE) as fp:
            a = self.classifier.accuracy(fp)
        assert_equal(type(a), float)

    def test_init_with_tsv_file(self):
        with open(TSV_FILE) as fp:
            cl = NaiveBayesClassifier(fp)
        assert_equal(cl.classify("I feel happy this morning"), 'pos')
        training_sentence = cl.train_set[0][0]
        assert_true(isinstance(training_sentence, unicode))

    def test_init_with_bad_format_specifier(self):
        assert_raises(ValueError,
            lambda: NaiveBayesClassifier(CSV_FILE, format='unknown'))

    def test_repr(self):
        assert_equal(repr(self.classifier),
            "<NaiveBayesClassifier trained on {0} instances>".format(len(train_set)))


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

    def test_pretty_format(self):
        pp = self.classifier.pprint(width=60)
        pf = self.classifier.pretty_format(width=60)
        assert_true(isinstance(pp, unicode))
        assert_equal(pp, pf)

    def test_repr(self):
        assert_equal(repr(self.classifier),
            "<DecisionTreeClassifier trained on {0} instances>".format(len(train_set)))

@attr('requires_numpy')
@attr('slow')
class TestMaxEntClassifier(unittest.TestCase):

    def setUp(self):
        self.classifier = MaxEntClassifier(train_set)

    def test_classify(self):
        res = self.classifier.classify("I feel happy this morning")
        assert_equal(res, 'positive')
        assert_equal(len(self.classifier.train_set), len(train_set))

    def test_prob_classify(self):
        res = self.classifier.prob_classify("I feel happy this morning")
        assert_equal(res.max(), 'positive')
        assert_true(res.prob("positive") > res.prob("negative"))



class TestPositiveNaiveBayesClassifier(unittest.TestCase):

    def setUp(self):
        sports_sentences = ['The team dominated the game',
                          'They lost the ball',
                          'The game was intense',
                          'The goalkeeper catched the ball',
                          'The other team controlled the ball'
                            'The ball went off the court',
                           'They had the ball for the whole game']

        various_sentences = ['The President did not comment',
                               'I lost the keys',
                               'The team won the game',
                               'Sara has two kids',
                               'The show is over',
                               'The cat ate the mouse.']

        self.classifier = PositiveNaiveBayesClassifier(positive_set=sports_sentences,
                                                        unlabeled_set=various_sentences)

    def test_classifier(self):
        assert_true(isinstance(self.classifier.classifier,
                               nltk.classify.PositiveNaiveBayesClassifier))


    def test_classify(self):
        assert_true(self.classifier.classify("My team lost the game."))
        assert_false(self.classifier.classify("The cat is on the table."))

    def test_update(self):
        orig_pos_length = len(self.classifier.positive_set)
        orig_unlabeled_length = len(self.classifier.unlabeled_set)
        self.classifier.update(new_positive_data=['He threw the ball to the base.'],
                                new_unlabeled_data=["I passed a tree today."])
        new_pos_length = len(self.classifier.positive_set)
        new_unlabeled_length = len(self.classifier.unlabeled_set)
        assert_equal(new_pos_length, orig_pos_length + 1)
        assert_equal(new_unlabeled_length, orig_unlabeled_length + 1)

    def test_accuracy(self):
        test_set = [
            ("My team lost the game", True),
            ("The ball was in the court.", True),
            ("We should have won the game.", True),
            ("And now for something completely different", False),
            ("I can't believe it's not butter.", False)
        ]
        accuracy = self.classifier.accuracy(test_set)
        assert_true(isinstance(accuracy, float))

    def test_repr(self):
        assert_equal(repr(self.classifier),
            "<PositiveNaiveBayesClassifier trained on {0} labeled and {1} unlabeled instances>"
                .format(len(self.classifier.positive_set),
                        len(self.classifier.unlabeled_set))
                     )


def test_basic_extractor():
    text = "I feel happy this morning."
    feats = basic_extractor(text, train_set)
    assert_true(feats["contains(feel)"])
    assert_true(feats['contains(morning)'])
    assert_false(feats["contains(amazing)"])

def test_basic_extractor_with_list():
    text = "I feel happy this morning.".split()
    feats = basic_extractor(text, train_set)
    assert_true(feats["contains(feel)"])
    assert_true(feats['contains(morning)'])
    assert_false(feats["contains(amazing)"])

def test_contains_extractor_with_string():
    text = "Simple is better than complex"
    features = contains_extractor(text)
    assert_true(features["contains(Simple)"])
    assert_false(features.get('contains(simple)', False))
    assert_true(features['contains(complex)'])
    assert_false(features.get("contains(derp)", False))

def test_contains_extractor_with_list():
    text = ["Simple", "is", "better", "than", "complex"]
    features = contains_extractor(text)
    assert_true(features['contains(Simple)'])
    assert_false(features.get("contains(simple)", False))
    assert_true(features['contains(complex)'])
    assert_false(features.get("contains(derp)", False))

def custom_extractor(document):
    feats = {}
    tokens = document.split()
    for tok in tokens:
        feat_name = "last_letter({0})".format(tok[-1])
        feats[feat_name] = True
    return feats

def test_get_words_from_dataset():
    tok = WordTokenizer()
    all_words = []
    for words, _ in train_set:
        all_words.extend(tok.itokenize(words, include_punc=False))
    assert_equal(_get_words_from_dataset(train_set), set(all_words))


if __name__ == '__main__':
    unittest.main()
