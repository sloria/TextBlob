import pytest

from textblob.classifiers import DecisionTreeClassifier, NaiveBayesClassifier

TRAIN = [
    (["sun", "warm"], "day"),
    (["sun", "bright"], "day"),
    (["rain", "cold"], "night"),
    (["rain", "dark"], "night"),
]
ADDED = [(["snow", "cold"], "night"), (["heat", "bright"], "day")]


def expected_features(data):
    vocabulary = {word for words, _ in data for word in words}
    return [
        ({f"contains({word})": word in words for word in vocabulary}, label)
        for words, label in data
    ]


@pytest.mark.parametrize(
    "classifier_type", [NaiveBayesClassifier, DecisionTreeClassifier]
)
@pytest.mark.parametrize("row_type", [list, iter])
@pytest.mark.parametrize("document_type", [list, iter])
def test_classifier_retains_single_pass_training_rows_and_documents(
    classifier_type, row_type, document_type
):
    data = row_type([(document_type(words), label) for words, label in TRAIN])

    classifier = classifier_type(data)

    assert classifier.train_features == expected_features(TRAIN)
    assert classifier.accuracy(TRAIN) == 1.0
    assert classifier.classify(["sun"]) == "day"
    assert classifier.classify(["rain"]) == "night"
    assert "4 instances" in repr(classifier)


@pytest.mark.parametrize(
    "classifier_type", [NaiveBayesClassifier, DecisionTreeClassifier]
)
@pytest.mark.parametrize("row_type", [list, iter])
@pytest.mark.parametrize("document_type", [list, iter])
def test_classifier_update_retains_new_vocabulary_from_single_pass_data(
    classifier_type, row_type, document_type
):
    classifier = classifier_type([(list(words), label) for words, label in TRAIN])
    classifier.train()
    data = row_type([(document_type(words), label) for words, label in ADDED])

    assert classifier.update(data)

    assert classifier.train_features == expected_features(TRAIN + ADDED)
    reference = classifier_type(TRAIN + ADDED)
    assert classifier.accuracy(TRAIN + ADDED) == reference.accuracy(TRAIN + ADDED)
    for words in (["snow"], ["heat"], ["snow", "cold"], ["heat", "bright"]):
        assert classifier.classify(words) == reference.classify(words)
