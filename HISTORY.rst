Changelog for textblob
======================

0.3.8 (2013-07-29)
------------------

- Fix bug with POS-tagger not tagging one-letter words.
- NPExtractor and Tagger objects can be passed to TextBlob's constructor.

0.3.7 (2013-07-28)
------------------

- Every word in a ``Blob`` or ``Sentence`` is a ``Word`` instance which has methods for inflection, e.g ``word.pluralize()`` and ``word.singularize()``.

- Updated the ``np_extractor`` module. Now has an new implementation, ``ConllExtractor`` that uses the Conll2000 chunking corpus. Only works on Py2.