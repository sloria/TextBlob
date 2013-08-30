# -*- coding: utf-8 -*-
"""File formats."""

from __future__ import absolute_import
from text.compat import PY2, csv

DEFAULT_ENCODING = 'utf-8'

class BaseFormat(object):

    """Interface for format classes.

    :param fname: A filename or file-like object.
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

class CSV(BaseFormat):

    """CSV format."""

    def __init__(self, fname):
        super(CSV, self).__init__(fname)
        try:
            with open(fname, 'r') as fp:
                if PY2:
                    reader = csv.reader(fp, encoding=DEFAULT_ENCODING)
                else:
                    reader = csv.reader(fp)
                self.data = [row for row in reader]
        except TypeError: # fname is a file-like object
            if PY2:
                reader = csv.reader(fname, encoding=DEFAULT_ENCODING)
            else:
                reader = csv.reader(fname)
            self.data = [row for row in reader]

    def to_iterable(self):
        '''Return an iterable object from the CSV data.'''
        return self.data

    @staticmethod
    def detect(stream):
        '''Return True if stream is valid CSV.'''
        try:
            csv.Sniffer().sniff(stream)
            return True
        except (csv.Error, TypeError):
            return False

AVAILABLE = {
    'csv': CSV
}

def detect(filename, max_read=1024):
    '''Attempt to detect a file's format, trying each of the supported
    formats. Return the format class that was detected. If no format is
    detected, return None.
    '''
    with open(filename, 'r') as fp:
        for Format in AVAILABLE.values():
            if Format.detect(fp.read(max_read)):
                return Format
            fp.seek(0)
    return None
