from unittest import TestCase

from textblob import Word


class PluralizationTestCase(TestCase):

    def s_singular__pluralize_test(self):
        lens = Word('lens')
        self.assertEquals(lens.pluralize(), 'lenses')

    def s_singular_singularize_test(self):
        lenses = Word('lenses')
        self.assertEquals(lenses.singularize(), 'lens')

    def diagnoses_singularize_test(self):
        diagnoses = Word('diagnoses')
        self.assertEquals(diagnoses.singularize(), 'diagnosis')
