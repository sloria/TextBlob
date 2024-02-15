from unittest import TestCase

from textblob.en.inflect import (
    plural_categories,
    pluralize,
    singular_ie,
    singular_irregular,
    singularize,
)


class InflectTestCase(TestCase):
    def s_singular_pluralize_test(self):
        assert pluralize("lens") == "lenses"

    def s_singular_singularize_test(self):
        assert singularize("lenses") == "lens"

    def diagnoses_singularize_test(self):
        assert singularize("diagnoses") == "diagnosis"

    def bus_pluralize_test(self):
        assert pluralize("bus") == "buses"

    def test_all_singular_s(self):
        for w in plural_categories["s-singular"]:
            assert singularize(pluralize(w)) == w

    def test_all_singular_ie(self):
        for w in singular_ie:
            assert pluralize(w).endswith("ies")
            assert singularize(pluralize(w)) == w

    def test_all_singular_irregular(self):
        for singular_w in singular_irregular.values():
            assert singular_irregular[pluralize(singular_w)] == singular_w
