.. _quickstart:

Tutorial: Quickstart
====================

.. module:: textblob.blob

TextBlob aims to provide access to common text-processing operations through a familiar interface. You can treat :class:`TextBlob <TextBlob>` objects as if they were Python strings that learned how to do Natural Language Processing.

Create a TextBlob
-----------------

First, the import.

.. doctest::

    >>> from textblob import TextBlob

Let's create our first :class:`TextBlob <TextBlob>`.

.. doctest::

    >>> wiki = TextBlob("Python is a high-level, general-purpose programming language.")

Part-of-speech Tagging
----------------------

Part-of-speech tags can be accessed through the :meth:`tags <TextBlob.tags>` property.

.. doctest::

    >>> wiki.tags
    [('Python', 'NNP'), ('is', 'VBZ'), ('a', 'DT'), ('high-level', 'JJ'), ('general-purpose', 'JJ'), ('programming', 'NN'), ('language', 'NN')]

Noun Phrase Extraction
----------------------

Similarly, noun phrases are accessed through the :meth:`noun_phrases <TextBlob.noun_phrases>` property.

.. doctest::

    >>> wiki.noun_phrases
    WordList(['python'])

Sentiment Analysis
------------------

The :meth:`sentiment <TextBlob.sentiment>` property returns a namedtuple of the form ``Sentiment(polarity, subjectivity)``. The polarity score is a float within the range [-1.0, 1.0]. The subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective.

.. doctest::

    >>> testimonial = TextBlob("Textblob is amazingly simple to use. What great fun!")
    >>> testimonial.sentiment
    Sentiment(polarity=0.39166666666666666, subjectivity=0.4357142857142857)
    >>> testimonial.sentiment.polarity
    0.39166666666666666


Tokenization
------------

You can break TextBlobs into words or sentences.

.. doctest::

    >>> zen = TextBlob("Beautiful is better than ugly. "
    ...                "Explicit is better than implicit. "
    ...                "Simple is better than complex.")
    >>> zen.words
    WordList(['Beautiful', 'is', 'better', 'than', 'ugly', 'Explicit', 'is', 'better', 'than', 'implicit', 'Simple', 'is', 'better', 'than', 'complex'])
    >>> zen.sentences
    [Sentence("Beautiful is better than ugly."), Sentence("Explicit is better than implicit."), Sentence("Simple is better than complex.")]

:class:`Sentence <Sentence>` objects have the same properties and methods as TextBlobs.

::

    >>> for sentence in zen.sentences:
    ...     print(sentence.sentiment)

For more advanced tokenization, see the :ref:`Advanced Usage <advanced>` guide.


Words Inflection and Lemmatization
----------------------------------

Each word in :meth:`TextBlob.words <TextBlob.words>` or :meth:`Sentence.words <Sentence.words>` is a :class:`Word <Word>`
object (a subclass of ``unicode``) with useful methods, e.g. for word inflection.

.. doctest::

    >>> sentence = TextBlob('Use 4 spaces per indentation level.')
    >>> sentence.words
    WordList(['Use', '4', 'spaces', 'per', 'indentation', 'level'])
    >>> sentence.words[2].singularize()
    'space'
    >>> sentence.words[-1].pluralize()
    'levels'

Words can be lemmatized by calling the :meth:`lemmatize <Word.lemmatize>` method.

.. doctest::

    >>> from textblob import Word
    >>> w = Word("octopi")
    >>> w.lemmatize()
    'octopus'
    >>> w = Word("went")
    >>> w.lemmatize("v")  # Pass in part of speech (verb)
    'go'

WordNet Integration
-------------------

You can access the synsets for a :class:`Word <Word>` via the :meth:`synsets <Word.synsets>` property or the :meth:`get_synsets <Word.get_synsets>` method, optionally passing in a part of speech.

.. doctest::

    >>> from textblob import Word
    >>> from textblob.wordnet import VERB
    >>> word = Word("octopus")
    >>> word.synsets
    [Synset('octopus.n.01'), Synset('octopus.n.02')]
    >>> Word("hack").get_synsets(pos=VERB)
    [Synset('chop.v.05'), Synset('hack.v.02'), Synset('hack.v.03'), Synset('hack.v.04'), Synset('hack.v.05'), Synset('hack.v.06'), Synset('hack.v.07'), Synset('hack.v.08')]

You can access the definitions for each synset via the :meth:`definitions <Word.definitions>` property or the :meth:`define() <Word.define>` method, which can also take an optional part-of-speech argument.

.. doctest::

    >>> Word("octopus").definitions
    ['tentacles of octopus prepared as food', 'bottom-living cephalopod having a soft oval body with eight long tentacles']

