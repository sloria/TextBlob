# -*- coding: utf-8 -*-
import os
import unittest
from nose.tools import *  # PEP8 asserts

from text import formats

HERE = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(HERE, 'data.csv')

class TestFormats(unittest.TestCase):

    def setUp(self):
        pass

    def test_detect_csv(self):
        format = formats.detect(CSV_FILE)
        assert_equal(format, formats.CSV)

class TestCSV(unittest.TestCase):

    def test_read_from_filename(self):
        data = formats.CSV(CSV_FILE)

    def test_read_from_fileobject(self):
        with open(CSV_FILE, 'r') as fp:
            data = formats.CSV(fp)

    def test_detect(self):
        with open(CSV_FILE, 'r') as fp:
            stream = fp.read()
            assert_true(formats.CSV.detect(stream))

if __name__ == '__main__':
    unittest.main()