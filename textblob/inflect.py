# -*- coding: utf-8 -*-
'''Make word inflection default to English. This allows for backwards
compatibility so you can still import text.inflect.

    >>> from text.inflect import singularize

is equivalent to

    >>> from text.en.inflect import singularize
'''
from __future__ import absolute_import
from textblob.en.inflect import singularize, pluralize
