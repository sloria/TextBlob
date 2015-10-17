from unittest import TestCase

from textblob import Word
from textblob.en.inflect import plural_categories

class InflectTestCase(TestCase):

    def s_singular__pluralize_test(self):
        lens = Word('lens')
        self.assertEquals(lens.pluralize(), 'lenses')

    def s_singular_singularize_test(self):
        lenses = Word('lenses')
        self.assertEquals(lenses.singularize(), 'lens')

    def diagnoses_singularize_test(self):
        diagnoses = Word('diagnoses')
        self.assertEquals(diagnoses.singularize(), 'diagnosis')

    def bus_pluralize_test(self):
        bus = Word('bus')
        self.assertEquals(bus.pluralize(), 'buses')

    def test_all_singular_s(self):
        for w in plural_categories['s-singular']:
            self.assertEquals(Word(w).pluralize().singularize(), w)