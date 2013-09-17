'''Default taggers to the English taggers for backwards incompatiblity, so you
can still do

>>> from text.taggers import NLTKTagger

which is equivalent to

>>> from text.en.taggers import NLTKTagger
'''
from __future__ import absolute_import
from text.base import BaseTagger
from text.en.taggers import PatternTagger, NLTKTagger, PerceptronTagger