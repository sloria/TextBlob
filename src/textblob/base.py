"""Abstract base classes for models (taggers, noun phrase extractors, etc.)
which define the interface for descendant classes.

.. versionchanged:: 0.7.0
    All base classes are defined in the same module, ``textblob.base``.
"""

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import TYPE_CHECKING

import nltk

if TYPE_CHECKING:
    from typing import Any, AnyStr

##### POS TAGGERS #####


class BaseTagger(metaclass=ABCMeta):
    """Abstract tagger class from which all taggers
    inherit from. All descendants must implement a
    ``tag()`` method.
    """

    @abstractmethod
    def tag(self, text: str, tokenize=True) -> list[tuple[str, str]]:
        """Return a list of tuples of the form (word, tag)
        for a given set of text or BaseBlob instance.
        """
        ...


##### NOUN PHRASE EXTRACTORS #####


class BaseNPExtractor(metaclass=ABCMeta):
    """Abstract base class from which all NPExtractor classes inherit.
    Descendant classes must implement an ``extract(text)`` method
    that returns a list of noun phrases as strings.
    """

    @abstractmethod
    def extract(self, text: str) -> list[str]:
        """Return a list of noun phrases (strings) for a body of text."""
        ...


##### TOKENIZERS #####


class BaseTokenizer(nltk.tokenize.api.TokenizerI, metaclass=ABCMeta):  # pyright: ignore
    """Abstract base class from which all Tokenizer classes inherit.
    Descendant classes must implement a ``tokenize(text)`` method
    that returns a list of noun phrases as strings.
    """

    @abstractmethod
    def tokenize(self, text: str) -> list[str]:
        """Return a list of tokens (strings) for a body of text.

        :rtype: list
        """
        ...

    def itokenize(self, text: str, *args, **kwargs):
        """Return a generator that generates tokens "on-demand".

        .. versionadded:: 0.6.0

        :rtype: generator
        """
        return (t for t in self.tokenize(text, *args, **kwargs))


##### SENTIMENT ANALYZERS ####


DISCRETE = "ds"
CONTINUOUS = "co"


class BaseSentimentAnalyzer(metaclass=ABCMeta):
    """Abstract base class from which all sentiment analyzers inherit.
    Should implement an ``analyze(text)`` method which returns either the
    results of analysis.
    """

    _trained: bool

    kind = DISCRETE

    def __init__(self):
        self._trained = False

    def train(self):
        # Train me
        self._trained = True

    @abstractmethod
    def analyze(self, text) -> Any:
        """Return the result of of analysis. Typically returns either a
        tuple, float, or dictionary.
        """
        # Lazily train the classifier
        if not self._trained:
            self.train()
        # Analyze text
        return None


##### PARSERS #####


class BaseParser(metaclass=ABCMeta):
    """Abstract parser class from which all parsers inherit from. All
    descendants must implement a ``parse()`` method.
    """

    @abstractmethod
    def parse(self, text: AnyStr):
        """Parses the text."""
        ...
