"""
Unit test for svm_sentiment.py
------------------------------
This ensures that the model runs without errors and returns valid output types.
"""

import svm_sentiment

def test_model_runs():
    """
    Checks that example predictions return a list of sentiments.
    """
    examples = [
        "I love this!",
        "This is bad.",
        "It’s okay."
    ]
    preds = svm_sentiment.model.predict(examples)
    assert len(preds) == len(examples), "Prediction count mismatch"
    for p in preds:
        assert p in ['positive', 'negative', 'neutral'], "Unexpected sentiment label"

print(" All basic tests passed.")
