"""Default sentiment analyzers are English for backwards compatibility, so
you can still do

>>> from textblob.sentiments import PatternAnalyzer

which is equivalent to

>>> from textblob.en.sentiments import PatternAnalyzer
"""
from textblob.base import BaseSentimentAnalyzer
from textblob.en.sentiments import (
    CONTINUOUS,
    DISCRETE,
    NaiveBayesAnalyzer,
    PatternAnalyzer,
)

__all__ = [
    "BaseSentimentAnalyzer",
    "DISCRETE",
    "CONTINUOUS",
    "PatternAnalyzer",
    "NaiveBayesAnalyzer",
]
