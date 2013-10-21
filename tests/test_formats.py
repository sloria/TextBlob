# -*- coding: utf-8 -*-
import os
import unittest
import logging
from nose.tools import *  # PEP8 asserts

from textblob import formats
from textblob.compat import unicode

logging.basicConfig(level=logging.DEBUG)
HERE = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(HERE, 'data.csv')
JSON_FILE = os.path.join(HERE, "data.json")
TSV_FILE = os.path.join(HERE, "data.tsv")

class TestFormats(unittest.TestCase):

    def setUp(self):
        pass

    def test_detect_csv(self):
        format = formats.detect(CSV_FILE)
        assert_equal(format, formats.CSV)

    def test_detect_json(self):
        format = formats.detect(JSON_FILE)
        assert_equal(format, formats.JSON)

    def test_available(self):
        assert_true('csv' in formats.AVAILABLE.keys())
        assert_true('json' in formats.AVAILABLE.keys())
        assert_true('tsv' in formats.AVAILABLE.keys())

class TestDelimitedFormat(unittest.TestCase):

    def test_delimiter_defaults_to_comma(self):
        assert_equal(formats.DelimitedFormat.delimiter, ",")

    def test_detect(self):
        with open(CSV_FILE, 'r') as fp:
            stream = fp.read()
            assert_true(formats.DelimitedFormat.detect(stream))
        with open(JSON_FILE, 'r') as fp:
            stream = fp.read()
            assert_false(formats.DelimitedFormat.detect(stream))

class TestCSV(unittest.TestCase):

    def test_read_from_filename(self):
        data = formats.CSV(CSV_FILE)

    def test_detect(self):
        with open(CSV_FILE, 'r') as fp:
            stream = fp.read()
            assert_true(formats.CSV.detect(stream))
        with open(JSON_FILE, 'r') as fp:
            stream = fp.read()
            assert_false(formats.CSV.detect(stream))

class TestTSV(unittest.TestCase):

    def test_read_from_filename(self):
        data = formats.TSV(TSV_FILE)

    def test_detect(self):
        with open(TSV_FILE, 'r') as fp:
            stream = fp.read()
            assert_true(formats.TSV.detect(stream))

        with open(CSV_FILE, 'r') as fp:
            stream = fp.read()
            assert_false(formats.TSV.detect(stream))

class TestJSON(unittest.TestCase):

    def test_read_from_filename(self):
        formats.JSON(JSON_FILE)

    def test_detect(self):
        with open(JSON_FILE, 'r') as fp:
            stream = fp.read()
            assert_true(formats.JSON.detect(stream))
        with open(CSV_FILE, 'r') as fp:
            stream = fp.read()
            assert_false(formats.JSON.detect(stream))

    def test_to_iterable(self):
        d = formats.JSON(JSON_FILE)
        logging.debug(d.dict)
        data = d.to_iterable()
        first = data[0]
        text, label = first[0], first[1]
        assert_true(isinstance(text, unicode))

if __name__ == '__main__':
    unittest.main()
