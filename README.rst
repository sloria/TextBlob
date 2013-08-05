
TextBlob: Pythonic Text Processing
==================================

.. image:: https://travis-ci.org/sloria/TextBlob.png
    :target: https://travis-ci.org/sloria/TextBlob
    :alt: Travis-CI

.. image:: https://pypip.in/d/textblob/badge.png
    :target: https://crate.io/packages/textblob/
    :alt: Number of PyPI downloads


Homepage: `https://textblob.readthedocs.org/ <https://textblob.readthedocs.org/>`_

`TextBlob` is a Python (2 and 3) library for processing textual data. It provides a consistent API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, and more.


.. code-block:: python

    from text.blob import TextBlob

    text = '''
    The titular threat of The Blob has always struck me as the ultimate movie
    monster: an insatiably hungry, amoeba-like mass able to penetrate
    virtually any safeguard, capable of--as a doomed doctor chillingly
    describes it--"assimilating flesh on contact.
    Snide comparisons to gelatin be damned, it's a concept with the most
    devastating of potential consequences, not unlike the grey goo scenario
    proposed by technological theorists fearful of
    artificial intelligence run rampant.
    '''

    blob = TextBlob(text)
    blob.pos_tags       # [(Word('The'), u'DT'), (Word('titular'), u'JJ'),
                        #  (Word('threat'), u'NN'), ...])
    blob.noun_phrases   # WordList(['titular threat', 'blob',
                        #            'ultimate movie monster',
                        #            'amoeba-like mass', ...])

    for sentence in blob.sentences:
        print(blob.sentiment)
    # (0.060, 0.605)
    # (-0.34, 0.77)

Get it now
----------
::

    $ pip install -U textblob
    $ curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python


Documentation
-------------

Hosted `here <https://textblob.readthedocs.org/>`_ at ReadTheDocs.

Requirements
------------

- Python >= 2.6 or >= 3.3


Testing
-------
Run ::

    python run_tests.py

to run all tests.

License
-------

TextBlob is licenced under the MIT license. See the bundled `LICENSE <https://github.com/sloria/TextBlob/blob/master/LICENSE>`_ file for more details.

.. _pattern: http://www.clips.ua.ac.be/pattern
.. _NLTK: http://nltk.org/