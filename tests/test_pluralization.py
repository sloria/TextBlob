from unittest import TestCase

from textblob import Word


class PluralizationTestCase(TestCase):

    def s_singular_test(self):
        lens = Word('lens')
        self.assertEquals(lens.pluralize(), 'lenses')
