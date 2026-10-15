import pytest

from textblob import TextBlob


@pytest.mark.parametrize(
    ("sentence", "separator", "count"),
    [
        ("Yes.", " ", 7),
        ("Hello.", "          ", 3),
        ("Hi!", "\t", 5),
        ("Why?", "\n\n", 4),
        ("Café.", "\r\n", 5),
        ("Hello.", " ", 2),
        ("Done.", "", 1),
    ],
)
def test_repeated_sentence_offsets(sentence, separator, count):
    text = separator.join([sentence] * count)
    blob = TextBlob(text)
    expected = [
        (i * (len(sentence) + len(separator)), len(sentence)) for i in range(count)
    ]

    sentences = blob.sentences
    assert isinstance(sentences, list)
    assert len(sentences) == count
    for result, (start, length) in zip(sentences, expected, strict=True):
        assert result.raw == sentence
        assert result.start_index == start
        assert result.end_index == start + length
        assert text[result.start : result.end] == sentence

    assert [item["start_index"] for item in blob.serialized] == [
        start for start, _ in expected
    ]


def test_empty_blob_has_no_sentence_offsets():
    assert TextBlob("").sentences == []
