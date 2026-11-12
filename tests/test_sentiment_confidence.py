import pytest

from textblob._text import Sentiment

LEXICON = """<sentiment language="en">
<word form="bright" pos="JJ" polarity="-0.8" subjectivity="0.2"
      confidence="0.2" wordnet_id="a-00000001" />
<word form="bright" pos="JJ" polarity="0.6" subjectivity="0.8"
      confidence="0.8" wordnet_id="a-00000002" />
<word form="unrated" pos="JJ" polarity="0.4" subjectivity="0.4"
      wordnet_id="a-00000003" label="test" />
</sentiment>"""


@pytest.mark.parametrize(
    "confidence, expected, words",
    [
        (None, (-0.1, 0.5), {"bright", "unrated"}),
        (0.0, (-0.1, 0.5), {"bright", "unrated"}),
        (0.5, (0.6, 0.8), {"bright"}),
        (0.8, (0.6, 0.8), {"bright"}),
        (1.0, (0.0, 0.0), set()),
    ],
)
def test_confidence_threshold_filters_senses_before_averaging(
    tmp_path, confidence, expected, words
):
    path = tmp_path / "sentiment.xml"
    path.write_text(LEXICON)
    sentiment = Sentiment(path=str(path), confidence=confidence, synset="wordnet_id")

    assert tuple(sentiment("bright")) == pytest.approx(expected)
    assert set(sentiment) == words
    assert sentiment.confidence == confidence
    assert ("unrated" in sentiment.labeler) == ("unrated" in words)
    low_confidence = confidence is None or confidence <= 0.2
    assert sentiment.synset(1) == pytest.approx(
        (-0.8, 0.2) if low_confidence else (0.0, 0.0)
    )


def test_explicit_load_uses_the_configured_confidence_threshold(tmp_path):
    path = tmp_path / "sentiment.xml"
    path.write_text(LEXICON)
    sentiment = Sentiment(confidence=0.8)

    sentiment.load(str(path))

    assert tuple(sentiment("bright")) == pytest.approx((0.6, 0.8))
    assert "unrated" not in sentiment
