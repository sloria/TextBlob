# -*- coding: utf-8 -*-
'''Default sentiment analyzers are English for backwards compatibility, so
you can still do

>>> from text.sentiments import PatternAnalyzer

which is equivalent to

>>> from text.en.sentiments import PatternAnalyzer
'''
from __future__ import absolute_import
from text.base import BaseSentimentAnalyzer
from text.en.sentiments import (DISCRETE, CONTINUOUS,
                                PatternAnalyzer, NaiveBayesAnalyzer)