from nose.tools import assert_equals, assert_true
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

    def s_singular_pluralize_test(self):
        assert_equals(pluralize('lens'), 'lenses')

    def s_singular_singularize_test(self):
        assert_equals(singularize('lenses'), 'lens')

    def diagnoses_singularize_test(self):
        assert_equals(singularize('diagnoses'), 'diagnosis')

    def bus_pluralize_test(self):
        assert_equals(pluralize('bus'), 'buses')

    def test_all_singular_s(self):
        for w in plural_categories['s-singular']:
            assert_equals(singularize(pluralize(w)), w)

    def test_all_singular_ie(self):
        for w in singular_ie:
            assert_true(pluralize(w).endswith('ies'))
            assert_equals(singularize(pluralize(w)), w)

    def test_all_singular_irregular(self):
        for singular_w in singular_irregular.values():
            assert_equals(singular_irregular[pluralize(singular_w)], singular_w)
