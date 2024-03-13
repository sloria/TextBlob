import os
import unittest
from unittest import mock

import nltk
import pytest

from textblob import formats
from textblob.classifiers import (
    DecisionTreeClassifier,
    MaxEntClassifier,
    NaiveBayesClassifier,
    NLTKClassifier,
    PositiveNaiveBayesClassifier,
    _get_words_from_dataset,
    basic_extractor,
    contains_extractor,
)
from textblob.exceptions import FormatError
from textblob.tokenizers import WordTokenizer

HERE = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(HERE, "data.csv")
JSON_FILE = os.path.join(HERE, "data.json")
TSV_FILE = os.path.join(HERE, "data.tsv")

train_set = [
    ("I love this car", "positive"),
    ("This view is amazing", "positive"),
    ("I feel great this morning", "positive"),
    ("I am so excited about the concert", "positive"),
    ("He is my best friend", "positive"),
    ("I do not like this car", "negative"),
    ("This view is horrible", "negative"),
    ("I feel tired this morning", "negative"),
    ("I am not looking forward to the concert", "negative"),
    ("He is my enemy", "negative"),
]

test_set = [
    ("I feel happy this morning", "positive"),
    ("Larry is my friend.", "positive"),
    ("I do not like that man.", "negative"),
    ("My house is not great.", "negative"),
    ("Your song is annoying.", "negative"),
]


class BadNLTKClassifier(NLTKClassifier):
    """An NLTK classifier without ``nltk_class`` defined. Oops!"""

    pass


class TestNLTKClassifier(unittest.TestCase):
    def setUp(self):
        self.bad_classifier = BadNLTKClassifier(train_set)

    def test_raises_value_error_without_nltk_class(self):
        with pytest.raises(ValueError):
            self.bad_classifier.classifier  # noqa: B018

        with pytest.raises(ValueError):
            self.bad_classifier.train(train_set)

        with pytest.raises(ValueError):
            self.bad_classifier.update([("This is no good.", "negative")])


class TestNaiveBayesClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = NaiveBayesClassifier(train_set)

    def test_default_extractor(self):
        text = "I feel happy this morning."
        assert self.classifier.extract_features(text) == basic_extractor(
            text, train_set
        )

    def test_classify(self):
        res = self.classifier.classify("I feel happy this morning")
        assert res == "positive"
        assert len(self.classifier.train_set) == len(train_set)

    def test_classify_a_list_of_words(self):
        res = self.classifier.classify(["I", "feel", "happy", "this", "morning"])
        assert res == "positive"

    def test_train_from_lists_of_words(self):
        # classifier can be trained on lists of words instead of strings
        train = [(doc.split(), label) for doc, label in train_set]
        classifier = NaiveBayesClassifier(train)
        assert classifier.accuracy(test_set) == self.classifier.accuracy(test_set)

    def test_prob_classify(self):
        res = self.classifier.prob_classify("I feel happy this morning")
        assert res.max() == "positive"
        assert res.prob("positive") > res.prob("negative")

    def test_accuracy(self):
        acc = self.classifier.accuracy(test_set)
        assert isinstance(acc, float)

    def test_update(self):
        res1 = self.classifier.prob_classify("lorem ipsum")
        original_length = len(self.classifier.train_set)
        self.classifier.update([("lorem ipsum", "positive")])
        new_length = len(self.classifier.train_set)
        res2 = self.classifier.prob_classify("lorem ipsum")
        assert res2.prob("positive") > res1.prob("positive")
        assert original_length + 1 == new_length

    def test_labels(self):
        labels = self.classifier.labels()
        assert "positive" in labels
        assert "negative" in labels

    def test_show_informative_features(self):
        self.classifier.show_informative_features()

    def test_informative_features(self):
        feats = self.classifier.informative_features(3)
        assert isinstance(feats, list)
        assert isinstance(feats[0], tuple)

    def test_custom_feature_extractor(self):
        cl = NaiveBayesClassifier(train_set, custom_extractor)
        cl.classify("Yay! I'm so happy it works.")
        assert cl.train_features[0][1] == "positive"

    def test_init_with_csv_file(self):
        with open(CSV_FILE) as fp:
            cl = NaiveBayesClassifier(fp, format="csv")
        assert cl.classify("I feel happy this morning") == "pos"
        training_sentence = cl.train_set[0][0]
        assert isinstance(training_sentence, str)

    def test_init_with_csv_file_without_format_specifier(self):
        with open(CSV_FILE) as fp:
            cl = NaiveBayesClassifier(fp)
        assert cl.classify("I feel happy this morning") == "pos"
        training_sentence = cl.train_set[0][0]
        assert isinstance(training_sentence, str)

    def test_init_with_json_file(self):
        with open(JSON_FILE) as fp:
            cl = NaiveBayesClassifier(fp, format="json")
        assert cl.classify("I feel happy this morning") == "pos"
        training_sentence = cl.train_set[0][0]
        assert isinstance(training_sentence, str)

    def test_init_with_json_file_without_format_specifier(self):
        with open(JSON_FILE) as fp:
            cl = NaiveBayesClassifier(fp)
        assert cl.classify("I feel happy this morning") == "pos"
        training_sentence = cl.train_set[0][0]
        assert isinstance(training_sentence, str)

    def test_init_with_custom_format(self):
        redis_train = [("I like turtles", "pos"), ("I hate turtles", "neg")]

        class MockRedisFormat(formats.BaseFormat):
            def __init__(self, client, port):
                self.client = client
                self.port = port

            @classmethod
            def detect(cls, stream):
                return True

            def to_iterable(self):
                return redis_train

        formats.register("redis", MockRedisFormat)
        mock_redis = mock.Mock()
        cl = NaiveBayesClassifier(mock_redis, format="redis", port=1234)
        assert cl.train_set == redis_train

    def test_data_with_no_available_format(self):
        mock_fp = mock.Mock()
        mock_fp.read.return_value = ""

        with pytest.raises(FormatError):
            NaiveBayesClassifier(mock_fp)

    def test_accuracy_on_a_csv_file(self):
        with open(CSV_FILE) as fp:
            a = self.classifier.accuracy(fp)
        assert type(a) == float

    def test_accuracy_on_json_file(self):
        with open(CSV_FILE) as fp:
            a = self.classifier.accuracy(fp)
        assert type(a) == float

    def test_init_with_tsv_file(self):
        with open(TSV_FILE) as fp:
            cl = NaiveBayesClassifier(fp)
        assert cl.classify("I feel happy this morning") == "pos"
        training_sentence = cl.train_set[0][0]
        assert isinstance(training_sentence, str)

    def test_init_with_bad_format_specifier(self):
        with pytest.raises(ValueError):
            NaiveBayesClassifier(CSV_FILE, format="unknown")

    def test_repr(self):
        assert (
            repr(self.classifier)
            == f"<NaiveBayesClassifier trained on {len(train_set)} instances>"
        )


class TestDecisionTreeClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = DecisionTreeClassifier(train_set)

    def test_classify(self):
        res = self.classifier.classify("I feel happy this morning")
        assert res == "positive"
        assert len(self.classifier.train_set) == len(train_set)

    def test_accuracy(self):
        acc = self.classifier.accuracy(test_set)
        assert isinstance(acc, float)

    def test_update(self):
        original_length = len(self.classifier.train_set)
        self.classifier.update([("lorem ipsum", "positive")])
        new_length = len(self.classifier.train_set)
        assert original_length + 1 == new_length

    def test_custom_feature_extractor(self):
        cl = DecisionTreeClassifier(train_set, custom_extractor)
        cl.classify("Yay! I'm so happy it works.")
        assert cl.train_features[0][1] == "positive"

    def test_pseudocode(self):
        code = self.classifier.pseudocode()
        assert "if" in code

    def test_pretty_format(self):
        pp = self.classifier.pprint(width=60)
        pf = self.classifier.pretty_format(width=60)
        assert isinstance(pp, str)
        assert pp == pf

    def test_repr(self):
        assert (
            repr(self.classifier)
            == f"<DecisionTreeClassifier trained on {len(train_set)} instances>"
        )


