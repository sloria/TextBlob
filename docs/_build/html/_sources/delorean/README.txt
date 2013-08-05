.. image:: https://travis-ci.org/myusuf3/delorean.png?branch=master


.. image:: https://pypip.in/d/Delorean/badge.png
    :target: https://crate.io/packages/Delorean/
    :alt: Number of PyPI downloads

Delorean: Time Travel Made Easy
===============================

`Delorean` is a library for clearing up the inconvenient truths that arise dealing with datetimes in Python. Understanding that timing is a delicate enough of a problem `delorean` hopes to provide a cleaner less troublesome solution to shifting, manipulating, and generating `datetimes`.

Delorean stands on the shoulders of giants `pytz <http://pytz.sourceforge.net/>`_ and `dateutil <http://labix.org/python-dateutil>`_

`Delorean` will provide natural language improvements for manipulating time, as well as datetime abstractions for ease of use. The overall goal is to improve datetime manipulations, with a little bit of software and philsophy.

Pretty much make you a badass time traveller.

Getting Started
^^^^^^^^^^^^^^^

Here is the world without a flux capacitor at your side:

.. code-block:: python

    from datetime import datetime
    from pytz import timezone

    EST = "US/Eastern"
    UTC = "UTC"

    d = datetime.utcnow()
    utc = timezone(UTC)
    est = timezone(EST)
    d = utc.localize(d)
    d = est.normalize(EST)
    return d

Now lets warm up the `delorean`:

.. code-block:: python

    from delorean import Delorean

    EST = "US/Eastern"

    d = Delorean(timezone=EST)
    return d

Look at you looking all fly. This was just a test drive: check out out what else
`delorean` can help with below.
