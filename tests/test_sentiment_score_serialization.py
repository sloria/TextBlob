import copy
import pickle

import pytest

from textblob._text import Score
from textblob.en import sentiment


@pytest.mark.parametrize("protocol", range(pickle.HIGHEST_PROTOCOL + 1))
@pytest.mark.parametrize("text", ["not very good!", "unknownword"])
def test_sentiment_scores_roundtrip_through_pickle(text, protocol):
    score = sentiment(text)

    restored = pickle.loads(pickle.dumps(score, protocol=protocol))

    assert type(restored) is Score
    assert tuple(restored) == tuple(score)
    assert restored.assessments == score.assessments


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy])
def test_sentiment_scores_support_copy(copier):
    score = sentiment("very good")

    restored = copier(score)

    assert type(restored) is Score
    assert tuple(restored) == tuple(score)
    assert restored.assessments == score.assessments
    if copier is copy.deepcopy:
        restored.assessments[0][0].append("changed")
        assert "changed" not in score.assessments[0][0]
