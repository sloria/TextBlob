import pytest

from textblob import Word, WordList


@pytest.mark.parametrize("values", [[], ["cats"], ["cats", "dogs"], ["cats", 4]])
def test_extend_self(monkeypatch, values):
    words = WordList([])
    words.extend(values)
    expected = list(words) * 2
    append = words.append

    def bounded_append(value):
        # Fail promptly instead of allowing a regression to exhaust memory.
        assert len(words) < len(expected)
        append(value)

    monkeypatch.setattr(words, "append", bounded_append)
    assert words.extend(words) is None
    assert words == expected
    assert [type(word) for word in words] == [type(word) for word in expected]


@pytest.mark.parametrize("iterable_type", [list, tuple, iter])
def test_extend_other_iterables(iterable_type):
    words = WordList(["cats"])
    assert words.extend(iterable_type(["dogs", 4])) is None
    assert words == ["cats", "dogs", 4]
    assert isinstance(words[1], Word)
    assert isinstance(words[2], int)


def test_extend_preserves_items_before_iterator_error():
    def values():
        yield "dogs"
        raise ValueError("cannot read another word")

    words = WordList(["cats"])
    with pytest.raises(ValueError, match="cannot read another word"):
        words.extend(values())
    assert words == ["cats", "dogs"]
    assert isinstance(words[1], Word)
