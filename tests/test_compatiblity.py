# -*- coding: utf-8 -*-
import unittest
import warnings

from nose.tools import *  # PEP8 asserts


class ImportTest(unittest.TestCase):

    def assert_deprecated_import(self, module):
        '''Assert that importing a module raises a DeprecationWarning.

        :param module: A string, the module name.
        '''
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            __import__(module)
        assert_true(issubclass(w[-1].category, DeprecationWarning))

    def test_old_text_blob(self):
        self.assert_deprecated_import("text.blob")

if __name__ == '__main__':
    unittest.main()
