.. textblob documentation master file, created by
   sphinx-quickstart on Mon Aug  5 01:41:33 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TextBlob: Simplified Text Processing
====================================

Release v\ |version|. (:ref:`Changelog`)

*TextBlob* is a Python (2 and 3) library for processing textual data. It provides a simple API for diving into common natural language processing (NLP) tasks such as part-of-speech tagging, noun phrase extraction, sentiment analysis, classification, translation, and more.


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


TextBlob stands on the giant shoulders of `NLTK`_ and `pattern`_, and plays nicely with both.

Features
--------

- Noun phrase extraction
- Part-of-speech tagging
- Sentiment analysis
- Classification (Naive Bayes, Decision Tree)
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

Ready to dive in? Go on to the :ref:`Quickstart guide <quickstart>`.

Guide
=====

.. toctree::
   :maxdepth: 2

   license
   install
   quickstart
   classifiers
   advanced_usage
   extensions
   api_reference

Project info
============

.. toctree::
   :maxdepth: 1

   changelog
   authors
   contributing


.. _NLTK: http://www.nltk.org
.. _pattern: http://www.clips.ua.ac.be/pages/pattern-en
