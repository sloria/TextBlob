from __future__ import annotations

import re
import string
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from nltk.tree import Tree

PUNCTUATION_REGEX = re.compile(f"[{re.escape(string.punctuation)}]")


def strip_punc(s: str, all: bool = False) -> str:
    """Removes punctuation from a string.

    :param s: The string.
    :param all: Remove all punctuation. If False, only removes punctuation from
        the ends of the string.
    """
    if all:
        return PUNCTUATION_REGEX.sub("", s.strip())
    else:
        return s.strip().strip(string.punctuation)


def lowerstrip(s: str, all: bool = False) -> str:
    """Makes text all lowercase and strips punctuation and whitespace.

    :param s: The string.
    :param all: Remove all punctuation. If False, only removes punctuation from
        the ends of the string.
    """
    return strip_punc(s.lower().strip(), all=all)


def tree2str(tree: Tree, concat: str = " ") -> str:
    """Convert a nltk.tree.Tree to a string.

    For example:
        (NP a/DT beautiful/JJ new/JJ dashboard/NN) -> "a beautiful dashboard"
    """
    return concat.join([word for (word, _) in tree])


def filter_insignificant(
    chunk: Iterable[tuple[str, str]],
    tag_suffixes: Iterable[str] = ("DT", "CC", "PRP$", "PRP"),
) -> list[tuple[str, str]]:
    """Filter out insignificant (word, tag) tuples from a chunk of text."""
    good: list[tuple[str, str]] = []
    for word, tag in chunk:
        ok = True
        for suffix in tag_suffixes:
            if tag.endswith(suffix):
                ok = False
                break
        if ok:
            good.append((word, tag))
    return good


def is_filelike(obj: object) -> bool:
    """Return whether ``obj`` is a file-like object."""
    if not hasattr(obj, "read"):
        return False
    if not callable(obj.read):
        return False
    return True
