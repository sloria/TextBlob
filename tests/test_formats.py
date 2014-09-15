# -*- coding: utf-8 -*-
import os
import unittest
from nose.tools import *  # noqa (PEP8 asserts)

from textblob import formats
from textblob.compat import unicode

HERE = os.path.abspath(os.path.dirname(__file__))
CSV_FILE = os.path.join(HERE, 'data.csv')
JSON_FILE = os.path.join(HERE, "data.json")
TSV_FILE = os.path.join(HERE, "data.tsv")

class TestFormats(unittest.TestCase):

    def setUp(self):
        pass

    def test_detect_csv(self):
        with open(CSV_FILE) as fp:
            format = formats.detect(fp)
        assert_equal(format, formats.CSV)

    def test_detect_json(self):
        with open(JSON_FILE) as fp:
            format = formats.detect(fp)
        assert_equal(format, formats.JSON)

    def test_available(self):
        registry = formats.get_registry()
        assert_true('csv' in registry.keys())
        assert_true('json' in registry.keys())
        assert_true('tsv' in registry.keys())

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
        with open(CSV_FILE) as fp:
            data = formats.CSV(fp)

    def test_detect(self):
        with open(CSV_FILE, 'r') as fp:
            stream = fp.read()
            assert_true(formats.CSV.detect(stream))
        with open(JSON_FILE, 'r') as fp:
            stream = fp.read()
            assert_false(formats.CSV.detect(stream))

class TestTSV(unittest.TestCase):

    def test_read_from_file_object(self):
        with open(TSV_FILE) as fp:
            data = formats.TSV(fp)

    def test_detect(self):
        with open(TSV_FILE, 'r') as fp:
            stream = fp.read()
            assert_true(formats.TSV.detect(stream))

        with open(CSV_FILE, 'r') as fp:
            stream = fp.read()
            assert_false(formats.TSV.detect(stream))

class TestJSON(unittest.TestCase):

    def test_read_from_file_object(self):
        with open(JSON_FILE) as fp:
            formats.JSON(fp)

    def test_detect(self):
        with open(JSON_FILE, 'r') as fp:
            stream = fp.read()
            assert_true(formats.JSON.detect(stream))
        with open(CSV_FILE, 'r') as fp:
            stream = fp.read()
            assert_false(formats.JSON.detect(stream))

    def test_to_iterable(self):
        with open(JSON_FILE) as fp:
            d = formats.JSON(fp)
        data = d.to_iterable()
        first = data[0]
        text, label = first[0], first[1]
        assert_true(isinstance(text, unicode))

class CustomFormat(formats.BaseFormat):
    def to_iterable():
        return [
            ('I like turtles', 'pos'),
            ('I hate turtles', 'neg')
        ]
    @classmethod
    def detect(cls, stream):
        return True


class TestRegistry(unittest.TestCase):
    def setUp(self):
        pass

    def test_register(self):
        registry = formats.get_registry()
        assert_false(CustomFormat in registry.values())

        formats.register('trt', CustomFormat)

        assert_true(CustomFormat in registry.values())
        assert_true('trt' in registry.keys())


if __name__ == '__main__':
    unittest.main()
