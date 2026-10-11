import pytest

from textblob import Word, WordList


@pytest.mark.parametrize("index", [-100, -1, 0, 1, 100])
def test_insert_preserves_word_operations(index):
    words = WordList(["cats", "dogs"])
    expected = ["cats", "dogs"]
    expected.insert(index, "wolves")

    assert words.insert(index, "wolves") is None

    assert words == expected
    assert all(isinstance(word, Word) for word in words)
    assert words.singularize() == WordList(expected).singularize()


@pytest.mark.parametrize("iterable", [list, tuple, iter])
@pytest.mark.parametrize(
    ("index", "replacement"),
    [
        (slice(1, 2), ["cats", "wolves"]),
        (slice(None, None, 2), ["cats", "wolves"]),
        (slice(None, None, -2), ["cats", "wolves"]),
        (slice(1, 1), ["cats"]),
        (slice(None), []),
    ],
)
def test_slice_assignment_preserves_word_operations(iterable, index, replacement):
    words = WordList(["dogs", "mice", "geese", "horses"])
    expected = list(words)
    expected[index] = replacement

    words[index] = iterable(replacement)

    assert words == expected
    assert all(isinstance(word, Word) for word in words)
    assert words.singularize() == WordList(expected).singularize()


def test_slice_assignment_from_string():
    words = WordList(["cats", "dogs"])
    words[1:] = "ox"
    assert words == ["cats", "o", "x"]
    assert all(isinstance(word, Word) for word in words)


def test_edits_preserve_non_string_objects():
    value = object()
    words = WordList([])
    words.insert(0, value)
    assert words[0] is value
    words[:] = [value, 42]
    assert words[0] is value
    assert words[1] == 42


def test_edits_preserve_existing_words_and_tags():
    tagged = Word("cats", pos_tag="NNS")
    words = WordList([])
    words.insert(0, tagged)
    assert words[0] is tagged
    words[:] = [tagged]
    assert words[0] is tagged
    assert words[0].pos_tag == "NNS"


def test_failed_slice_assignment_does_not_modify_words():
    words = WordList(["cats", "dogs"])

    def failing_iterable():
        yield "wolves"
        raise RuntimeError("unavailable replacement")

    with pytest.raises(RuntimeError, match="unavailable replacement"):
        words[:] = failing_iterable()
    assert words == ["cats", "dogs"]

    with pytest.raises(ValueError, match="extended slice"):
        words[::2] = ["wolves", "geese"]
    assert words == ["cats", "dogs"]
