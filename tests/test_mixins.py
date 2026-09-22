import pytest

from textblob import Sentence, TextBlob, Word


@pytest.mark.parametrize("blob_type", [TextBlob, Sentence])
@pytest.mark.parametrize(
    "iterable_type",
    [
        list,
        iter,
        pytest.param(lambda values: (item for item in values), id="generator"),
    ],
)
def test_join_accepts_strings_and_blobs(blob_type, iterable_type):
    values = [Word("one"), TextBlob("two"), Sentence("three"), "four"]
    result = blob_type(" / ").join(iterable_type(values))

    assert type(result) is blob_type
    assert str(result) == "one / two / three / four"


@pytest.mark.parametrize("blob_type", [TextBlob, Sentence])
def test_join_empty_iterable(blob_type):
    result = blob_type(" / ").join(iter([]))

    assert type(result) is blob_type
    assert str(result) == ""


@pytest.mark.parametrize("blob_type", [TextBlob, Sentence])
@pytest.mark.parametrize("value", [None, 1, b"bytes", object()])
def test_join_rejects_unsupported_items(blob_type, value):
    with pytest.raises(TypeError):
        blob_type(" / ").join(["one", value])
