# -*- coding: utf-8 -*-
'''text module for backwards compatibility. Importing
``text`` is now deprecated.

.. deprecated:: 0.8.0
    Import ``textblob`` instead.
'''
from __future__ import absolute_import
import warnings

warnings.warn("Importing text is deprecated. Import textblob instead.",
                category=DeprecationWarning)

from textblob import *
