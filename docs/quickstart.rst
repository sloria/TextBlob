.. _quickstart:

Quickstart
==========

TextBlob aims to provide access to common text-processing operations through a familiar interface. You can treat ``TextBlob`` objects as if they were Python strings that learned how to do Natural Language Processing.

.. testsetup::

    from __future__ import unicode_literals

Create a TextBlob
-----------------

First, the import.

.. doctest::

    >>> from text.blob import TextBlob

Let's create our first ``TextBlob``.

.. doctest::

    >>> wiki = TextBlob("Python is a high-level, general-purpose programming language.")

Part-of-speech Tagging
----------------------

Part-of-speech tags can be accessed through the ``pos_tags`` property.

.. doctest::

    >>> wiki.pos_tags
    [(u'Python', u'NNP'), (u'is', u'VBZ'), (u'a', u'DT'), (u'high-level', u'NN'), (u'general-purpose', u'JJ'), (u'programming', u'NN'), (u'language', u'NN')]

Noun Phrase Extraction
----------------------

Similarly, noun phrases are accessed through the ``noun_phrases`` property.

.. doctest::

    >>> wiki.noun_phrases
    WordList([u'python'])

Sentiment Analysis
------------------

The ``sentiment`` property returns a tuple of the form ``(polarity, subjectivity)`` where ``polarity`` ranges from -1.0 to 1.0 and
``subjectivity`` ranges from 0.0 to 1.0.

.. doctest::

    >>> testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
    >>> testimonial.sentiment
    (0.39166666666666666, 0.4357142857142857)


Tokenization
------------

You can break TextBlobs into words or sentences.

.. doctest::

    >>> zen = TextBlob("Beautiful is better than ugly. "
    ...                "Explicit is better than implicit. "
    ...                "Simple is better than complex.")
    >>> zen.words
    WordList([u'Beautiful', u'is', u'better', u'than', u'ugly', u'Explicit', u'is', u'better', u'than', u'implicit', u'Simple', u'is', u'better', u'than', u'complex'])
    >>> zen.sentences
    [Sentence('Beautiful is better than ugly.'), Sentence('Explicit is better than implicit.'), Sentence('Simple is better than complex.')]

``Sentence`` objects have the same properties and methods as TextBlobs.

::

    >>> for sentence in zen.sentences:
    ...     print(sentence.sentiment)

For more advanced tokenization, see the :ref:`Advanced Usage <advanced>` guide.


Words and Inflection
--------------------

Each word in ``TextBlob.words`` or ``Sentence.words`` is a ``Word``
object (a subclass of ``unicode``) with useful methods, e.g. for word inflection.

.. doctest::

    >>> sentence = TextBlob('Use 4 spaces per indentation level.')
    >>> sentence.words
    WordList([u'Use', u'4', u'spaces', u'per', u'indentation', u'level'])
    >>> sentence.words[2].singularize()
    'space'
    >>> sentence.words[-1].pluralize()
    'levels'

WordLists
---------

Similarly, ``WordLists`` are just Python lists with additional methods.

.. doctest::

    >>> animals = TextBlob("cat dog octopus")
    >>> animals.words
    WordList([u'cat', u'dog', u'octopus'])
    >>> animals.words.pluralize()
    ['cats', 'dogs', 'octopodes']


Get Word and Noun Phrase Frequencies
------------------------------------

There are two ways to get the frequency of a word or noun phrase in a ``TextBlob``.

The first is through the ``word_counts`` dictionary. ::

    >>> wiki.word_counts['its']
    2

If you access the frequencies this way, the search will *not* be case sensitive, and words that are not found will have a frequency of 0.

The second way is to use the ``count(strg, [case_sensitive=False])`` method. ::

    >>> wiki.words.count('its')
    2

You can specify whether or not the search should be case-sensitive. ::

    >>> wiki.words.count('its', case_sensitive=True)
    1

Each of these methods can also be used with noun phrases. ::

    >>> wiki.noun_phrases.count('python')
    1

TextBlobs Are Like Python Strings!
----------------------------------

You can use Python's substring syntax.

.. doctest::

    >>> zen[0:19]
    TextBlob('Beautiful is better')

You can use common string methods.

.. doctest::

    >>> zen.upper()
    TextBlob('BEAUTIFUL IS BETTER THAN UGLY. EXPLICIT ...BETTER THAN COMPLEX.')
    >>> zen.find("Simple")
    65

You can make comparisons between TextBlobs and strings.

.. doctest::

    >>> apple_blob = TextBlob('apples')
    >>> banana_blob = TextBlob('bananas')
    >>> apple_blob < banana_blob
    True
    >>> apple_blob == 'apples'
    True

You can concatenate and interpolate TextBlobs and strings.

.. doctest::

    >>> apple_blob + ' and ' + banana_blob
    TextBlob('apples and bananas')
    >>> u"{0} and {1}".format(apple_blob, banana_blob)
    u'apples and bananas'

`n`-grams
---------

The ``TextBlob.ngrams()`` method returns a list of tuples of `n` successive words.

.. doctest::

    >>> blob = TextBlob("Now is better than never.")
    >>> blob.ngrams(n=3)
    [WordList([u'Now', u'is', u'better']), WordList([u'is', u'better', u'than']), WordList([u'better', u'than', u'never'])]



Get Start and End Indices of Sentences
--------------------------------------

Use ``sentence.start`` and ``sentence.end`` to get the indices where a sentence starts and ends within a ``TextBlob``.

.. doctest::

    >>> for s in zen.sentences:
    ...     print(s)
    ...     print("---- Starts at index {}, Ends at index {}".format(s.start, s.end))
    Beautiful is better than ugly.
    ---- Starts at index 0, Ends at index 30
    Explicit is better than implicit.
    ---- Starts at index 30, Ends at index 63
    Simple is better than complex.
    ---- Starts at index 63, Ends at index 93


Dealing with HTML
-----------------

If your text comes in the form of an HTML string, you can pass ``clean_html=True`` to the TextBlob constructor to strip the markup.

.. doctest::

    >>> html = "<b>HAML</b> Ain't Markup <a href='/languages'>Language</a>"
    >>> clean = TextBlob(html, clean_html=True)
    >>> print(clean.raw)
    HAML Ain't Markup Language

Get a JSON-serialized version of a blob
---------------------------------------

You can get a JSON representation of a blob with

.. doctest::

    >>> zen.json()
    '[{"sentiment": [0.2166666666666667, 0.8333333333333334], "stripped": "beautiful is better than ugly", "noun_phrases": ["beautiful"], "raw": "Beautiful is better than ugly.", "end_index": 30, "start_index": 0}, {"sentiment": [0.5, 0.5], "stripped": "explicit is better than implicit", "noun_phrases": ["explicit"], "raw": "Explicit is better than implicit.", "end_index": 63, "start_index": 30}, {"sentiment": [0.06666666666666667, 0.41904761904761906], "stripped": "simple is better than complex", "noun_phrases": ["simple"], "raw": "Simple is better than complex.", "end_index": 93, "start_index": 63}]'


Next Steps
++++++++++

Want to use a different POS tagger or noun phrase chunker implementation? Check out the :ref:`Advanced Usage <advanced>` guide.
