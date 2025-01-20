"""Custom decorators."""

from __future__ import annotations

from functools import wraps
from typing import TYPE_CHECKING

from textblob.exceptions import MissingCorpusError

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import TypeVar

    ReturnType = TypeVar("ReturnType")


class cached_property:
    """A property that is only computed once per instance and then replaces
    itself with an ordinary attribute. Deleting the attribute resets the
    property.

    Credit to Marcel Hellkamp, author of bottle.py.
    """

    def __init__(self, func):
        self.__doc__ = func.__doc__
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


def requires_nltk_corpus(
    func: Callable[..., ReturnType],
) -> Callable[..., ReturnType]:
    """Wraps a function that requires an NLTK corpus. If the corpus isn't found,
    raise a :exc:`MissingCorpusError`.
    """

    @wraps(func)
    def decorated(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except LookupError as error:
            raise MissingCorpusError() from error

    return decorated
