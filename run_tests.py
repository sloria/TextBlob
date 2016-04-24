#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
The main test runner script.

Usage: ::
    python run_tests.py
Skip slow tests
    python run_tests.py fast
When there's no Internet
    python run_tests.py no-internet
'''
from __future__ import unicode_literals
import nose
import sys
from textblob.compat import PY2

PY26 = PY2 and int(sys.version_info[1]) < 7
PYPY = "PyPy" in sys.version


def main():
    args = get_argv()
    success = nose.run(argv=args)
    sys.exit(0) if success else sys.exit(1)


def get_argv():
    args = [sys.argv[0], "tests", '--verbosity', '2']
    attr_conditions = []  # Use nose's attribselect plugin to filter tests
    if "force-all" in sys.argv:
        # Don't exclude any tests
        return args
    if "cover" in sys.argv:
        args += ["--with-coverage", "--cover-html"]
    try:
        __import__('numpy')
    except ImportError:
        # Exclude tests that require numpy
        attr_conditions.append("not requires_numpy")
    if not PY2:
        # Exclude tests that only work on python2
        attr_conditions.append("not py2_only")
    if PYPY:
        # Exclude tests that don't work on PyPY
        attr_conditions.append("not no_pypy")
    if "fast" in sys.argv:
        attr_conditions.append("not slow")
    if "no-internet" in sys.argv:
        # Exclude tests that require internet
        attr_conditions.append("not requires_internet")

    # Skip tests with the "skip" attribute
    attr_conditions.append("not skip")

    attr_expression = " and ".join(attr_conditions)
    if attr_expression:
        args.extend(["-A", attr_expression])
    return args

if __name__ == '__main__':
    main()
