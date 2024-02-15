"""Make word inflection default to English. This allows for backwards
compatibility so you can still import text.inflect.

    >>> from textblob.inflect import singularize

is equivalent to

    >>> from textblob.en.inflect import singularize
"""
from textblob.en.inflect import pluralize, singularize

__all__ = [
    "singularize",
    "pluralize",
]
