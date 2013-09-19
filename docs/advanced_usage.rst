.. _advanced:

Advanced Usage: Overriding Models and the Blobber Class
=======================================================

TextBlob allows you to specify which algorithms you want to use under the hood of its simple API.

Sentiment Analyzers
-------------------

New in version `0.5.0`.

The ``text.sentiments`` module contains two sentiment analysis implementations, ``PatternAnalyzer`` (based on the pattern_ library) and ``NaiveBayesAnalyzer`` (an NLTK_ classifier trained on a movie reviews corpus).

The default implementation is ``PatternAnalyzer``, but you can override the analyzer by passing another implementation into a TextBlob's constructor.

For instance, the ``NaiveBayesAnalyzer`` returns its result as a tuple of the form: ``(classification, pos_probability, neg_probability)``.

::

    >>> from text.blob import TextBlob
    >>> from text.sentiments import NaiveBayesAnalyzer
    >>> blob = TextBlob("I love this library", analyzer=NaiveBayesAnalyzer())
    >>> blob.sentiment
    ('pos', 0.7996209910191279, 0.2003790089808724)

Tokenizers
----------

New in version `0.4.0`.

The ``words`` and ``sentences`` properties are helpers that use the ``text.tokenizers.WordTokenizer`` and ``text.tokenizers.SentenceTokenizer`` classes, respectively.

You can use other tokenizers, such as those provided by NLTK, by passing them into the ``TextBlob`` constructor then accessing the ``tokens`` property.

::

    >>> from text.blob import TextBlob
    >>> from nltk.tokenize import TabTokenizer
    >>> tokenizer = TabTokenizer()
    >>> blob = TextBlob("This is\ta rather tabby\tblob.", tokenizer=tokenizer)
    >>> blob.tokens
    WordList(["This is", "a rather tabby", "blob."])

You can also use the ``tokenize([tokenizer])`` method.

::

    >>> from text.blob import TextBlob
    >>> from nltk.tokenize import BlanklineTokenizer
    >>> tokenizer = BlanklineTokenizer()
    >>> blob = TextBlob("A token\n\nof appreciation")
    >>> blob.tokenize(tokenizer)
    WordList([u'A token', u'of appreciation'])

Noun Phrase Chunkers
--------------------

TextBlob currently has two noun phrases chunker implementations,
``text.np_extractors.FastNPExtractor`` (default, based on Shlomi Babluki's implementation from
`this blog post <http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/>`_)
and ``text.np_extractors.ConllExtractor``, which uses the CoNLL 2000 corpus to train a tagger.

You can change the chunker implementation (or even use your own) by explicitly passing an instance of a noun phrase extractor to a TextBlob's constructor.

::

    >>> from text.blob import TextBlob
    >>> from text.np_extractors import ConllExtractor
    >>> extractor = ConllExtractor()
    >>> blob = TextBlob("Python is a high-level programming language.", np_extractor=extractor)
    >>> blob.noun_phrases
    WordList([u'python', u'high-level programming language'])

POS Taggers
-----------

TextBlob currently has three POS tagger implementations, located in ``text.taggers``. The default is the ``PatternTagger`` which uses the same implementation as the pattern_ library.

The second implementation is ``NLTKTagger`` which uses NLTK_'s TreeBank tagger. *It requires numpy and only works on Python 2*.

The third implementation is ``PerceptronTagger`` which is based on the Averaged Perceptron algorithm, as implemented by Matthew Honnibal. More information can be found here: `A Good Part of Speech Tagger in About 200 Lines of Python <http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/>`_. *This tagger requires the trontagger.pickle file*. See the :ref:`installation guide <install>` for instructions on obtaining the pickled model.

Similar to the tokenizers and noun phrase chunkers, you can explicitly specify which POS tagger to use by passing a tagger instance to the constructor.

::

    >>> from text.blob import TextBlob
    >>> from text.taggers import NLTKTagger
    >>> nltk_tagger = NLTKTagger()
    >>> blob = TextBlob("Tag! You're It!", pos_tagger=nltk_tagger)
    >>> blob.pos_tags
    [(Word('Tag'), u'NN'), (Word('You'), u'PRP'), (Word('''), u'VBZ'), (Word('re'), u'NN'), (Word('It')
    , u'PRP')]

.. _pattern: http://www.clips.ua.ac.be/pattern
.. _NLTK: http://nltk.org/

Parsers
-------

New in version `0.6.0`.

Parser implementations can also be passed to the TextBlob constructor.

::

    >>> from text.blob import TextBlob
    >>> from text.parsers import PatternParser
    >>> blob = TextBlob("Parsing is fun.", parser=PatternParser())
    >>> blob.parse()
    'Parsing/VBG/B-VP/O is/VBZ/I-VP/O fun/VBG/I-VP/O ././O/O'


Blobber: A TextBlob Factory
---------------------------

New in `0.4.0`.

It can be tedious to repeatedly pass taggers, NP extractors, sentiment analyzers, classifiers, and tokenizers to  multiple TextBlobs. To keep your code `DRY <https://en.wikipedia.org/wiki/DRY_principle>`_, you can use the ``Blobber`` class to create TextBlobs that share the same models.

First, instantiate a ``Blobber`` with the tagger, NP extractor, sentiment analyzer, classifier, and/or tokenizer of your choice.

.. doctest::

    >>> from text.blob import Blobber
    >>> from text.taggers import NLTKTagger
    >>> tb = Blobber(pos_tagger=NLTKTagger())

You can now create new TextBlobs like so:

.. doctest::

    >>> blob1 = tb("This is a blob.")
    >>> blob2 = tb("This is another blob.")
    >>> blob1.pos_tagger is blob2.pos_tagger
    True

