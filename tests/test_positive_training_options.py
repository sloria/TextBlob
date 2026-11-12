from functools import partial

import nltk
import pytest
from nltk.probability import ELEProbDist, LidstoneProbDist

from textblob.classifiers import PositiveNaiveBayesClassifier, contains_extractor

POSITIVE = [["sun", "warm"], ["sun", "bright"], ["sun"]]
UNLABELED = [["rain", "cold"], ["rain", "dark"], ["sun", "rain"], ["cold"]]


@pytest.mark.parametrize("prior", [0.2, 0.5])
@pytest.mark.parametrize("gamma", [0.1, 0.5, 2.0])
@pytest.mark.parametrize("positional", [False, True])
def test_positive_training_forwards_probability_estimator(prior, gamma, positional):
    estimator = partial(LidstoneProbDist, gamma=gamma)
    classifier = PositiveNaiveBayesClassifier(
        POSITIVE, UNLABELED, positive_prob_prior=prior
    )
    expected = nltk.classify.PositiveNaiveBayesClassifier.train(
        [contains_extractor(words) for words in POSITIVE],
        [contains_extractor(words) for words in UNLABELED],
        positive_prob_prior=prior,
        estimator=estimator,
    )

    actual = (
        classifier.train(estimator)
        if positional
        else classifier.train(estimator=estimator)
    )

    assert actual is classifier.classifier
    for words in (["sun"], ["rain"], ["warm", "cold"], []):
        features = contains_extractor(words)
        for label in (False, True):
            assert actual.prob_classify(features).prob(label) == pytest.approx(
                expected.prob_classify(features).prob(label)
            )


def test_default_training_estimator_remains_ele():
    classifier = PositiveNaiveBayesClassifier(POSITIVE, UNLABELED)
    default = classifier.train()
    explicit = classifier.train(estimator=ELEProbDist)

    for words in (["sun"], ["rain"]):
        features = contains_extractor(words)
        assert default.prob_classify(features).prob(True) == explicit.prob_classify(
            features
        ).prob(True)
