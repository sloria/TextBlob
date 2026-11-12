import nltk
import pytest

from textblob.classifiers import PositiveNaiveBayesClassifier, contains_extractor


@pytest.mark.parametrize("prior", [0.2, 0.8])
@pytest.mark.parametrize("update_kind", ["positive", "unlabeled", "both", "neither"])
def test_update_preserves_the_prior_and_matches_fresh_training(prior, update_kind):
    positive = [["ball"], ["goal"]]
    unlabeled = [["ball"], ["news"], ["weather"], ["music"]]
    new_positive = [["team"]] if update_kind in {"positive", "both"} else []
    new_unlabeled = [["team"], ["news"]] if update_kind in {"unlabeled", "both"} else []
    expected = nltk.classify.PositiveNaiveBayesClassifier.train(
        [contains_extractor(document) for document in positive + new_positive],
        [contains_extractor(document) for document in unlabeled + new_unlabeled],
        positive_prob_prior=prior,
    )
    classifier = PositiveNaiveBayesClassifier(
        positive, unlabeled, positive_prob_prior=prior
    )
    # Exercise updating an already trained model, as in incremental use.
    classifier.classify(["ball"])

    assert classifier.update(new_positive, new_unlabeled)

    assert classifier.positive_prob_prior == prior
    assert classifier.classifier.prob_classify({}).prob(True) == pytest.approx(prior)
    for document in [["ball"], ["team"], ["news"], ["unknown"], []]:
        features = contains_extractor(document)
        actual = classifier.classifier.prob_classify(features)
        assert actual.prob(True) == pytest.approx(
            expected.prob_classify(features).prob(True)
        )


def test_update_explicitly_changes_the_prior_and_keeps_it_for_later_updates():
    classifier = PositiveNaiveBayesClassifier(
        [["ball"]], [["ball"], ["news"]], positive_prob_prior=0.2
    )

    classifier.update(positive_prob_prior=0.7)
    assert classifier.positive_prob_prior == 0.7
    assert classifier.classifier.prob_classify({}).prob(True) == pytest.approx(0.7)

    classifier.update(new_unlabeled_data=[["weather"]])
    assert classifier.positive_prob_prior == 0.7
    assert classifier.classifier.prob_classify({}).prob(True) == pytest.approx(0.7)


def test_update_preserves_the_default_prior():
    classifier = PositiveNaiveBayesClassifier([["ball"]], [["ball"], ["news"]])

    classifier.update(new_positive_data=[["goal"]])

    assert classifier.positive_prob_prior == 0.5
    assert classifier.classifier.prob_classify({}).prob(True) == pytest.approx(0.5)
