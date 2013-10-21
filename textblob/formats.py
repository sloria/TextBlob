# -*- coding: utf-8 -*-
"""File formats for training and testing data."""

from __future__ import absolute_import
from textblob.compat import PY2, csv
import json

DEFAULT_ENCODING = 'utf-8'

class BaseFormat(object):

    """Interface for format classes.

    :param f: A filename.
    """

    def __init__(self, fname):
        pass

    def to_iterable(self):
        '''Return an iterable object from the data.'''
        raise NotImplementedError("Must implement a 'to_iterable' method.")

    @staticmethod
    def detect(stream):
        '''Detect the file format given a filename.
        Return True if a stream is this file format.
        '''
        raise NotImplementedError("Must implement a 'detect' static method.")

class DelimitedFormat(BaseFormat):

    """A general character-delimited format."""

    delimiter = ","

    def __init__(self, fname):
        super(DelimitedFormat, self).__init__(fname)
        with open(fname, 'r') as fp:
            if PY2:
                reader = csv.reader(fp, delimiter=self.delimiter,
                                    encoding=DEFAULT_ENCODING)
            else:
                reader = csv.reader(fp, delimiter=self.delimiter)
            self.data = [row for row in reader]

    def to_iterable(self):
        '''Return an iterable object from the data.'''
        return self.data

    @staticmethod
    def detect(stream):
        '''Return True if stream is valid.'''
        try:
            csv.Sniffer().sniff(stream, delimiters=",")
            return True
        except (csv.Error, TypeError):
            return False


class CSV(DelimitedFormat):

    '''CSV format. Assumes each row is of the form ``text,label``.
    ::

        Today is a good day,pos
        I hate this car.,pos
    '''
    delimiter = ","

    @staticmethod
    def detect(stream):
        '''Return True if stream is valid CSV.'''
        try:
            csv.Sniffer().sniff(stream, delimiters=",")
            return True
        except (csv.Error, TypeError):
            return False

class TSV(DelimitedFormat):

    '''TSV format. Assumes each row is of the form ``text\tlabel``.
    '''

    delimiter = "\t"

    @staticmethod
    def detect(stream):
        '''Return True if stream is valid CSV.'''
        try:
            csv.Sniffer().sniff(stream, delimiters="\t")
            return True
        except (csv.Error, TypeError):
            return False

class JSON(BaseFormat):

    """JSON format.

    Assumes that JSON is formatted as an array of objects with ``text`` and
    ``label`` properties.
    ::

        [
            {"text": "Today is a good day.", "label": "pos"},
            {"text": "I hate this car.", "label": "neg"}
        ]
    """

    def __init__(self, fname):
        super(JSON, self).__init__(fname)
        with open(fname, "r") as fp:
            self.dict = json.load(fp)

    def to_iterable(self):
        '''Return an iterable object from the JSON data.'''
        return [(d['text'], d['label']) for d in self.dict]

    @staticmethod
    def detect(stream):
        '''Return True if stream is valid JSON.'''
        try:
            json.loads(stream)
            return True
        except ValueError:
            return False

AVAILABLE = {
    'csv': CSV,
    'json': JSON,
    'tsv': TSV
}

def detect(filename, max_read=1024):
    '''Attempt to detect a file's format, trying each of the supported
    formats. Return the format class that was detected. If no format is
    detected, return ``None``.
    '''
    with open(filename, 'r') as fp:
        for Format in AVAILABLE.values():
            if Format.detect(fp.read(max_read)):
                return Format
            fp.seek(0)
    return None
