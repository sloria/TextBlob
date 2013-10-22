# -*- coding: utf-8 -*-
'''
Translator module that uses the Google Translate API.

Adapted from Terry Yin's google-translate-python.
Language detection added by Steven Loria.
'''
from __future__ import absolute_import
import re
from textblob.compat import PY2, request, urlquote


class Translator(object):

    '''A language translator and detector.

    Usage:
    ::
        >>> from textblob.translate import Translator
        >>> t = Translator()
        >>> t.translate('hello', from_lang='en', to_lang='fr')
        u'bonjour'
        >>> t.detect("hola")
        u'es'
    '''

    string_pattern = r"\"(([^\"\\]|\\.)*)\""
    translation_pattern = re.compile(
                        r"\,?\["
                           + string_pattern + r"\,"
                           + string_pattern + r"\,"
                           + string_pattern + r"\,"
                           + string_pattern
                        +r"\]")
    detection_pattern = re.compile(
            r".*?\,\"([a-z]{2}(\-\w{2})?)\"\,.*?", flags=re.S)

    translate_url = ("http://translate.google.com/translate_a/"
                    "t?client=t&ie=UTF-8&oe=UTF-8&sl={0}&tl={1}&text={2}")
    detect_url = "http://translate.google.com/translate_a/t?client=t&ie=UTF-8&oe=UTF-8&text={0}"

    headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) '
            'AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.168 Safari/535.19')}

    def translate(self, source, from_lang='en', to_lang='en', host=None, type_=None):
        '''Translate the source text from one language to another.'''
        if PY2:
            source = source.encode('utf-8')
        escaped_source = urlquote(source, '')
        url = self.translate_url.format(from_lang, to_lang, escaped_source)
        json5 = self._get_json5(url, host=host, type_=type_)
        return self._unescape(self._get_translation_from_json5(json5))

    def detect(self, source, host=None, type_=None):
        '''Detect the source text's language.'''
        if PY2:
            source = source.encode('utf-8')
        escaped_source = urlquote(source, '')
        url = self.detect_url.format(escaped_source)
        json5 = self._get_json5(url, host=host, type_=type_)
        lang = self._get_language_from_json5(json5)
        return lang

    def _get_language_from_json5(self, content):
        match = self.detection_pattern.match(content)
        if not match:
            return None
        return match.group(1)

    def _get_translation_from_json5(self, content):
        result = ""
        pos = 2
        while True:
            m = self.translation_pattern.match(content, pos)
            if not m:
                break
            result += m.group(1)
            pos = m.end()
        return result

    def _get_json5(self, url, host=None, type_=None):
        req = request.Request(url=url, headers=self.headers)
        if host or type_:
            req.set_proxy(host=host, type=type_)
        r = request.urlopen(req)
        content = r.read()
        return content.decode('utf-8')

    def _unescape(self, text):
        return re.sub(r"\\.?", lambda x:eval('"%s"'%x.group(0)), text)
