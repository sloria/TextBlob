# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import re

from nose.plugins.attrib import attr
from nose.tools import *  # noqa (PEP8 asserts)
import mock

from textblob.translate import Translator, _unescape
from textblob.exceptions import TranslatorError, NotTranslated


class TestTranslator(unittest.TestCase):

    """Unit tests with external requests mocked out."""

    def setUp(self):
        self.translator = Translator()
        self.sentence = "This is a sentence."

    @mock.patch('textblob.translate.Translator._request')
    def test_translate(self, mock_request):
        mock_request.return_value = '["Esta es una frase.","en"]'
        t = self.translator.translate(self.sentence, to_lang="es")
        assert_equal(t, "Esta es una frase.")
        assert_true(mock_request.called_once)

    @mock.patch('textblob.translate.Translator._request')
    def test_failed_translation_raises_not_translated(self, mock_request):
        failed_responses = ['""', '[""]', '["",""]', '" n0tv&l1d "']
        mock_request.side_effect = failed_responses
        text = ' n0tv&l1d '
        for response in failed_responses:
            assert_raises(NotTranslated,
                          self.translator.translate, text, to_lang="es")
        assert_equal(mock_request.call_count, len(failed_responses))

    @mock.patch("textblob.translate.Translator._request")
    def test_tk_parameter_included_in_request_url(self, mock_request):
        mock_request.return_value = '["Esta es una frase.","en"]'
        self.translator.translate(self.sentence, to_lang="es")
        assert_true(mock_request.called_once)
        args, kwargs = mock_request.call_args
        url = args[0]
        assert_true(re.match('.+&tk=\d+\.\d+$', url))

    @mock.patch('textblob.translate.Translator._request')
    def test_detect(self, mock_request):
        mock_request.return_value = '["Esta es una frase.","en"]'
        language = self.translator.detect(self.sentence)
        assert_equal(language, "en")
        assert_true(mock_request.called_once)

    def test_detect_requires_more_than_two_characters(self):
        assert_raises(TranslatorError, lambda: self.translator.detect('f'))
        assert_raises(TranslatorError, lambda: self.translator.detect('fo'))


@attr("requires_internet")
class TestTranslatorIntegration(unittest.TestCase):

    """Integration tests that actually call the translation API."""

    def setUp(self):
        self.translator = Translator()

    def test_detect(self):
        assert_equal(self.translator.detect('Hola'), "es")
        assert_equal(self.translator.detect('Hello'), "en")

    def test_detect_non_ascii(self):
        lang = self.translator.detect("关于中文维基百科")
        assert_equal(lang, 'zh-CN')
        lang2 = self.translator.detect("известен още с псевдонимите")
        assert_equal(lang2, "bg")
        lang3 = self.translator.detect("Избранная статья")
        assert_equal(lang3, "ru")

    def test_translate_spaces(self):
        es_text = "Hola, me llamo Adrián! Cómo estás? Yo bien"
        to_en = self.translator.translate(es_text, from_lang="es", to_lang="en")
        assert_equal(to_en, "Hello, my name is Adrian! How are you? I am good")

    def test_translate_missing_from_language_auto_detects(self):
        text = "Ich hole das Bier"
        translated = self.translator.translate(text, to_lang="en")
        assert_equal(translated, "I'll get the beer")

    def test_translate_text(self):
        text = "This is a sentence."
        translated = self.translator.translate(text, to_lang="es")
        assert_equal(translated, "Esta es una frase.")
        es_text = "Esta es una frase."
        to_en = self.translator.translate(es_text, from_lang="es", to_lang="en")
        assert_equal(to_en, "This is a phrase.")

    def test_translate_non_ascii(self):
        text = "ذات سيادة كاملة"
        translated = self.translator.translate(text, from_lang='ar', to_lang='en')
        assert_equal(translated, "With full sovereignty")

        text2 = "美丽比丑陋更好"
        translated = self.translator.translate(text2, from_lang="zh-CN", to_lang='en')
        assert_equal(translated, "Beauty is better than ugly")

    @mock.patch('textblob.translate.Translator._validate_translation', mock.MagicMock())
    def test_translate_unicode_escape(self):
        text = "Jenner & Block LLP"
        translated = self.translator.translate(text, from_lang="en", to_lang="en")
        assert_equal(translated, "Jenner & Block LLP")


def test_unescape():
    assert_equal(_unescape('and'), 'and')
    assert_equal(_unescape('\u0026'), '&')


if __name__ == '__main__':
    unittest.main()
