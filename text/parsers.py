# -*- coding: utf-8 -*-
'''Default parsers to English for backwards compatibility so you can still do

>>> from text.parsers import PatternParser

which is equivalent to

>>> from text.en.parsers import PatternParser
'''
from __future__ import absolute_import
from text.base import BaseParser
from text.en.parsers import PatternParser