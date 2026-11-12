import pytest

from textblob.en import sentiments


@pytest.mark.parametrize("keep_assessments", [False, True])
@pytest.mark.parametrize(
    "text", ["Very good, but not perfect!", "A terrible outcome.", "", "CAFÉ :D"]
)
def test_pattern_analyzer_evaluates_the_lexicon_once(
    monkeypatch, text, keep_assessments
):
    analyze = sentiments.pattern_sentiment
    expected = analyze(text)
    calls = []

    def track_analysis(value):
        calls.append(value)
        return analyze(value)

    monkeypatch.setattr(sentiments, "pattern_sentiment", track_analysis)

    result = sentiments.PatternAnalyzer().analyze(
        text, keep_assessments=keep_assessments
    )

    assert calls == [text]
    assert (result.polarity, result.subjectivity) == pytest.approx(tuple(expected))
    if keep_assessments:
        assert result.assessments == expected.assessments
