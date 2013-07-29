TextBlob
========

.. image:: https://travis-ci.org/sloria/TextBlob.png
    :target: https://travis-ci.org/sloria/TextBlob
    :alt: Travis-CI

.. image:: https://pypip.in/d/textblob/badge.png
    :target: https://crate.io/packages/textblob/
    :alt: Number of PyPI downloads

Simplified text processing for Python 2 and 3.


Requirements
------------

- Python >= 2.6 or >= 3.1


Installation
------------

TextBlob's only external dependency is PyYAML. A vendorized version of NLTK is bundled internally.

If you have ``pip``: ::

    pip install textblob

Or (if you must): ::

    easy_install textblob

**IMPORTANT**: TextBlob depends on some NLTK corpora to work. The easiest way
to get these is to run this command: ::

    curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python

You can also download the script `here <https://raw.github.com/sloria/TextBlob/master/download_corpora.py>`_ .
Then run: ::

    python download_corpora.py



Usage
-----

Simple.

Create a TextBlob
+++++++++++++++++

.. code-block:: python

    from text.blob import TextBlob

    wikitext = '''
    Python is a widely used general-purpose, high-level programming language.
    Its design philosophy emphasizes code readability, and its syntax allows
    programmers to express concepts in fewer lines of code than would be
    possible in languages such as C.
    '''

    wiki = TextBlob(wikitext)

Part-of-speech tags and noun phrases...
+++++++++++++++++++++++++++++++++++++++

\...are just properties.

.. code-block:: python

    wiki.pos_tags       # [(Word('Python'), 'NNP'), (Word('is'), 'VBZ'),
                        #  (Word('widely'), 'RB')...]

    wiki.noun_phrases   # WordList(['python', 'design philosophy',  'code readability'])

Sentiment analysis
++++++++++++++++++

The ``sentiment`` property returns a tuple of the form ``(polarity, subjectivity)`` where ``polarity`` ranges from -1.0 to 1.0 and
``subjectivity`` ranges from 0.0 to 1.0.

.. code-block:: python

    blob.sentiment        # (0.20, 0.58)

Tokenization
++++++++++++

.. code-block:: python

    zen = TextBlob("Beautiful is better than ugly. "
                    "Explicit is better than implicit. "
                    "Simple is better than complex.")

    zen.words            # WordList(['Beautiful', 'is', 'better'...])

    zen.sentences        # [Sentence('Beautiful is better than ugly.'),
                          #  Sentence('Explicit is better than implicit.'),
                          #  ...]

Words and inflection
++++++++++++++++++++

Each word in ``TextBlob.words`` or ``Sentence.words`` is a ``Word``
object (a subclass of ``unicode``) with useful methods, e.g. for word inflection.

.. code-block:: python

    sentence = TextBlob('Use 4 spaces per indentation level.')
    sentence.words
    # OUT: WordList(['Use', '4', 'spaces', 'per', 'indentation', 'level'])
    sentence.words[2].singularize()
    # OUT: 'space'
    sentence.words[-1].pluralize()
    # OUT: 'levels'

Get word and noun phrase frequencies
++++++++++++++++++++++++++++++++++++

.. code-block:: python

    wiki.word_counts['its']   # 2 (not case-sensitive by default)
    wiki.words.count('its')   # Same thing
    wiki.words.count('its', case_sensitive=True)  # 1

    wiki.noun_phrases.count('code readability')  # 1

TextBlobs are like Python strings!
++++++++++++++++++++++++++++++++++

.. code-block:: python

    zen[0:19]            # TextBlob("Beautiful is better")
    zen.upper()          # TextBlob("BEAUTIFUL IS BETTER THAN UGLY...")
    zen.find("Simple")   # 65

    apple_blob = TextBlob('apples')
    banana_blob = TextBlob('bananas')
    apple_blob < banana_blob           # True
    apple_blob + ' and ' + banana_blob # TextBlob('apples and bananas')
    "{0} and {1}".format(apple_blob, banana_blob)  # 'apples and bananas'


Get start and end indices of sentences
++++++++++++++++++++++++++++++++++++++

Use ``sentence.start`` and ``sentence.end``. This can be useful for sentence highlighting, for example.

.. code-block:: python

    for sentence in zen.sentences:
        print(sentence)  # Beautiful is better than ugly
        print("---- Starts at index {}, Ends at index {}"\
                    .format(sentence.start, sentence.end))  # 0, 30

Get a JSON-serialized version of the blob
+++++++++++++++++++++++++++++++++++++++++

.. code-block:: python

    zen.json   # '[{"sentiment": [0.2166666666666667, ' '0.8333333333333334],
                # "stripped": "beautiful is better than ugly", '
                # '"noun_phrases": ["beautiful"], "raw": "Beautiful is better than ugly. ", '
                # '"end_index": 30, "start_index": 0}
                #  ...]'

Overriding the noun phrase extractor
++++++++++++++++++++++++++++++++++++

TextBlob currently has two noun phrases chunker implementations,
``text.np_extractor.FastNPExtractor`` (default, based on Shlomi Babluki's implementation from
`this blog post <http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/>`_)
and ``text.np_extractor.ConllExtractor`` (currently working on Python 2 only).

You can change the chunker implementation (or even use your own) by overriding ``TextBlob.np_extractor``

.. code-block:: python

    from text.np_extractor import ConllExtractor
    extractor = ConllExtractor()
    blob = TextBlob("Python is a widely used general-purpose, high-level programming language.")
    blob.np_extractor = extractor
    blob.noun_phrases  # This will use the Conll2000 noun phrase extractor


Testing
-------
Run ::

    nosetests

to run all tests.

License
-------

TextBlob is licenced under the MIT license. See the bundled `LICENSE <https://github.com/sloria/TextBlob/blob/master/LICENSE>`_ file for more details.

.. _download_corpora.py:
