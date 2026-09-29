"""Default taggers to the English taggers for backwards incompatibility, so you
can still do

>>> from textblob.taggers import NLTKTagger

which is equivalent to

>>> from textblob.en.taggers import NLTKTagger
"""

from textblob.base import BaseTagger
from textblob.en.taggers import NLTKTagger, PatternTagger

__all__ = [
    "BaseTagger",
    "PatternTagger",
    "NLTKTagger",
]
