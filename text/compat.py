# -*- coding: utf-8 -*-

'''
text.blob Python 3 compatibility module.
'''


import sys

IS_PY3 = (sys.version_info[0] == 3)

if IS_PY3:
    unicode = str
    bytes = bytes
    basestring = str
else:
    unicode = unicode

