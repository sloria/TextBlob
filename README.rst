TextBlob
========

.. image:: https://travis-ci.org/sloria/TextBlob.png

Simplified text processing for Python 2 and 3.


Requirements
------------

- Python 2.6, 2.7, or 3.3


Usage
-----

Simple.

Create a TextBlob
+++++++++++++++++

.. code-block:: python

    from text.blob import TextBlob

    zen = """Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    """

    blob = TextBlob(zen) # Create a new TextBlob

Part-of-speech tags and noun phrases...
+++++++++++++++++++++++++++++++++++++++

\...are just properties.

.. code-block:: python

    blob.pos_tags         # [('beautiful', 'JJ'), ('is', 'VBZ'), ('better', 'RBR'),
                          # ('than', 'IN'), ('ugly', 'RB'), ...]

    blob.noun_phrases     # ['beautiful', 'explicit', 'simple', 'complex', 'flat',
                          # 'sparse', 'readability', 'special cases',
                          # 'practicality beats purity', 'errors', 'unless',
                          # 'obvious way','dutch', 'right now', 'bad idea',
                          # 'good idea', 'namespaces', 'great idea']

Sentiment analysis
++++++++++++++++++

The :code:`sentiment` property returns a tuple of the form :code:`(polarity, subjectivity)` where :code:`polarity` ranges from -1.0 to 1.0 and
:code:`subjectivity` ranges from 0.0 to 1.0.

.. code-block:: python

    blob.sentiment        # (0.20, 0.58)

Tokenization
++++++++++++

.. code-block:: python

    blob.words            # WordList(['Beautiful', 'is', 'better'...'more',
                          #           'of', 'those'])

    blob.sentences        # [Sentence('Beautiful is better than ugly.'),
                          #  Sentence('Explicit is better than implicit.'),
                          #  ...]

Get word and noun phrase frequencies
++++++++++++++++++++++++++++++++++++

.. code-block:: python

    blob.word_counts['special']   # 2 (not case-sensitive by default)
    blob.words.count('special')   # Same thing
    blob.words.count('special', case_sensitive=True)  # 1

    blob.noun_phrases.count('great idea')  # 1

TextBlobs are like Python strings!
++++++++++++++++++++++++++++++++++

.. code-block:: python

    blob[0:19]            # TextBlob("Beautiful is better")
    blob.upper()          # TextBlob("BEAUTIFUL IS BETTER THAN UGLY...")
    blob.find("purity")   # 293

    apple_blob = TextBlob('apples')
    banana_blob = TextBlob('bananas')
    apple_blob < banana_blob           # True
    apple_blob + ' and ' + banana_blob # TextBlob('apples and bananas')
    "{0} and {1}".format(apple_blob, banana_blob)  # 'apples and bananas'


Get start and end indices of sentences
++++++++++++++++++++++++++++++++++++++

Use :code:`sentence.start` and :code:`sentence.end`. This can be useful for sentence highlighting, for example.

.. code-block:: python

    for sentence in blob.sentences:
        print(sentence)  # Beautiful is better than ugly
        print("---- Starts at index {}, Ends at index {}"\
                    .format(sentence.start, sentence.end))  # 0, 30

Get a JSON-serialized version of the blob
+++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    blob.json   # '[{"sentiment": [0.2166666666666667, ' '0.8333333333333334],
                # "stripped": "beautiful is better than ugly", '
                # '"noun_phrases": ["beautiful"], "raw": "Beautiful is better than ugly. ", '
                # '"end_index": 30, "start_index": 0}
                #  ...]'


Installation
------------

If you have :code:`pip`: ::

    pip install textblob

Or (if you must): ::

    easy_install textblob

**IMPORTANT**: TextBlob depends on some NLTK models to work. The easiest way
to get these is to run the :code:`download_corpora.py` script included with
this distribution. You can get it `here <https://raw.github.com/sloria/TextBlob/master/download_corpora.py>`_ .
Then run: ::

    python download_corpora.py


Testing
-------
Run ::

    nosetests

to run all tests.

License
-------

TextBlob is licenced under the MIT license. See the bundled `LICENSE <https://github.com/sloria/TextBlob/blob/master/LICENSE>`_ file for more details.
