# -*- coding: utf-8 -*-
'''Default noun phrase extractors are for English to maintain backwards
compatibility, so you can still do

>>> from text.np_extractors import ConllExtractor

which is equivalent to

>>> from text.en.np_extractors import ConllExtractor
'''
from __future__ import absolute_import
from text.base import BaseNPExtractor
from text.en.np_extractors import ConllExtractor, FastNPExtractor