You can also create synsets directly.

.. doctest::

    >>> from textblob.wordnet import Synset
    >>> octopus = Synset('octopus.n.02')
    >>> shrimp = Synset('shrimp.n.03')
    >>> octopus.path_similarity(shrimp)
    0.1111111111111111

For more information on the WordNet API, see the NLTK documentation on the `Wordnet Interface <http://nltk.googlecode.com/svn/trunk/doc/howto/wordnet.html>`_.

WordLists
---------

A :class:`WordList <textblob.WordList>` is just a Python list with additional methods.

.. doctest::

    >>> animals = TextBlob("cat dog octopus")
    >>> animals.words
    WordList(['cat', 'dog', 'octopus'])
    >>> animals.words.pluralize()
    WordList(['cats', 'dogs', 'octopodes'])

Spelling Correction
-------------------

Use the :meth:`correct() <TextBlob.correct>` method to attempt spelling correction.

.. doctest::

    >>> b = TextBlob("I havv goood speling!")
    >>> print(b.correct())
    I have good spelling!

:class:`Word <Word>` objects have a :meth:`spellcheck() Word.spellcheck` method that returns a list of ``(word, confidence)`` tuples with spelling suggestions.

.. doctest::

    >>> from textblob import Word
    >>> w = Word('falibility')
    >>> w.spellcheck()
    [('fallibility', 1.0)]

Spelling correction is based on Peter Norvig's "How to Write a Spelling Corrector"[#]_ as implemented in the pattern library. It is about 70% accurate [#]_.


Get Word and Noun Phrase Frequencies
------------------------------------

There are two ways to get the frequency of a word or noun phrase in a :class:`TextBlob <TextBlob>`.

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
    TextBlob("Simple es mejor que complejo .")

If no source language is specified, TextBlob will attempt to detect the language. You can specify the source language explicitly, like so.

.. doctest::

    >>> chinese_blob = TextBlob(u"美丽优于丑陋")
    >>> chinese_blob.translate(from_lang="zh-CN", to='en')
    TextBlob("Beautiful is better than ugly")

You can also attempt to detect a TextBlob's language using :meth:`TextBlob.detect_language() <TextBlob.detect_language>`.

.. doctest::

    >>> b = TextBlob(u"بسيط هو أفضل من مجمع")
    >>> b.detect_language()
    'ar'

As a reference, language codes can be found `here <https://developers.google.com/translate/v2/using_rest#language-params>`_.

Language translation and detection is powered by the `Google Translate API`_.

.. _`Google Translate API`: https://developers.google.com/translate/

Parsing
-------

Use the :meth:`parse() <TextBlob.parse>` method to parse the text.

.. doctest::

    >>> b = TextBlob("And now for something completely different.")
    >>> print(b.parse())
    And/CC/O/O now/RB/B-ADVP/O for/IN/B-PP/B-PNP something/NN/B-NP/I-PNP completely/RB/B-ADJP/O different/JJ/I-ADJP/O ././O/O

By default, TextBlob uses pattern's parser [#]_.


TextBlobs Are Like Python Strings!
----------------------------------

You can use Python's substring syntax.

.. doctest::

    >>> zen[0:19]
    TextBlob("Beautiful is better")

You can use common string methods.

.. doctest::

    >>> zen.upper()
    TextBlob("BEAUTIFUL IS BETTER THAN UGLY. EXPLICIT IS BETTER THAN IMPLICIT. SIMPLE IS BETTER THAN COMPLEX.")
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
    TextBlob("apples and bananas")
    >>> "{0} and {1}".format(apple_blob, banana_blob)
    'apples and bananas'

`n`-grams
---------

The :class:`TextBlob.ngrams() <TextBlob.ngrams>` method returns a list of tuples of `n` successive words.

.. doctest::

    >>> blob = TextBlob("Now is better than never.")
    >>> blob.ngrams(n=3)
    [WordList(['Now', 'is', 'better']), WordList(['is', 'better', 'than']), WordList(['better', 'than', 'never'])]


Get Start and End Indices of Sentences
--------------------------------------

Use ``sentence.start`` and ``sentence.end`` to get the indices where a sentence starts and ends within a :class:`TextBlob <TextBlob>`.

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

Next Steps
++++++++++

Want to build your own text classification system? Check out the :ref:`Classifiers Tutorial <classifiers>`.

Want to use a different POS tagger or noun phrase chunker implementation? Check out the :ref:`Advanced Usage <advanced>` guide.

.. [#]  http://norvig.com/spell-correct.html
.. [#]  http://www.clips.ua.ac.be/pages/pattern-en#spelling
.. [#]  http://www.clips.ua.ac.be/pages/pattern-en#parser
