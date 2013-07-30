#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
The main test runner script.

Usage:
    python run_tests.py
    # To skip slow tests
    python run_tests.py fast
'''
from __future__ import unicode_literals
import nose
import sys
from text.compat import PY2

PY26 = PY2 and int(sys.version_info[1]) < 7


def main():
    args = get_argv()
    success = nose.run(argv=args)
    sys.exit(0) if success else sys.exit(1)


def get_argv():
    args = [sys.argv[0], '--exclude', 'nltk']
    attr_conditions = []  # Use nose's attribselect plugin to filter tests
    if "force-all" in sys.argv:
        # Don't exclude any tests
        return args
    if PY26:
        # Exclude tests that don't work on python2.6
        attr_conditions.append("not py27_only")
    try:
        __import__('numpy')
    except ImportError:
        # Exclude tests that require numpy
        attr_conditions.append("not requires_numpy")
    if not PY2:
        # Exclude tests that only work on python2
        attr_conditions.append("not py2_only")
    if "fast" in sys.argv:
        attr_conditions.append("not slow")

    attr_expression = " and ".join(attr_conditions)
    if attr_expression:
        args.extend(["-A", attr_expression])
    return args

if __name__ == '__main__':
    main()
