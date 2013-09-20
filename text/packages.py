# -*- coding: utf-8 -*-
'''
Module to provide import context for vendorized packages such as nltk.
'''
from __future__ import absolute_import
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.append(HERE)

import nltk
