import sys

PY2 = int(sys.version[0]) == 2

if PY2:
    text_type = unicode
    binary_type = str
    string_types = (str, unicode)
    unicode = unicode
else:
    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
