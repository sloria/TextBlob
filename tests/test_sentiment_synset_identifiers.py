import pytest

from textblob._text import Sentiment


@pytest.mark.parametrize(
    "identifier", ["a-00000001", "n-00000002", "v-00000003", "r-00000004", "c_267"]
)
def test_sentiment_resolves_known_synset_identifiers_on_first_use(tmp_path, identifier):
    path = tmp_path / "sentiment.xml"
    path.write_text(
        '<sentiment language="en">'
        '<word form="bright" pos="JJ" polarity="0.6" subjectivity="0.8" '
        f'wordnet_id="{identifier}" />'
        "</sentiment>"
    )
    sentiment = Sentiment(path=str(path), synset="wordnet_id")

    score = sentiment(identifier)

    assert tuple(score) == (0.6, 0.8)
    assert score.assessments == [([identifier], 0.6, 0.8, None)]


@pytest.mark.parametrize("text", ["c-17", "a-99999999", "ordinary text"])
def test_unknown_synset_shaped_strings_remain_ordinary_text(text):
    sentiment = Sentiment()

    score = sentiment(text)

    assert tuple(score) == (0.0, 0.0)
    assert score.assessments == []


def test_plain_words_still_use_ordinary_assessment():
    sentiment = Sentiment()
    sentiment.annotate("bright", polarity=0.6, subjectivity=0.8)

    assert tuple(sentiment("bright")) == (0.6, 0.8)
