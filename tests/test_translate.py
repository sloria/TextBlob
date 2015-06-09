# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

from nose.plugins.attrib import attr
from nose.tools import *  # noqa (PEP8 asserts)
import mock

from textblob.translate import Translator, _unescape
from textblob.compat import unicode
from textblob.exceptions import TranslatorError

class TestTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = Translator()
        self.sentence = "This is a sentence."

    @mock.patch('textblob.translate.Translator._get_json5')
    def test_translate(self, mock_get_json5):
        mock_get_json5.return_value = unicode('{"sentences":[{"trans":'
                                        '"Esta es una frase.","orig":'
                                        '"This is a sentence.","translit":"",'
                                        '"src_translit":""}],"src":"en",'
                                        '"server_time":2}')
        t = self.translator.translate(self.sentence, to_lang="es")
        assert_equal(t, "Esta es una frase.")
        assert_true(mock_get_json5.called_once)

    @mock.patch('textblob.translate.Translator._get_json5')
    def test_detect_parses_json5(self, mock_get_json5):
        mock_get_json5.return_value = unicode('{"sentences":[{"trans":'
                                        '"This is a sentence.","orig":'
                                        '"This is a sentence.","translit":"",'
                                        '"src_translit":""}],"src":"en",'
                                        '"server_time":1}')
        lang = self.translator.detect(self.sentence)
        assert_equal(lang, "en")
        mock_get_json5.return_value = unicode('{"sentences":[{"trans":'
                                        '"Hello","orig":"Hola",'
                                        '"translit":"","src_translit":""}],'
                                        '"src":"es","server_time":2}')
        lang2 = self.translator.detect("Hola")
        assert_equal(lang2, "es")

    @attr("requires_internet")
    def test_detect(self):
        assert_equal(self.translator.detect('Hola'), "es")
        assert_equal(self.translator.detect('Hello'), "en")

    @attr('requires_internet')
    def test_detect_non_ascii(self):
        lang = self.translator.detect(unicode("关于中文维基百科"))
        assert_equal(lang, 'zh-CN')
        lang2 = self.translator.detect(unicode("известен още с псевдонимите"))
        assert_equal(lang2, "bg")
        lang3 = self.translator.detect(unicode("Избранная статья"))
        assert_equal(lang3, "ru")

    @attr("requires internet")
    def test_translate_spaces(self):
        es_text = u"Hola, me llamo Adrián! Cómo estás? Yo bien"
        to_en = self.translator.translate(es_text, from_lang="es", to_lang="en")
        assert_equal(to_en, "Hello, my name is Adrian! How are you? I'm fine")

    @attr("requires_internet")
    def test_translate_text(self):
        text = "This is a sentence."
        translated = self.translator.translate(text, to_lang="es")
        assert_equal(translated, "Esta es una frase.")
        es_text = "Esta es una frase."
        to_en = self.translator.translate(es_text, from_lang="es", to_lang="en")
        assert_equal(to_en, "This is a sentence.")

    @attr("requires_internet")
    def test_translate_non_ascii(self):
        text = unicode("ذات سيادة كاملة")
        translated = self.translator.translate(text, from_lang='ar', to_lang='en')
        assert_equal(translated, "With full sovereignty")

        text2 = unicode("美丽优于丑陋")
        translated = self.translator.translate(text2, from_lang="zh-CN", to_lang='en')
        assert_equal(translated, "Beautiful is better than ugly")

    @attr("requires_internet")
    def test_translate_unicode_escape(self):
        text = "Jenner & Block LLP"
        translated = self.translator.translate(text, from_lang="en", to_lang="en")
        assert_equal(translated, "Jenner & Block LLP")

    def test_detect_requires_more_than_two_characters(self):
        assert_raises(TranslatorError, lambda: self.translator.detect('f'))
        assert_raises(TranslatorError, lambda: self.translator.detect('fo'))

    def test_get_language_from_json5(self):
        json5 = ('{"sentences":[{"trans":"This is a sentence.",'
                 '"orig":"This is a sentence.","translit":"",'
                 '"src_translit":""}],"src":"en","server_time":1}')
        lang = self.translator._get_language_from_json5(json5)
        assert_equal(lang, "en")


def test_unescape():
    assert_equal(_unescape('and'), 'and')
    assert_equal(_unescape('\u0026'), '&')

if __name__ == '__main__':
    unittest.main()
