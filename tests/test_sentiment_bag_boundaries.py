import pytest

from textblob._text import Sentiment
from textblob.en import sentiment as english_sentiment


class TermDocument:
    def __init__(self, terms):
        self.terms = terms

    def __iter__(self):
        return iter(self.terms)


def make_sentiment():
    sentiment = Sentiment()
    sentiment.annotate("good", pos="JJ", polarity=0.8, subjectivity=0.6)
    sentiment.annotate("bad", pos="JJ", polarity=-0.6, subjectivity=0.7)
    sentiment.annotate("very", pos="RB", polarity=0.2, subjectivity=0.4, intensity=2.0)
    return sentiment


@pytest.mark.parametrize("document_type", [dict, TermDocument])
@pytest.mark.parametrize(
    "words",
    [
        ["not", "good", "very", "bad"],
        ["very", "good", "bad", "not"],
        ["good", "bad", "not", "very"],
        ["bad", "very", "not", "good"],
    ],
)
def test_unordered_terms_keep_independent_sentiment_and_weights(document_type, words):
    weights = {"not": 1, "good": 2, "very": 3, "bad": 4}
    terms = document_type({word: weights[word] for word in words})

    score = make_sentiment()(terms)

    assert tuple(score) == pytest.approx(
        ((2 * 0.8 + 3 * 0.2 - 4 * 0.6) / 9, (2 * 0.6 + 3 * 0.4 + 4 * 0.7) / 9)
    )
    assert sorted(chunk for chunk, *_ in score.assessments) == [
        ["bad"],
        ["good"],
        ["very"],
    ]


@pytest.mark.parametrize(
    "words, expected", [(["not", "good"], -0.4), (["very", "good"], 1.0)]
)
def test_ordered_word_sequences_still_apply_negation_and_modifiers(words, expected):
    assert make_sentiment()(words)[0] == pytest.approx(expected)


def test_bundled_english_lexicon_is_independent_of_term_order():
    assert tuple(english_sentiment({"not": 1, "good": 1})) == pytest.approx(
        tuple(english_sentiment({"good": 1, "not": 1}))
    )
