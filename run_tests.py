#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
The main test runner script.

Usage:
    python run_tests.py
    # To skip slow tests
    python run_tests.py fast
'''

import os
import sys
from text.compat import PY2

BASE_CMD = 'nosetests'

def get_command():
    command = BASE_CMD
    try:
        __import__('numpy')
    except ImportError:
        # Exclude tests that require numpy
        command += " -a '!requires_numpy'"
    if not PY2:
        # Exclude tests that only work on python2
        command += " -a !py2_only"
    if "fast" in sys.argv:
        command += " -a !slow"
    return command


if __name__ == '__main__':
    os.system(get_command())
