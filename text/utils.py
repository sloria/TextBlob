# -*- coding: utf-8 -*-

import re
import string

PUNCTUATION_REGEX = re.compile('[{0}]'.format(re.escape(string.punctuation)))


def strip_punc(s):
    '''Removes punctuation from a string.'''
    return PUNCTUATION_REGEX.sub('', s)


def lowerstrip(s):
    '''Makes text all lowercase and strips punctuation and whitespace.'''
    return strip_punc(s.lower().strip())
