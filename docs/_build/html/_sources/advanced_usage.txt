Advanced Usage
==============

In construction.

Noun Phrase Chunkers
--------------------

TextBlob currently has two noun phrases chunker implementations,
``text.np_extractors.FastNPExtractor`` (default, based on Shlomi Babluki's implementation from
`this blog post <http://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/>`_)
and ``text.np_extractors.ConllExtractor``, which uses the CoNLL 2000 corpus to train a tagger.

You can change the chunker implementation (or even use your own) by explicitly passing an instance of a noun phrase extractor to a TextBlob's constructor.

.. code-block:: python

    from text.blob import TextBlob
    from text.np_extractors import ConllExtractor

    extractor = ConllExtractor()
    blob = TextBlob("Extract my noun phrases.", np_extractor=extractor)
    blob.noun_phrases  # This will use the Conll2000 noun phrase extractor


POS Taggers
-----------

TextBlob currently has two POS tagger implementations, located in ``text.taggers``. The default is the ``PatternTagger`` which uses the same implementation as the excellent pattern_ library.

The second implementation is ``NLTKTagger`` which uses NLTK_'s TreeBank tagger. *It requires numpy and only works on Python 2*.

Similar to the noun phrase chunkers, you can explicitly specify which POS tagger to use by passing a tagger instance to the constructor.

.. code-block:: python

    from text.blob import TextBlob
    from text.taggers import NLTKTagger

    nltk_tagger = NLTKTagger()
    blob = TextBlob("Tag! You're It!", pos_tagger=nltk_tagger)
    blob.pos_tags

.. _pattern: http://www.clips.ua.ac.be/pattern
.. _NLTK: http://nltk.org/
