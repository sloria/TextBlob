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
    :members:

.. autoclass:: Sentence
    :members:

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

.. automodule:: text.tokenizers
    :members:
    :inherited-members:

POS Taggers
-----------

.. automodule:: text.taggers
    :members:
    :inherited-members:

Noun Phrase Extractors
----------------------

.. automodule:: text.np_extractors
    :members: BaseNPExtractor, ConllExtractor, FastNPExtractor
    :inherited-members:


Sentiment Analyzers
-------------------

.. automodule:: text.sentiments
    :members:
    :inherited-members:


Parsers
-------

.. automodule:: text.parsers
    :members:
    :inherited-members:

.. _api_classifiers:

Classifiers
-----------

.. automodule:: text.classifiers
    :members:
    :inherited-members:

Blobber
-------

.. autoclass:: text.blob.Blobber
    :members:
    :special-members:
    :exclude-members: __weakref__

File Formats
------------

..automodule:: text.formats
    :members:
    :inherited-members:

Exceptions
----------
.. module:: text.exceptions

.. autoexception:: text.exceptions.MissingCorpusException




