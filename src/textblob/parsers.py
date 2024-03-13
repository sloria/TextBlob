"""Default parsers to English for backwards compatibility so you can still do

>>> from textblob.parsers import PatternParser

which is equivalent to

>>> from textblob.en.parsers import PatternParser
"""

from textblob.base import BaseParser
from textblob.en.parsers import PatternParser

__all__ = [
    "BaseParser",
    "PatternParser",
]
