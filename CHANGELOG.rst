Changelog
=========

0.13.1 (2017-11-11)
-------------------

Bug fixes:

- Avoid AttributeError when using pattern's sentiment analyzer
  (:issue:`178`). Thanks :user:`tylerjharden` for the catch and patch.
- Correctly pass ``format`` argument to ``NLTKClassifier.accuracy``
  (:issue:`177`). Thanks :user:`pavelmalai` for the catch and patch.

0.13.0 (2017-08-15)
-------------------

Features:

- Performance improvements to `NaiveBayesClassifier` (:issue:`63`, :issue:`77`,
  :issue:`123`). Thanks :user:`jcalbert` for the PR.

0.12.0 (2017-02-27)
-------------------

Features:

- Add `Word.stem` and `WordList.stem` methods (:issue:`145`). Thanks :user:`nitkul`.

Bug fixes:

- Fix translation and language detection (:issue:`137`). Thanks :user:`EpicJhon` for the fix.

Changes:

- *Backwards-incompatible*: Remove Python 2.6 and 3.3 support.

0.11.1 (2016-02-17)
-------------------

Bug fixes:

- Fix translation and language detection (:issue:`115`, :issue:`117`, :issue:`119`). Thanks :user:`AdrianLC` and :user:`jschnurr` for the fix. Thanks :user:`AdrianLC`, :user:`edgaralts`, and :user:`pouya-cognitiv` for reporting.

0.11.0 (2015-11-01)
-------------------

Changes:

