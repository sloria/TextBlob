# -*- coding: utf-8 -*-

import re
import string

PUNCTUATION_REGEX = re.compile('[{0}]'.format(re.escape(string.punctuation)))

def strip_punc(s, all=False):
    '''Removes punctuation from a string.

    :param s: The string.
    :param all: Remove all punctuation. If False, only removes punctuation from
        the ends of the string.
    '''
    if all:
        return PUNCTUATION_REGEX.sub('', s.strip())
    else:
        return s.strip().strip(string.punctuation)


def lowerstrip(s, all=False):
    '''Makes text all lowercase and strips punctuation and whitespace.

    :param s: The string.
    :param all: Remove all punctuation. If False, only removes punctuation from
        the ends of the string.
    '''
    return strip_punc(s.lower().strip(), all=all)