@pytest.mark.numpy
@pytest.mark.slow
class TestMaxEntClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = MaxEntClassifier(train_set)

    def test_classify(self):
        res = self.classifier.classify("I feel happy this morning")
        assert res == "positive"
        assert len(self.classifier.train_set) == len(train_set)

    def test_prob_classify(self):
        res = self.classifier.prob_classify("I feel happy this morning")
        assert res.max() == "positive"
        assert res.prob("positive") > res.prob("negative")


class TestPositiveNaiveBayesClassifier(unittest.TestCase):
    def setUp(self):
        sports_sentences = [
            "The team dominated the game",
            "They lost the ball",
            "The game was intense",
            "The goalkeeper catched the ball",
            "The other team controlled the ball" "The ball went off the court",
            "They had the ball for the whole game",
        ]

        various_sentences = [
            "The President did not comment",
            "I lost the keys",
            "The team won the game",
            "Sara has two kids",
            "The show is over",
            "The cat ate the mouse.",
        ]

        self.classifier = PositiveNaiveBayesClassifier(
            positive_set=sports_sentences, unlabeled_set=various_sentences
        )

    def test_classifier(self):
        assert isinstance(
            self.classifier.classifier, nltk.classify.PositiveNaiveBayesClassifier
        )

    def test_classify(self):
        assert self.classifier.classify("My team lost the game.")
        assert not self.classifier.classify("The cat is on the table.")

    def test_update(self):
        orig_pos_length = len(self.classifier.positive_set)
        orig_unlabeled_length = len(self.classifier.unlabeled_set)
        self.classifier.update(
            new_positive_data=["He threw the ball to the base."],
            new_unlabeled_data=["I passed a tree today."],
        )
        new_pos_length = len(self.classifier.positive_set)
        new_unlabeled_length = len(self.classifier.unlabeled_set)
        assert new_pos_length == orig_pos_length + 1
        assert new_unlabeled_length == orig_unlabeled_length + 1

    def test_accuracy(self):
        test_set = [
            ("My team lost the game", True),
            ("The ball was in the court.", True),
            ("We should have won the game.", True),
            ("And now for something completely different", False),
            ("I can't believe it's not butter.", False),
        ]
        accuracy = self.classifier.accuracy(test_set)
        assert isinstance(accuracy, float)

    def test_repr(self):
        assert (
            repr(self.classifier)
            == f"<PositiveNaiveBayesClassifier trained on {len(self.classifier.positive_set)} labeled and {len(self.classifier.unlabeled_set)} unlabeled instances>"  # noqa: E501
        )


def test_basic_extractor():
    text = "I feel happy this morning."
    feats = basic_extractor(text, train_set)
    assert feats["contains(feel)"]
    assert feats["contains(morning)"]
    assert not feats["contains(amazing)"]


def test_basic_extractor_with_list():
    text = "I feel happy this morning.".split()
    feats = basic_extractor(text, train_set)
    assert feats["contains(feel)"]
    assert feats["contains(morning)"]
    assert not feats["contains(amazing)"]


def test_contains_extractor_with_string():
    text = "Simple is better than complex"
    features = contains_extractor(text)
    assert features["contains(Simple)"]
    assert not features.get("contains(simple)", False)
    assert features["contains(complex)"]
    assert not features.get("contains(derp)", False)


def test_contains_extractor_with_list():
    text = ["Simple", "is", "better", "than", "complex"]
    features = contains_extractor(text)
    assert features["contains(Simple)"]
    assert not features.get("contains(simple)", False)
    assert features["contains(complex)"]
    assert not features.get("contains(derp)", False)


def custom_extractor(document):
    feats = {}
    tokens = document.split()
    for tok in tokens:
        feat_name = f"last_letter({tok[-1]})"
        feats[feat_name] = True
    return feats


def test_get_words_from_dataset():
    tok = WordTokenizer()
    all_words = []
    for words, _ in train_set:
        all_words.extend(tok.itokenize(words, include_punc=False))
    assert _get_words_from_dataset(train_set) == set(all_words)


if __name__ == "__main__":
    unittest.main()
