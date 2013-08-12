Changelog
=========

0.5.1 (unreleased)
------------------
- Fix bug that disallowed display of non-ascii characters in the Python REPL.
- Backwards incompatible: Restore ``blob.json`` property for backwards compatibility with textblob<=0.3.10. Add a ``to_json()`` method that takes the same arguments as ``json.dumps``.
- Add ``WordList.append`` and ``WordList.extend`` methods that append Word objects.

0.5.0 (2013-08-10)
------------------
- Language translation and detection API!
- Add ``text.sentiments`` module. Contains the ``PatternAnalyzer`` (default implementation) as well as a ``NaiveBayesAnalyzer``.
- Part-of-speech tags can be accessed via ``TextBlob.tags`` or ``TextBlob.pos_tags``.
- Add ``polarity`` and ``subjectivity`` helper properties.

0.4.0 (2013-08-05)
------------------
- New ``text.tokenizers`` module with ``WordTokenizer`` and ``SentenceTokenizer``. Tokenizer instances (from either textblob itself or NLTK) can be passed to TextBlob's constructor. Tokens are accessed through the new ``tokens`` property.
- New ``Blobber`` class for creating TextBlobs that share the same tagger, tokenizer, and np_extractor.
- Add ``ngrams`` method.
- `Backwards-incompatible`: ``TextBlob.json()`` is now a method, not a property. This allows you to pass arguments (the same that you would pass to ``json.dumps()``).
- New home for documentation: https://textblob.readthedocs.org/
- Add parameter for cleaning HTML markup from text.
- Minor improvement to word tokenization.
- Updated NLTK.
- Fix bug with adding blobs to bytestrings.

0.3.10 (2013-08-02)
-------------------
- Bundled NLTK no longer overrides local installation.
- Fix sentiment analysis of text with non-ascii characters.

0.3.9 (2013-07-31)
------------------
- Updated nltk.
- ConllExtractor is now Python 3-compatible.
- Improved sentiment analysis.
- Blobs are equal (with `==`) to their string counterparts.
- Added instructions to install textblob without nltk bundled.
- Dropping official 3.1 and 3.2 support.

0.3.8 (2013-07-30)
------------------
- Importing TextBlob is now **much faster**. This is because the noun phrase parsers are trained only on the first call to ``noun_phrases`` (instead of training them every time you import TextBlob).
- Add text.taggers module which allows user to change which POS tagger implementation to use. Currently supports PatternTagger and NLTKTagger (NLTKTagger only works with Python 2).
- NPExtractor and Tagger objects can be passed to TextBlob's constructor.
- Fix bug with POS-tagger not tagging one-letter words.
- Rename text/np_extractor.py -> text/np_extractors.py
- Add run_tests.py script.

0.3.7 (2013-07-28)
------------------

- Every word in a ``Blob`` or ``Sentence`` is a ``Word`` instance which has methods for inflection, e.g ``word.pluralize()`` and ``word.singularize()``.

- Updated the ``np_extractor`` module. Now has an new implementation, ``ConllExtractor`` that uses the Conll2000 chunking corpus. Only works on Py2.