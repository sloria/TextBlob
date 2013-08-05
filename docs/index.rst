.. textblob documentation master file, created by
   sphinx-quickstart on Mon Aug  5 01:41:33 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

TextBlob: Simplified Text Processing
====================================

Release v\ |version|. (:ref:`Installation <install>`)

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
    # (sentiment score, subjectivity score)
    # (0.060, 0.605)
    # (-0.34, 0.77)

Get it now
----------
::

    $ pip install -U textblob
    $ curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python

Ready to dive in? Go on to the :ref:`Quickstart guide <quickstart>`.


Guide
=====

.. toctree::
   :maxdepth: 2

   license
   install
   quickstart
   advanced_usage
   api_reference

.. _NLTK: http://www.nltk.org
.. _pattern: http://www.clips.ua.ac.be/pages/pattern-en