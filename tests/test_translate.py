# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest

from nose.plugins.attrib import attr
from nose.tools import *  # PEP8 asserts
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
        mock_get_json5.return_value = unicode('[[["Esta es una frase","This is a '
            'sentence","",""]],,"en",,[["Esta es una",[1],true,false,374,0,3,0]'
            ',["frase",[2],true,false,470,3,4,0]],[["This is a",1,[["Esta es'
            ' una",374,true,false],["Se trata de una",6,true,false],'
            '["Este es un",0,true,false],["Se trata de un",0,true,false],'
            '["Esto es un",0,true,false]],[[0,9]],"This is a sentence"],'
            '["sentence",2,[["frase",470,true,false],["sentencia",6,true,false],'
            '["oraci\xf3n",0,true,false],["pena",0,true,false],["condena"'
            ',0,true,false]],[[10,18]],""]],,,[["en"]],29]')
        t = self.translator.translate(self.sentence, to_lang="es")
        assert_equal(t, "Esta es una frase")
        assert_true(mock_get_json5.called_once)

    @mock.patch('textblob.translate.Translator._get_json5')
    def test_detect_parses_json5(self, mock_get_json5):
        mock_get_json5.return_value = unicode('[[["This is a sentence",'
            '"This is a sentence","",""]],,"en",,,,,,[["en"]],4]')
        lang = self.translator.detect(self.sentence)
        assert_equal(lang, "en")
        mock_get_json5.return_value = unicode('[[["Hello","Hola","",""]],[["interjection",'
                                        '["Hello!","Hi!","Hey!","Hullo!","Hallo!",'
                                        '"Hoy!","Hail!"],[["Hello!",["\xa1Hola!","'
                                        '\xa1Caramba!","\xa1Oiga!","\xa1Diga!","'
                                        '\xa1Bueno!","\xa1Vale!"],,0.39160562],'
                                        '["Hi!",["\xa1Hola!"],,0.24506053],'
                                        '["Hey!",["\xa1Hola!","\xa1Eh!"],,0.038173068]'
                                        ',["Hullo!",["\xa1Hola!","\xa1Caramba!",'
                                        '"\xa1Oiga!","\xa1Diga!","\xa1Bueno!",'
                                        '"\xa1Al\xf3!"]],["Hallo!",["\xa1Hola!",'
                                        '"\xa1Caramba!","\xa1Oiga!","\xa1Bueno!"]],'
                                        '["Hoy!",["\xa1Eh!","\xa1Hola!"]],["Hail!",'
                                        '["\xa1Salve!","\xa1Hola!"]]],"\xa1Hola!",9]],'
                                        '"es",,[["Hello",[1],true,false,783,0,1,0]],'
                                        '[["Hola",1,[["Hello",783,true,false],'
                                        '["Hi",214,true,false],["Hola",1,true,false],'
                                        '["Hey",0,true,false],["Welcome",0,true,false]],'
                                        '[[0,4]],"Hola"]],,,[],4]')
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

    @attr("requires_internet")
    def test_translate(self):
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
        assert_equal(translated, "Fully sovereign")

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
        json5 = '[[["This is a sentence.","This is a sentence.","",""]],,"en",,,,,,[["en"]],0]'
        lang = self.translator._get_language_from_json5(json5)
        assert_equal(lang, "en")


def test_unescape():
    assert_equal(_unescape('and'), 'and')
    assert_equal(_unescape('\u0026'), '&')

if __name__ == '__main__':
    unittest.main()
