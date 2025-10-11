"""
test_svm_sentiment.py
unit tests for SVMSentimentClassifier.
"""

import pytest
from svm_sentiment import SVMSentimentClassifier

@pytest.fixture
def trained_classifier():
    texts = [
        "I love this movie!", "That was terrible.", "It's okay, not bad",
        "Absolutely amazing", "Worst thing ever.", "Fine but forgettable."
    ]
    labels = ["positive", "negative", "neutral", "positive", "negative", "neutral"]

    clf = SVMSentimentClassifier()
    clf.train(texts, labels)
    return clf

def test_positive_sentiment(trained_classifier):
    result = trained_classifier.predict("This is fantastic!")
    assert result in ["positive", "negative", "neutral"]

def test_negative_sentiment(trained_classifier):
    result = trained_classifier.predict("I really hated it")
    assert result in ["positive", "negative", "neutral"]

def test_neutral_sentiment(trained_classifier):
    result = trained_classifier.predict("It was fine, nothing special.")
    assert result in ["positive", "negative", "neutral"]   

def test_model_training_required():
    clf = SVMSentimentClassifier()
    with pytest.raises(Exception):
        clf.predict("I love it!")
        
         