import pytest

from textblob._text import Sentiment
from textblob.en import sentiment


@pytest.mark.parametrize(
    "tokens",
    [
        ["GOOD"],
        ["Very", "GOOD"],
        ["NOT", "good"],
        ["not", "HORRIBLE"],
        ["VERY", "bad", "!"],
        [":D"],
        ["good"],
        [],
    ],
)
def test_pretokenized_sentiment_matches_string_case_normalization(tokens):
    expected = sentiment(" ".join(tokens))

    actual = sentiment(tokens)

    assert tuple(actual) == pytest.approx(tuple(expected))
    assert actual.assessments == expected.assessments


def test_pretokenized_unicode_words_use_the_same_lowercasing_as_strings():
    lexicon = Sentiment()
    lexicon.annotate("café", polarity=0.5, subjectivity=0.75)

    score = lexicon(["CAFÉ"])

    assert tuple(score) == (0.5, 0.75)
    assert score.assessments == [(["café"], 0.5, 0.75, None)]
