# -*- coding: utf-8 -*-
'''Various parser implementations.

.. versionadded:: 0.6.0
'''
from __future__ import absolute_import
from text.en import parse as pattern_parse

class BaseParser(object):

    '''Abstract parser class from which all parsers inherit from. All
    descendants must implement a `parse()` method.
    '''

    def parse(self, text):
        '''Parses the text.'''
        raise NotImplementedError("Must implement a parse() method.")

class PatternParser(BaseParser):

    '''Parser that uses the implementation in Tom de Smedt's pattern library.
    http://www.clips.ua.ac.be/pages/pattern-en#parser
    '''

    def parse(self, text):
        '''Parses the text.'''
        return pattern_parse(text)
