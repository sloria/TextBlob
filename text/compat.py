# -*- coding: utf-8 -*-
import sys

PY2 = int(sys.version[0]) == 2

if PY2:
    def b(s):
        return s
    def u(s):
        return unicode(s, "unicode_escape")
    from itertools import imap
    import urllib2 as request
    from urllib import quote as urlquote
    text_type = unicode
    binary_type = str
    string_types = (str, unicode)
    unicode = unicode
    basestring = basestring
    imap = imap
else:
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
