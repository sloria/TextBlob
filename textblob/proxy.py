#-*- coding: utf-8 -*-
"""
Natural Language Toolkit: Utility functions

Copyright (C) 2001-2021 NLTK Project
Author: Steven Bird <stevenbird1@gmail.com>
URL: <http://nltk.org/>
For license information, see LICENSE.TXT"""
import nltk


def set_proxy(proxy, user=None, password=""):
    """
    Set the HTTP proxy for Python to download through.

    If ``proxy`` is None then tries to set proxy from environment or system
    settings.

    :param proxy: The HTTP proxy server to use. For example:
        'http://proxy.example.com:3128/'
    :param user: The username to authenticate with. Use None to disable
        authentication.
    :param password: The password to authenticate with.
    """
    nltk.set_proxy(proxy, user=user, password=password)
