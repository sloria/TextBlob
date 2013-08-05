.. _advanced:

Advanced Usage
==============

TextBlob allows you to specify which algorithms you want to use under the hood of its simple API.

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

TextBlob currently has two POS tagger implementations, located in ``text.taggers``. The default is the ``PatternTagger`` which uses the same implementation as the excellent pattern_ library.

The second implementation is ``NLTKTagger`` which uses NLTK_'s TreeBank tagger. *It requires numpy and only works on Python 2*.

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
