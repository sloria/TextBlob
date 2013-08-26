.. _quickstart:

Tutorial: Quickstart
====================

TextBlob aims to provide access to common text-processing operations through a familiar interface. You can treat ``TextBlob`` objects as if they were Python strings that learned how to do Natural Language Processing.


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

Part-of-speech tags can be accessed through the ``tags`` property.

.. doctest::

    >>> wiki.tags
    [(u'Python', u'NNP'), (u'is', u'VBZ'), (u'a', u'DT'), (u'high-level', u'NN'), (u'general-purpose', u'JJ'), (u'programming', u'NN'), (u'language', u'NN')]

Noun Phrase Extraction
----------------------

Similarly, noun phrases are accessed through the ``noun_phrases`` property.

.. doctest::

    >>> wiki.noun_phrases
    WordList([u'python'])

Sentiment Analysis
------------------

The ``sentiment`` property returns the a tuple of the form ``(polarity, subjectivity)``. The polarity score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.

.. doctest::

    >>> testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
    >>> testimonial.sentiment
    (0.39166666666666666, 0.4357142857142857)

You can also access the scores from the ``blob.polarity`` and ``blob.subjectivity`` properties.


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

Spelling Correction
-------------------

Use the ``correct()`` method to attempt spelling correction.

.. doctest::

    >>> b = TextBlob("I havv goood speling!")
    >>> print(b.correct())
    I have good spelling!

``Word`` objects have a ``spellcheck()`` method that returns a list of ``(word, confidence)`` tuples with spelling suggestions.

.. doctest::

    >>> from text.blob import Word
    >>> w = Word('falibility')
    >>> w.spellcheck()
    [(u'fallibility', 1.0)]

Spelling correction is based on Peter Norvig's "How to Write a Spelling Corrector"[#]_ as implemented in the pattern library. It is about 70% accurate [#]_.


Get Word and Noun Phrase Frequencies
------------------------------------

There are two ways to get the frequency of a word or noun phrase in a ``TextBlob``.

The first is through the ``word_counts`` dictionary. ::

    >>> monty = TextBlob("We are no longer the Knights who say Ni. "
    ...                     "We are now the Knights who say Ekki ekki ekki PTANG.")
    >>> monty.word_counts['ekki']
    3

If you access the frequencies this way, the search will *not* be case sensitive, and words that are not found will have a frequency of 0.

The second way is to use the ``count()`` method. ::

    >>> monty.words.count('ekki')
    3

You can specify whether or not the search should be case-sensitive (default is ``False``). ::

    >>> monty.words.count('ekki', case_sensitive=True)
    2

Each of these methods can also be used with noun phrases. ::

    >>> wiki.noun_phrases.count('python')
    1

Translation and Language Detection
----------------------------------
New in version `0.5.0`.

TextBlobs can be translated between languages.

.. doctest::

    >>> en_blob = TextBlob(u"Simple is better than complex.")
    >>> en_blob.translate(to="es")
    TextBlob(u'Simple es mejor que complejo .')

The default source language is English. You can specify the source language explicitly, like so.

.. doctest::

    >>> chinese_blob = TextBlob(u"美丽优于丑陋")
    >>> chinese_blob.translate(from_lang="zh-CN", to='en')
    TextBlob(u'Beautiful is better than ugly')

You can also attempt to detect a TextBlob's language using ``TextBlob.detect_language()``.

.. doctest::

    >>> b = TextBlob(u"بسيط هو أفضل من مجمع")
    >>> b.detect_language()
    u'ar'

As a reference, language codes can be found `here <https://developers.google.com/translate/v2/using_rest#language-params>`_.

Language translation and detection is powered by the `Google Translate API`_.

.. _`Google Translate API`: https://developers.google.com/translate/

Parsing
-------

Use the ``parse()`` method to parse the text.

.. doctest::

    >>> b = TextBlob("And now for something completely different.")
    >>> b.parse()
    'And/CC/O/O now/RB/B-ADVP/O for/IN/B-PP/B-PNP something/NN/B-NP/I-PNP completely/RB/B-ADJP/O different/JJ/I-ADJP/O ././O/O'

By default, TextBlob uses pattern's parser [#]_.


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
    ---- Starts at index 31, Ends at index 64
    Simple is better than complex.
    ---- Starts at index 65, Ends at index 95


Dealing with HTML
-----------------

If your text comes in the form of an HTML string, you can pass ``clean_html=True`` to the TextBlob constructor to strip the markup.

.. doctest::

    >>> html = "<b>HAML</b> Ain't Markup <a href='/languages'>Language</a>"
    >>> clean = TextBlob(html, clean_html=True)
    >>> str(clean)
    "HAML Ain't Markup Language"

Get a JSON-serialized version of a blob
---------------------------------------

You can get a JSON representation of a blob with

.. doctest::

    >>> zen.json
    '[{"polarity": 0.2166666666666667, "stripped": "beautiful is better than ugly", "noun_phrases": ["beautiful"], "raw": "Beautiful is better than ugly.", "subjectivity": 0.8333333333333334, "end_index": 30, "start_index": 0}, {"polarity": 0.5, "stripped": "explicit is better than implicit", "noun_phrases": ["explicit"], "raw": "Explicit is better than implicit.", "subjectivity": 0.5, "end_index": 64, "start_index": 31}, {"polarity": 0.06666666666666667, "stripped": "simple is better than complex", "noun_phrases": ["simple"], "raw": "Simple is better than complex.", "subjectivity": 0.41904761904761906, "end_index": 95, "start_index": 65}]'

Next Steps
++++++++++

Want to build your own text classification system? Check out the :ref:`Classifiers Tutorial <classifiers>`.

Want to use a different POS tagger or noun phrase chunker implementation? Check out the :ref:`Advanced Usage <advanced>` guide.

.. [#]  http://norvig.com/spell-correct.html
.. [#]  http://www.clips.ua.ac.be/pages/pattern-en#spelling
.. [#]  http://www.clips.ua.ac.be/pages/pattern-en#parser
