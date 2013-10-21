# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import unittest
from nose.plugins.attrib import attr
from nose.tools import *  # PEP8 asserts

from textblob.translate import Translator
from textblob.compat import unicode

@attr('requires_internet')
class TestTranslator(unittest.TestCase):

    def setUp(self):
        self.translator = Translator()
        self.sentence = "This is a sentence."

    def test_translate(self):
        t = self.translator.translate(self.sentence, to_lang="es")
        assert_equal(t, "Esta es una frase.")

    def test_detect(self):
        lang = self.translator.detect(self.sentence)
        assert_equal(lang, "en")
        lang2 = self.translator.detect("Hola")
        assert_equal(lang2, "es")
        lang3 = self.translator.detect("Kumusta ka na?")
        assert_equal(lang3, "tl")
        lang4 = self.translator.detect("Programmiersprache")
        assert_equal(lang4, 'de')

    def test_detect_non_ascii(self):
        lang = self.translator.detect(unicode("关于中文维基百科"))
        assert_equal(lang, 'zh-CN')
        lang2 = self.translator.detect(unicode("известен още с псевдонимите"))
        assert_equal(lang2, "bg")
        lang3 = self.translator.detect(unicode("Избранная статья"))
        assert_equal(lang3, "ru")


    def test_get_language_from_json5(self):
        json5 = '[[["This is a sentence.","This is a sentence.","",""]],,"en",,,,,,[["en"]],0]'
        lang = self.translator._get_language_from_json5(json5)
        assert_equal(lang, "en")

if __name__ == '__main__':
    unittest.main()
