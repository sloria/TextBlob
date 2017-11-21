
TextBlob: Simplified Text Processing
====================================

.. image:: https://badge.fury.io/py/textblob.svg
    :target: http://badge.fury.io/py/textblob
    :alt: Latest version

.. image:: https://travis-ci.org/sloria/TextBlob.svg?branch=master
    :target: https://travis-ci.org/sloria/TextBlob
    :alt: Travis-CI

Homepage: `https://textblob.readthedocs.io/ <https://textblob.readthedocs.io/>`_

`TextBlob` is a Python (2 and 3) library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.


.. code-block:: python

    from textblob import TextBlob

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
    blob.tags           # [('The', 'DT'), ('titular', 'JJ'),
                        #  ('threat', 'NN'), ('of', 'IN'), ...]

    blob.noun_phrases   # WordList(['titular threat', 'blob',
                        #            'ultimate movie monster',
                        #            'amoeba-like mass', ...])

    for sentence in blob.sentences:
        print(sentence.sentiment.polarity)
    # 0.060
    # -0.341

    blob.translate(to="es")  # 'La amenaza titular de The Blob...'

TextBlob stands on the giant shoulders of `NLTK`_ and `pattern`_, and plays nicely with both.

Features
--------

- Noun phrase extraction
- Part-of-speech tagging
- Sentiment analysis
- Classification (Naive Bayes, Decision Tree)
- Language translation and detection powered by Google Translate
- Tokenization (splitting text into words and sentences)
- Word and phrase frequencies
- Parsing
- `n`-grams
- Word inflection (pluralization and singularization) and lemmatization
- Spelling correction
- Add new models or languages through extensions
- WordNet integration

Get it now
----------
::

    $ pip install -U textblob
    $ python -m textblob.download_corpora

Examples
--------

See more examples at the `Quickstart guide`_.

.. _`Quickstart guide`: https://textblob.readthedocs.io/en/latest/quickstart.html#quickstart


Documentation
-------------

Full documentation is available at https://textblob.readthedocs.io/.

Requirements
------------

- Python >= 2.7 or >= 3.4

Project Links
-------------

- Docs: https://textblob.readthedocs.io/
- Changelog: https://textblob.readthedocs.io/en/latest/changelog.html
- PyPI: https://pypi.python.org/pypi/TextBlob
- Issues: https://github.com/sloria/TextBlob/issues

License
-------

MIT licensed. See the bundled `LICENSE <https://github.com/sloria/TextBlob/blob/master/LICENSE>`_ file for more details.

.. _pattern: http://www.clips.ua.ac.be/pattern
.. _NLTK: http://nltk.org/
