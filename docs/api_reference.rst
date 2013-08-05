.. _api:

API Reference
=============

Blob Classes
------------
.. module:: text.blob

These include the :class:`TextBlob <TextBlob>` and :class:`Sentence <Sentence>`
classes, which both inherit from :class:`BaseBlob <BaseBlob>`.

.. autoclass:: BaseBlob
    :members:

.. autoclass:: TextBlob

.. autoclass:: Sentence

Lower-level classes
-------------------
.. autoclass:: Word
    :inherited-members:
    :members:

.. autoclass:: WordList
    :inherited-members:
    :members:

POS Taggers
-----------
.. module:: text.taggers

.. autoclass:: text.taggers.BaseTagger

.. autoclass:: text.taggers.PatternTagger
    :inherited-members:

.. autoclass:: text.taggers.NLTKTagger
    :inherited-members:

Noun Phrase Extractors
----------------------
.. module:: text.np_extractors

.. autoclass:: text.np_extractors.BaseNPExtractor
.. autoclass:: text.np_extractors.FastNPExtractor
.. autoclass:: text.np_extractors.ConllExtractor

Exceptions
----------
.. module:: text.exceptions

.. autoexception:: text.exceptions.MissingCorpusException




