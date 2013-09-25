# -*- coding: utf-8 -*-
import sys

PY2 = int(sys.version[0]) == 2

if PY2:
    def b(s):
        return s
    def u(s):
        return unicode(s, "unicode_escape")
    from itertools import imap, izip
    import urllib2 as request
    from urllib import quote as urlquote
    text_type = unicode
    binary_type = str
    string_types = (str, unicode)
    unicode = unicode
    basestring = basestring
    imap = imap
    izip = izip
    import unicodecsv as csv

    def implements_to_string(cls):
        '''Class decorator that renames __str__ to __unicode__ and
        modifies __str__ that returns utf-8.
        '''
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls

else: # PY3
    def b(s):
        return s.encode("latin-1")
    def u(s):
        return s
    from urllib import request
    from urllib.parse import quote as urlquote
    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)
    imap = map
    izip = zip
    import csv

    implements_to_string = lambda x: x


def add_metaclass(metaclass):
    """Class decorator for creating a class with a metaclass.
    From the six library.
    """
    def wrapper(cls):
        orig_vars = cls.__dict__.copy()
        orig_vars.pop('__dict__', None)
        orig_vars.pop('__weakref__', None)
        for slots_var in orig_vars.get('__slots__', ()):
            orig_vars.pop(slots_var)
        return metaclass(cls.__name__, cls.__bases__, orig_vars)
    return wrapper