- Compatible with nltk>=3.1. NLTK versions < 3.1 are no longer supported.
- Change default tagger to NLTKTagger (uses NLTK's averaged perceptron tagger).
- Tested on Python 3.5.

Bug fixes:

- Fix singularization of a number of words. Thanks :user:`jonmcoe`.
- Fix spelling correction when nltk>=3.1 is installed (:issue:`99`). Thanks :user:`shubham12101` for reporting.

0.10.0 (2015-10-04)
-------------------

Changes:

- Unchanged text is now considered a translation error. Raises ``NotTranslated`` (:issue:`76`). Thanks :user:`jschnurr`.

Bug fixes:

- ``Translator.translate`` will detect language of input text by default (:issue:`85`). Thanks again :user:`jschnurr`.
- Fix matching of tagged phrases with CFG in ``ConllExtractor``. Thanks :user:`lragnarsson`.
- Fix inflection of a few irregular English nouns. Thanks :user:`jonmcoe`.

0.9.1 (2015-06-10)
------------------

Bug fixes:

- Fix ``DecisionTreeClassifier.pprint`` for compatibility with nltk>=3.0.2.
- Translation no longer adds erroneous whitespace around punctuation characters (:issue:`83`). Thanks :user:`AdrianLC` for reporting and thanks :user:`jschnurr` for the patch.

0.9.0 (2014-09-15)
------------------

- TextBlob now depends on NLTK 3. The vendorized version of NLTK has been removed.
- Fix bug that raised a `SyntaxError` when translating text with non-ascii characters on Python 3.
- Fix bug that showed "double-escaped" unicode characters in translator output (issue #56). Thanks Evan Dempsey.
- *Backwards-incompatible*: Completely remove ``import text.blob``. You should ``import textblob`` instead.
- *Backwards-incompatible*: Completely remove ``PerceptronTagger``. Install ``textblob-aptagger`` instead.
- *Backwards-incompatible*: Rename ``TextBlobException`` to ``TextBlobError`` and ``MissingCorpusException`` to ``MissingCorpusError``.
- *Backwards-incompatible*: ``Format`` classes are passed a file object rather than a file path.
- *Backwards-incompatible*: If training a classifier with data from a file, you must pass a file object (rather than a file path).
- Updated English sentiment corpus.
- Add ``feature_extractor`` parameter to ``NaiveBayesAnalyzer``.
- Add ``textblob.formats.get_registry()`` and ``textblob.formats.register()`` which allows users to register custom data source formats.
- Change ``BaseClassifier.detect`` from a ``staticmethod`` to a ``classmethod``.
- Improved docs.
- Tested on Python 3.4.


0.8.4 (2014-02-02)
------------------
- Fix display (``__repr__``) of WordList slices on Python 3.
- Add download_corpora module. Corpora must now be downloaded using ``python -m textblob.download_corpora``.

0.8.3 (2013-12-29)
------------------
- Sentiment analyzers return namedtuples, e.g. ``Sentiment(polarity=0.12, subjectivity=0.34)``.
- Memory usage improvements to NaiveBayesAnalyzer and basic_extractor (default feature extractor for classifiers module).
- Add ``textblob.tokenizers.sent_tokenize`` and ``textblob.tokenizers.word_tokenize`` convenience functions.
- Add ``textblob.classifiers.MaxEntClassifer``.
- Improved NLTKTagger.

0.8.2 (2013-12-21)
------------------
- Fix bug in spelling correction that stripped some punctuation (Issue #48).
- Various improvements to spelling correction: preserves whitespace characters (Issue #12); handle contractions and punctuation between words. Thanks @davidnk.
- Make ``TextBlob.words`` more memory-efficient.
- Translator now sends POST instead of GET requests. This allows for larger bodies of text to be translated (Issue #49).
- Update pattern tagger for better accuracy.

0.8.1 (2013-11-16)
------------------
- Fix bug that caused ``ValueError`` upon sentence tokenization. This removes modifications made to the NLTK sentence tokenizer.
- Add ``Word.lemmatize()`` method that allows passing in a part-of-speech argument.
- ``Word.lemma`` returns correct part of speech for Word objects that have their ``pos`` attribute set. Thanks @RomanYankovsky.


0.8.0 (2013-10-23)
------------------
- *Backwards-incompatible*: Renamed package to ``textblob``. This avoids clashes with other namespaces called `text`. TextBlob should now be imported with ``from textblob import TextBlob``.
- Update pattern resources for improved parser accuracy.
- Update NLTK.
- Allow Translator to connect to proxy server.
- PerceptronTagger completely deprecated. Install the ``textblob-aptagger`` extension instead.

0.7.1 (2013-09-30)
------------------
- Bugfix updates.
- Fix bug in feature extraction for ``NaiveBayesClassifier``.
- ``basic_extractor`` is now case-sensitive, e.g. contains(I) != contains(i)
- Fix ``repr`` output when a TextBlob contains non-ascii characters.
- Fix part-of-speech tagging with ``PatternTagger`` on Windows.
- Suppress warning about not having scikit-learn installed.

0.7.0 (2013-09-25)
------------------
- Wordnet integration. ``Word`` objects have ``synsets`` and ``definitions`` properties. The ``text.wordnet`` module allows you to create ``Synset`` and ``Lemma`` objects directly.
- Move all English-specific code to its own module, ``text.en``.
- Basic extensions framework in place. TextBlob has been refactored to make it easier to develop extensions.
- Add ``text.classifiers.PositiveNaiveBayesClassifier``.
- Update NLTK.
- ``NLTKTagger`` now working on Python 3.
- Fix ``__str__`` behavior. ``print(blob)`` should now print non-ascii text correctly in both Python 2 and 3.
- *Backwards-incompatible*: All abstract base classes have been moved to the ``text.base`` module.
- *Backwards-incompatible*: ``PerceptronTagger`` will now be maintained as an extension, ``textblob-aptagger``. Instantiating a ``text.taggers.PerceptronTagger()`` will raise a ``DeprecationWarning``.

0.6.3 (2013-09-15)
------------------
- Word tokenization fix: Words that stem from a contraction will still have an apostrophe, e.g. ``"Let's" => ["Let", "'s"]``.
- Fix bug with comparing blobs to strings.
- Add ``text.taggers.PerceptronTagger``, a fast and accurate POS tagger. Thanks `@syllog1sm <http://github.com/syllog1sm>`_.
- Note for Python 3 users: You may need to update your corpora, since NLTK master has reorganized its corpus system. Just run ``curl https://raw.github.com/sloria/TextBlob/master/download_corpora.py | python`` again.
- Add ``download_corpora_lite.py`` script for getting the minimum corpora requirements for TextBlob's basic features.

0.6.2 (2013-09-05)
------------------
- Fix bug that resulted in a ``UnicodeEncodeError`` when tagging text with non-ascii characters.
- Add ``DecisionTreeClassifier``.
- Add ``labels()`` and ``train()`` methods to classifiers.

0.6.1 (2013-09-01)
------------------
- Classifiers can be trained and tested on CSV, JSON, or TSV data.
- Add basic WordNet lemmatization via the ``Word.lemma`` property.
- ``WordList.pluralize()`` and ``WordList.singularize()`` methods return ``WordList`` objects.

0.6.0 (2013-08-25)
------------------
- Add Naive Bayes classification. New ``text.classifiers`` module, ``TextBlob.classify()``, and ``Sentence.classify()`` methods.
- Add parsing functionality via the ``TextBlob.parse()`` method. The ``text.parsers`` module currently has one implementation (``PatternParser``).
- Add spelling correction. This includes the ``TextBlob.correct()`` and ``Word.spellcheck()`` methods.
- Update NLTK.
- Backwards incompatible: ``clean_html`` has been deprecated, just as it has in NLTK. Use Beautiful Soup's ``soup.get_text()`` method for HTML-cleaning instead.
- Slight API change to language translation: if ``from_lang`` isn't specified, attempts to detect the language.
- Add ``itokenize()`` method to tokenizers that returns a generator instead of a list of tokens.

0.5.3 (2013-08-21)
------------------
- Unicode fixes: This fixes a bug that sometimes raised a ``UnicodeEncodeError`` upon creating accessing ``sentences`` for TextBlobs with non-ascii characters.
- Update NLTK

0.5.2 (2013-08-14)
------------------
- `Important patch update for NLTK users`: Fix bug with importing TextBlob if local NLTK is installed.
- Fix bug with computing start and end indices of sentences.


0.5.1 (2013-08-13)
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
- New home for documentation: https://textblob.readthedocs.io/
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
