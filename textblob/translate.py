# -*- coding: utf-8 -*-
"""
Translator module that uses the Google Translate API.

Adapted from Terry Yin's google-translate-python.
Language detection added by Steven Loria.
"""
from __future__ import absolute_import

import codecs
import ctypes
import json
import re
import time

from textblob.compat import PY2, request, urlencode
from textblob.exceptions import TranslatorError, NotTranslated


class Translator(object):

    """A language translator and detector.

    Usage:
    ::
        >>> from textblob.translate import Translator
        >>> t = Translator()
        >>> t.translate('hello', from_lang='en', to_lang='fr')
        u'bonjour'
        >>> t.detect("hola")
        u'es'
    """

    url = "http://translate.google.com/translate_a/t"

    headers = {
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'User-Agent': (
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) '
            'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')
    }

    def translate(self, source, from_lang='auto', to_lang='en', host=None, type_=None):
        """Translate the source text from one language to another."""
        if PY2:
            source = source.encode('utf-8')
        data = {"client": "p",
                "ie": "UTF-8", "oe": "UTF-8",
                "dt": "at", "tk": _calculate_tk(source),
                "sl": from_lang, "tl": to_lang, "text": source}
        response = self._request(self.url, host=host, type_=type_, data=data)
        result = json.loads(response)
        if isinstance(result, list):
            try:
                result = result[0]  # ignore detected language
            except IndexError:
                pass
        self._validate_translation(source, result)
        return result

    def detect(self, source, host=None, type_=None):
        """Detect the source text's language."""
        if PY2:
            source = source.encode('utf-8')
        if len(source) < 3:
            raise TranslatorError('Must provide a string with at least 3 characters.')
        data = {"client": "p",
                "ie": "UTF-8", "oe": "UTF-8",
                "dt": "at", "tk": _calculate_tk(source),
                "sl": "auto", "text": source}
        response = self._request(self.url, host=host, type_=type_, data=data)
        result, language = json.loads(response)
        return language

    def _validate_translation(self, source, result):
        """Validate API returned expected schema, and that the translated text
        is different than the original string.
        """
        if not result:
            raise NotTranslated('Translation API returned and empty response.')
        if PY2:
            result = result.encode('utf-8')
        if result.strip() == source.strip():
            raise NotTranslated('Translation API returned the input string unchanged.')

    def _request(self, url, host=None, type_=None, data=None):
        encoded_data = urlencode(data).encode('utf-8')
        req = request.Request(url=url, headers=self.headers, data=encoded_data)
        if host or type_:
            req.set_proxy(host=host, type=type_)
        resp = request.urlopen(req)
        content = resp.read()
        return content.decode('utf-8')


def _unescape(text):
    """Unescape unicode character codes within a string.
    """
    pattern = r'\\{1,2}u[0-9a-fA-F]{4}'
    decode = lambda x: codecs.getdecoder('unicode_escape')(x.group())[0]
    return re.sub(pattern, decode, text)


def _calculate_tk(source):
    """Reverse engineered cross-site request protection."""
    # Source: https://github.com/soimort/translate-shell/issues/94#issuecomment-165433715
    b = int(time.time() / 3600)

    if PY2:
        d = map(ord, source)
    else:
        d = source.encode('utf-8')

    def RL(a, b):
        for c in range(0, len(b) - 2, 3):
            d = b[c+2]
            d = ord(d) - 87 if d >= 'a' else int(d)
            xa = ctypes.c_uint32(a).value
            d = xa >> d if b[c+1] == '+' else xa << d
            a = a + d & 4294967295 if b[c] == '+' else a ^ d
        return ctypes.c_int32(a).value

    a = b
    for di in d:
        a = RL(a + di, "+-a^+6")
    a = RL(a, "+-3^+b+-f")
    a = a if a >= 0 else ((a & 2147483647) + 2147483648)
    a %= pow(10, 6)

    tk = '{0:d}.{1:d}'.format(a, a ^ b)
    return tk
