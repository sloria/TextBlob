# -*- coding: utf-8 -*-
import sys

PY2 = int(sys.version[0]) == 2
PY26 = PY2 and int(sys.version_info[1]) < 7

if PY2:
    from itertools import imap, izip
    import urllib2 as request
    from urllib import quote as urlquote
    from urllib import urlencode
    text_type = unicode
    binary_type = str
    string_types = (str, unicode)
    unicode = unicode
    basestring = basestring
    imap = imap
    izip = izip
    import unicodecsv as csv
    if PY26:
        from .ordereddict import OrderedDict
    else:
        from collections import OrderedDict

    def implements_to_string(cls):
        """Class decorator that renames __str__ to __unicode__ and
        modifies __str__ that returns utf-8.
        """
        cls.__unicode__ = cls.__str__
        cls.__str__ = lambda x: x.__unicode__().encode('utf-8')
        return cls
else: # PY3
    from urllib import request
    from urllib.parse import quote as urlquote
    from urllib.parse import urlencode
    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)
    imap = map
    izip = zip
    import csv
    from collections import OrderedDict

    implements_to_string = lambda x: x


def with_metaclass(meta, *bases):
    """Defines a metaclass.

    Creates a dummy class with a dummy metaclass. When subclassed, the dummy
    metaclass is used, which has a constructor that instantiates a
    new class from the original parent. This ensures that the dummy class and
    dummy metaclass are not in the inheritance tree.

    Credit to Armin Ronacher.
    """
    class metaclass(meta):
        __call__ = type.__call__
        __init__ = type.__init__
        def __new__(cls, name, this_bases, d):
            if this_bases is None:
                return type.__new__(cls, name, (), d)
            return meta(name, bases, d)
    return metaclass('temporary_class', None, {})
