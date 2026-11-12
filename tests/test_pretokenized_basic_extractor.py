import pytest

from textblob.classifiers import basic_extractor


@pytest.mark.parametrize("row_type", [list, iter])
@pytest.mark.parametrize("document_type", [list, tuple, iter])
def test_basic_extractor_accepts_pretokenized_labeled_documents(
    row_type, document_type
):
    data = row_type(
        [
            (document_type(["good", "movie"]), "positive"),
            (document_type(["bad", "movie"]), "negative"),
        ]
    )

    assert basic_extractor(["good", "movie"], data) == {
        "contains(good)": True,
        "contains(movie)": True,
        "contains(bad)": False,
    }


def test_basic_extractor_accepts_an_empty_first_document():
    assert basic_extractor(["good"], [([], "neutral"), (["good"], "positive")]) == {
        "contains(good)": True
    }


@pytest.mark.parametrize("words", [[], ["good", "movie"]])
def test_basic_extractor_preserves_vocabulary_input(words):
    assert basic_extractor(["good"], iter(words)) == {
        f"contains({word})": word == "good" for word in words
    }


@pytest.mark.parametrize("data", [[(5, "positive")], [(None, "positive")]])
def test_basic_extractor_still_rejects_noniterable_documents(data):
    with pytest.raises(ValueError, match="train_set is probably malformed"):
        basic_extractor(["good"], data)
