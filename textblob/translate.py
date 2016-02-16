# -*- coding: utf-8 -*-
"""
Translator module that uses the Google Translate API.

Adapted from Terry Yin's google-translate-python.
Language detection added by Steven Loria.
"""
from __future__ import absolute_import
import json
import re
import codecs
from textblob.compat import PY2, request, urlencode, basestring
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

    headers = {'Connection': 'keep-alive',
               'Accept': '*/*',
               'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) '
                              'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18'
                              '.0.1025.168 Safari/535.19')
    }

    def translate(self, source, from_lang=None, to_lang='en', host=None, type_=None):
        """Translate the source text from one language to another."""
        result = self._api_request(self.url, source=source, from_lang=from_lang,
                                   to_lang=to_lang, host=host, type_=type_)
        if self._valid(result):
            data = json.loads(result)
            if isinstance(data, list):
                data = data[0]
            elif isinstance(data, basestring):
                data = data

            if data.strip() == source.strip():
                raise NotTranslated('Translation API returned the input string unchanged.')

            return _unescape(data)

        else:
            raise TranslatorError('Translation API returned an unexpected result.')

    def detect(self, source, host=None, type_=None):
        """Detect the source text's language."""
        if len(source) < 3:
            raise TranslatorError('Must provide a string with at least 3 characters.')

        result = self._api_request(self.url, source=source, from_lang='auto',
                                   to_lang='en', host=host, type_=type_)
        if self._valid(result):
            data = json.loads(result)
            return data[1]
        else:
            raise TranslatorError('Translation API could not detect language.')

    def _valid(self, content):
        """Validate API returned valid JSON with expected schema.
        """
        json_data = json.loads(content)
        return ((isinstance(json_data, list) and len(json_data) == 2) or
                (isinstance(json_data, basestring)))

    def _api_request(self, url=url, source=None, from_lang=None, to_lang=None,
                     host=None, type_=None):
        if PY2:
            source = source.encode('utf-8')

        data = {"client": "p", "ie": "UTF-8", "oe": "UTF-8",
                "sl": from_lang or 'auto', "tl": to_lang, "text": source}
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
