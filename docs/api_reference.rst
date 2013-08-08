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

Tokenizers
----------
New in `0.4.0`.

.. automodule:: text.tokenizers
    :members:

POS Taggers
-----------

.. automodule:: text.taggers
    :members:

Noun Phrase Extractors
----------------------

.. automodule:: text.np_extractors
    :members: BaseNPExtractor, ConllExtractor, FastNPExtractor

Sentiment Analyzers
-------------------

New in `0.5.0`.

.. automodule:: text.sentiments
    :members:

Blobber
-------
New in `0.4.0`.

.. autoclass:: text.blob.Blobber
    :members:
    :special-members:
    :exclude-members: __weakref__

Exceptions
----------
.. module:: text.exceptions

.. autoexception:: text.exceptions.MissingCorpusException




