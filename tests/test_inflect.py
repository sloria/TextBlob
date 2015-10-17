from unittest import TestCase

from textblob.en.inflect import (
    plural_categories,
    singular_ie,
    singular_irregular,
    singular_uncountable,
    singular_uninflected,
    singularize,
    pluralize
)


class InflectTestCase(TestCase):

    def s_singular__pluralize_test(self):
        self.assertEquals(pluralize('lens'), 'lenses')

    def s_singular_singularize_test(self):
        self.assertEquals(singularize('lenses'), 'lens')

    def diagnoses_singularize_test(self):
        self.assertEquals(singularize('diagnoses'), 'diagnosis')

    def bus_pluralize_test(self):
        self.assertEquals(pluralize('bus'), 'buses')

    def test_all_singular_s(self):
        for w in plural_categories['s-singular']:
            self.assertEquals(singularize(pluralize(w)), w)

    def test_all_singular_ie(self):
        for w in singular_ie:
            self.assertTrue(pluralize(w).endswith('ies'))
            self.assertEquals(singularize(pluralize(w)), w)

    def test_all_singular_irregular(self):
        for singular_w in singular_irregular.values():
            self.assertEquals(singular_irregular[pluralize(singular_w)], singular_w)
