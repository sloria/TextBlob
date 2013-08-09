# -*- coding: utf-8 -*-

'''Wrappers for various units of text.'''
import sys
import json
from collections import defaultdict

from .packages import nltk
from .decorators import cached_property
from .utils import lowerstrip, PUNCTUATION_REGEX
from .inflect import singularize as _singularize, pluralize as _pluralize
from .mixins import ComparableMixin
from .compat import string_types, unicode
from .np_extractors import BaseNPExtractor, FastNPExtractor
from .taggers import BaseTagger, PatternTagger
from .tokenizers import BaseTokenizer, WordTokenizer, SentenceTokenizer
from .sentiments import BaseSentimentAnalyzer, PatternAnalyzer
from .translate import Translator
from .exceptions import MissingCorpusException


class Word(unicode):

    '''A simple word representation.'''

    translator = Translator()

    def __new__(cls, string, pos_tag=None):
        '''Return a new instance of the class. It is necessary to override
        this method in order to handle the extra pos_tag argument in the
        constructor.
        '''
        return super(Word, cls).__new__(cls, string)

    def __init__(self, string, pos_tag=None):
        self.string = string
        self.pos_tag = pos_tag

    def __repr__(self):
        return repr(self.string)

    def __str__(self):
        return self.string

    def singularize(self):
        '''Return the singular version of the word as a string.'''
        return _singularize(self.string)

    def pluralize(self):
        '''Return the plural version of the word as a string.'''
        return _pluralize(self.string)

    def translate(self, from_lang="en", to="en"):
        '''Translate the word to another language using Google's
        Translate API.

        New in `0.5.0`.
        '''
        return self.translator.translate(self.string,
                                        from_lang=from_lang, to_lang=to)

    def detect_language(self):
        '''Detect the word's language using Google's Translate API.

        New in `0.5.0`.
        '''
        return self.translator.detect(self.string)


class WordList(list):

    '''A list-like collection of words.'''

    def __init__(self, collection):
        '''Initialize a WordList. Takes a collection of strings as
        its only argument.
        '''
        self._collection = [Word(w) for w in collection]
        super(WordList, self).__init__(self._collection)

    def __repr__(self):
        '''Returns a string representation for debugging.'''
        class_name = self.__class__.__name__
        # String representation of words
        strings = [unicode(w) for w in self._collection]
        if len(self) > 60:
            return '{cls}({beginning}...{end})'.format(cls=class_name,
                                                beginning=strings[:3],
                                                end=strings[-3:])
        else:
            return '{cls}({lst})'.format(cls=class_name, lst=strings)

    def __getitem__(self, key):
        '''Returns a string at the given index.'''
        if isinstance(key, slice):
            return self.__class__(self._collection[key])
        else:
            return self._collection[key]

    def __getslice__(self, i, j):
        # This is included for Python 2.* compatibility
        return self.__class__(self._collection[i:j])

    def count(self, strg, case_sensitive=False, *args, **kwargs):
        """Get the count of a word or phrase `s` within this WordList.

        Arguments:
        - s: The string to count.
        - case_sensitive: A boolean, whether or not the search is case-sensitive.
        """
        if not case_sensitive:
            return [word.lower() for word in self].count(strg.lower(), *args,
                    **kwargs)
        return self._collection.count(strg, *args, **kwargs)

    def upper(self):
        '''Return a new WordList with each word upper-cased.'''
        return self.__class__([word.upper() for word in self])

    def lower(self):
        '''Return a new WordList with each word lower-cased.'''
        return self.__class__([word.lower() for word in self])

    def singularize(self):
        '''Return the single version of each word in this WordList.'''
        return [word.singularize() for word in self]

    def pluralize(self):
        '''Return the plural version of each word in this WordList.'''
        return [word.pluralize() for word in self]


class BaseBlob(ComparableMixin):

    '''An abstract base class that all text.blob classes will inherit from.
    Includes words, POS tag, NP, and word count properties. Also includes
    basic dunder and string methods for making objects like Python strings.

    :param text: A string.
    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to :class:`WordTokenizer() <text.tokenizers.WordTokenizer>`.
    :param np_extractor: (optional) An NPExtractor instance. If ``None``, defaults to :class:`FastNPExtractor() <text.np_extractors.FastNPExtractor>`.
    :param pos_tagger: (optional) A Tagger instance. If ``None``, defaults to :class:`PatternTagger <text.taggers.PatternTagger>`.
    :param analyzer: (optional) A sentiment analyzer. If ``None``, defaults to :class:`PatternAnalyzer` <text.sentiments.PatternAnalyzer>`.
    :param clean_html: (optional) Remove HTML markup from ``text``.
    '''

    np_extractor = FastNPExtractor()
    pos_tagger = PatternTagger()
    tokenizer = WordTokenizer()
    translator = Translator()
    analyzer = PatternAnalyzer()

    def __init__(self, text, tokenizer=None,
                pos_tagger=None, np_extractor=None, analyzer=None,
                clean_html=False):
        if type(text) not in string_types:
            raise TypeError('The `text` argument passed to `__init__(text)` '
                            'must be a string, not {0}'.format(type(text)))
        self.raw = self.string = text if not clean_html else nltk.clean_html(text)
        self.stripped = lowerstrip(self.raw, all=True)
        # tokenizer may be a textblob or an NLTK tokenizer
        if (tokenizer is not None and
                not (isinstance(tokenizer, BaseTokenizer) or
                    isinstance(tokenizer, nltk.tokenize.api.TokenizerI))):
            raise ValueError("tokenizer must be an instance of BaseTokenizer")
        self.tokenizer = tokenizer if tokenizer else BaseBlob.tokenizer
        if (np_extractor is not None and
                not isinstance(np_extractor, BaseNPExtractor)):
            raise ValueError("np_extractor must be an instance of BaseNPExtractor")
        self.np_extractor = np_extractor if np_extractor else BaseBlob.np_extractor
        if (pos_tagger is not None and
                not isinstance(pos_tagger, BaseTagger)):
            raise ValueError("pos_tagger must be an instance of BaseTagger")
        self.pos_tagger = pos_tagger if pos_tagger else BaseBlob.pos_tagger
        if (analyzer is not None and
                not isinstance(analyzer, BaseSentimentAnalyzer)):
            raise ValueError("analyzer must be an instance of BaseSentimentAnalyzer")
        self.analyzer = analyzer if analyzer else BaseBlob.analyzer

    @cached_property
    def words(self):
        '''Return a list of word tokens. This excludes punctuation characters.
        If you want to include punctuation characters, access the ``tokens``
        property.
        '''
        return WordList(WordTokenizer().tokenize(self.raw, include_punc=False))

    @cached_property
    def tokens(self):
        '''Return a list of tokens, using this blob's tokenizer object
        (defaults to :class:`WordTokenizer <text.tokenizers.WordTokenizer>`).
        '''
        return WordList(self.tokenizer.tokenize(self.raw))

    def tokenize(self, tokenizer=None):
        '''Return a list of tokens, using ``tokenizer``.

        :param tokenizer: (optional) A tokenizer object. If None, defaults to this blob's default tokenizer.
        '''
        t = tokenizer if tokenizer is not None else self.tokenizer
        return WordList(t.tokenize(self.raw))

    @cached_property
    def sentiment(self):
        '''Return a tuple of form (polarity, subjectivity ) where polarity
        is a float within the range [-1.0, 1.0] and subjectivity is a float
        within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is
        very subjective.

        :rtype: tuple
        '''
        return self.analyzer.analyze(self.raw)

    @cached_property
    def polarity(self):
        '''Return the polarity score as a float within the range [-1.0, 1.0]

        :rtype: float
        '''
        return PatternAnalyzer().analyze(str(self))[0]

    @cached_property
    def subjectivity(self):
        '''Return the subjectivity score as a float within the range [0.0, 1.0]
        where 0.0 is very objective and 1.0 is very subjective.

        :rtype: float
        '''
        return PatternAnalyzer().analyze(str(self))[1]

    @cached_property
    def noun_phrases(self):
        '''Returns a list of noun phrases for this blob.'''
        return WordList([phrase.strip().lower()
                        for phrase in self.np_extractor.extract(self.raw)
                        if len(phrase) > 1])

    @cached_property
    def pos_tags(self):
        '''Returns an list of tuples of the form (word, POS tag).

        Example:
        ::

            [('At', 'IN'), ('eight', 'CD'), ("o'clock", 'JJ'), ('on', 'IN'),
                    ('Thursday', 'NNP'), ('morning', 'NN')]

        :rtype: list of tuples
        '''
        return [(Word(word, pos_tag=t), unicode(t))
                for word, t in self.pos_tagger.tag(self.raw)
                if not PUNCTUATION_REGEX.match(unicode(t))]

    tags = pos_tags

    @cached_property
    def word_counts(self):
        '''Dictionary of word frequencies in this text.
        '''
        counts = defaultdict(int)
        stripped_words = [lowerstrip(word) for word in self.words]
        for word in stripped_words:
            counts[word] += 1
        return counts

    @cached_property
    def np_counts(self):
        '''Dictionary of noun phrase frequencies in this text.
        '''
        counts = defaultdict(int)
        for phrase in self.noun_phrases:
            counts[phrase] += 1
        return counts

    def ngrams(self, n=3):
        '''Return a list of n-grams (tuples of n successive words) for this
        blob.
        '''
        if n <= 0:
            return []
        grams = [WordList(self.words[i:i+n])
                            for i in range(len(self.words) - n + 1)]
        return grams

    def translate(self, from_lang="en", to="en"):
        '''Translate the blob to another language.
        Uses the Google Translate API. Returns a new TextBlob.

        Requires an internet connection.

        Usage:
        ::

            >>> b = TextBlob("Simple is better than complex")
            >>> b.translate(to="es")
            TextBlob('Lo simple es mejor que complejo')

        Language code reference:
            https://developers.google.com/translate/v2/using_rest#language-params

        New in `0.5.0`.

        :param from_lang: Language to translate from.
        :param to: Language to translate to.
        :rtype: Blob

        '''
        return self.__class__(self.translator.translate(self.raw,
                        from_lang=from_lang, to_lang=to))

    def detect_language(self):
        '''Detect the blob's language using the Google Translate API.

        Requires an internet connection.

        Usage:
        ::

            >>> b = TextBlob("bonjour")
            >>> b.detect_language()
            u'fr'

        Language code reference:
            https://developers.google.com/translate/v2/using_rest#language-params

        New in `0.5.0`.

        :rtype: str

        '''
        return self.translator.detect(self.raw)

    def __repr__(self):
        '''Returns a string representation for debugging.'''
        class_name = self.__class__.__name__
        if len(self) > 100:
            return unicode("{cls}('{beginning}...{end}')".format(cls=class_name,
                    beginning=unicode(self)[:50], end=self.raw[-20:]))
        else:
            return unicode("{cls}('{text}')".format(cls=class_name, text=self.raw))

    def __len__(self):
        '''Returns the length of the raw text.'''
        return len(self.raw)

    def __str__(self):
        '''Returns a string representation used in print statements
        or str(my_blob).'''
        return self.raw

    def __unicode__(self):
        '''Returns the unicode representation of the blob.'''
        return unicode(self.raw)

    def __iter__(self):
        '''Makes the object iterable as if it were a string,
        iterating through the raw string's characters.
        '''
        return iter(self.raw)

    def _cmpkey(self):
        '''Key used by ComparableMixin to implement all rich comparison
        operators.
        '''
        return self.raw

    def __eq__(self, other):
        '''Equality comparator. Blobs are be equal to blobs with the same
        text and also to their string counterparts.
        '''
        if type(other) in string_types:
            return self.raw == other
        else:
            return super(BaseBlob, self).__eq__(other)

    def __hash__(self):
        return hash(self._cmpkey())

    def __getitem__(self, index):
        '''Returns a  substring. If index is an integer, returns a Python
        string of a single character. If a range is given, e.g. `blob[3:5]`,
        a new instance of the class is returned.
        '''
        if isinstance(index, int):
            return self.raw[index]  # Just return a single character
        else:
            # Return a new blob object
            return self.__class__(self.raw[index])

    def __add__(self, other):
        '''Concatenates two text objects the same way Python strings are
        concatenated.

        Arguments:
        - `other`: a string or a text object
        '''
        if type(other) in string_types:
            return TextBlob(str(self) + other)
        elif isinstance(other, BaseBlob):
            return TextBlob(str(self) + str(other))
        else:
            raise TypeError('Operands must be either strings or {0} objects'
                .format(self.__class__.__name__))

    def __contains__(self, sub):
        '''Implements the `in` keyword like a Python string.'''
        return sub in str(self)

    def find(self, sub, start=0, end=sys.maxsize):
        '''Behaves like the built-in str.find() method. Returns an integer,
        the index of the first occurrence of the substring argument sub in the
        sub-string given by [start:end].
        '''
        return str(self).find(sub, start, end)

    def rfind(self, sub, start=0, end=sys.maxsize):
        '''Behaves like the built-in str.rfind() method. Returns an integer,
        the index of he last (right-most) occurence of the substring argument
        sub in the sub-sequence given by [start:end].
        '''
        return str(self).rfind(sub, start, end)

    def index(self, sub, start=0, end=sys.maxsize):
        '''Like blob.find() but raise ValueError when the substring
        is not found.
        '''
        return str(self).index(sub, start, end)

    def startswith(self, prefix, start=0, end=sys.maxsize):
        """Returns True if the blob starts with the given prefix."""
        return str(self).startswith(prefix, start, end)

    def endswith(self, suffix, start=0, end=sys.maxsize):
        """Returns True if the blob ends with the given suffix."""
        return str(self).endswith(suffix, start, end)

    # PEP8 aliases
    starts_with = startswith
    ends_with = endswith

    def title(self):
        """Returns a blob object with the text in title-case."""
        return TextBlob(str(self).title())

    def format(self, *args, **kwargs):
        """Perform a string formatting operation, like the built-in
        `str.format(*args, **kwargs)`. Returns a blob object.
        """
        return TextBlob(str(self).format(*args, **kwargs))

    def split(self, sep=None, maxsplit=sys.maxsize):
        """Behaves like the built-in str.split() except returns a
        WordList.
        """
        return WordList(str(self).split(sep, maxsplit))

    def strip(self, chars=None):
        """Behaves like the built-in str.strip([chars]) method. Returns
        an object with leading and trailing whitespace removed.
        """
        return self.__class__(str(self).strip(chars))

    def upper(self):
        """Like str.upper(), returns new object with all upper-cased characters.
        """
        return self.__class__(str(self).upper())

    def lower(self):
        """Like str.lower(), returns new object with all lower-cased characters.
        """
        return self.__class__(str(self).lower())

    def join(self, iterable):
        """Behaves like the built-in `str.join(iterable)` method, except
        returns a blob object.

        Returns a blob which is the concatenation of the strings or blobs
        in the iterable.
        """
        return self.__class__(str(self).join(iterable))

    def replace(self, old, new, count=sys.maxsize):
        """Return a new blob object with all the occurence of `old` replaced
        by `new`.
        """
        return self.__class__(str(self).replace(old, new, count))


class TextBlob(BaseBlob):

    """A general text block, meant for larger bodies of text (esp. those
    containing sentences). Inherits from :class:`BaseBlob <BaseBlob>`.

    :param text: A string.
    :param tokenizer: (optional) A tokenizer instance. If ``None``, defaults to :class:`WordTokenizer() <text.tokenizers.WordTokenizer>`.
    :param np_extractor: (optional) An NPExtractor instance. If ``None``, defaults to :class:`FastNPExtractor() <text.np_extractors.FastNPExtractor>`.
    :param pos_tagger: (optional) A Tagger instance. If ``None``, defaults to :class:`PatternTagger <text.taggers.PatternTagger>`.
    :param analyzer: (optional) A sentiment analyzer. If ``None``, defaults to :class:`PatternAnalyzer` <text.sentiments.PatternAnalyzer>`.
    :param clean_html: (optional) Remove HTML markup from ``text``.
    """

    @cached_property
    def sentences(self):
        '''Return list of :class:`Sentence <Sentence>` objects.'''
        return TextBlob.create_sentence_objects(self.raw)

    @cached_property
    def words(self):
        '''Return a list of word tokens. This excludes punctuation characters.
        If you want to include punctuation characters, access the ``tokens``
        property.
        '''
        # NLTK's word tokenizer expects sentences as input, so tokenize the
        # blob into sentences before tokenizing to words
        words = []
        for sent in self.sentences:
            words.extend(WordTokenizer().tokenize(str(sent), include_punc=False))
        return WordList(words)


    @property
    def raw_sentences(self):
        '''List of strings, the raw sentences in the blob.'''
        return [sentence.raw for sentence in self.sentences]

    @property
    def serialized(self):
        '''Returns a list of each sentences dict representation.'''
        return [sentence.dict for sentence in self.sentences]

    def json(self, *args, **kwargs):
        '''Returns a json representation of this blob.'''
        return json.dumps(self.serialized, *args, **kwargs)

    @staticmethod
    def create_sentence_objects(blob):
        '''Returns a list of Sentence objects given
        a list of sentence strings. Attempts to handle sentences that
        have more than one punctuation mark at the end of the sentence.
        Examples: "An ellipses is no problem..." or "This is awesome!!!"
        '''
        sent_tokenizer = SentenceTokenizer()
        sentence_objects = []
        try:
            sentences = sent_tokenizer.tokenize(blob)  # List of raw sentences
        except LookupError:
            raise MissingCorpusException()
        # if there is only one sentence or string of text
        if len(sentences) <= 1:
            sentence_objects.append(Sentence(sentences[0], start_index=0,
                                    end_index=len(sentences[0]) - 1))
        else:
        # If there are many sentences
            char_index = 0  # Keeps track of character index within the blob
            for i, raw_sentence in enumerate(sentences):
                # Compute the start and end indices of the sentence
                # within the blob
                start_index = char_index
                char_index += len(raw_sentence)

                # Sometimes the NLTK tokenizer misses some punctuation when
                # there are multiple punctuations, e.g. with ellipses ("...")
                # or multiple exclamation points ("!!!")
                try:
                    next_token = sentences[i + 1]
                except IndexError:
                    # Continue if the last token is a punctuation
                    if len(raw_sentence) <= 1:
                        continue
                # If the next token is 1 character, assume it's a punctuation
                if len(next_token) == 1:
                    raw_sentence += next_token  # append the extra punctuation
                    char_index += 1  # also correct the char_index
                # Create a Sentence object and add it the the list
                sentence_objects.append(Sentence(raw_sentence,
                        start_index=start_index, end_index=char_index))
        return sentence_objects


class Sentence(BaseBlob):

    '''A sentence within a TextBlob. Inherits from :class:`BaseBlob <BaseBlob>`.

    :param sentence: A string, the raw sentence.
    :param start_index: An int, the index where this sentence begins
                        in a TextBlob. If not given, defaults to 0.
    :param end_index: An int, the index where this sentence ends in
                        a TextBlob. If not given, defaults to the
                        length of the sentence - 1.
    '''

    def __init__(self, sentence, start_index=0, end_index=None, *args, **kwargs):
        super(Sentence, self).__init__(sentence, *args, **kwargs)
        self.start = self.start_index = start_index
        self.end = self.end_index = end_index if end_index else len(sentence) - 1

    @property
    def dict(self):
        '''The dict representation of this sentence.'''
        return {
            'raw': self.raw,
            'start_index': self.start_index,
            'end_index': self.end_index,
            'stripped': self.stripped,
            'noun_phrases': self.noun_phrases,
            'polarity': self.polarity,
            'subjectivity': self.subjectivity,
        }

class Blobber(object):

    '''A factory for TextBlobs that all share the same tagger,
    tokenizer, and np_extractor.

    Usage:

        >>> from text.blob import Blobber
        >>> from text.taggers import NLTKTagger
        >>> from text.tokenizers import SentenceTokenizer
        >>> tb = Blobber(pos_tagger=NLTKTagger(), tokenizer=SentenceTokenizer())
        >>> blob1 = tb("This is one blob.")
        >>> blob2 = tb("This blob has the same tagger and tokenizer.")
        >>> blob1.pos_tagger == blob2.pos_tagger
        True

    :param tokenizer: A tokenizer. Default: :class:`WordTokenizer <text.tokenizers.WordTokenizer>`.
    :param pos_tagger: A POS tagger. Default: :class:`PatternTagger <text.taggers.PatternTagger>`.
    :param np_extractor: A NP extractor. Default: :class:`FastNPExtractor <text.np_extractors.FastNPExtractor>`.
    :param analyzer: (optional) A sentiment analyzer. If ``None``, defaults to :class:`PatternAnalyzer` <text.sentiments.PatternAnalyzer>`.
    '''

    np_extractor = FastNPExtractor()
    pos_tagger = PatternTagger()
    tokenizer = WordTokenizer()
    analyzer = PatternAnalyzer()

    def __init__(self, tokenizer=None, pos_tagger=None, np_extractor=None,
                analyzer=None):
        # tokenizer may be a textblob or an NLTK tokenizer
        if (tokenizer is not None and
                not (isinstance(tokenizer, BaseTokenizer) or
                    isinstance(tokenizer, nltk.tokenize.api.TokenizerI))):
            raise ValueError("tokenizer must be an instance of BaseTokenizer")
        self.tokenizer = tokenizer if tokenizer else Blobber.tokenizer
        if (np_extractor is not None and
                not isinstance(np_extractor, BaseNPExtractor)):
            raise ValueError("np_extractor must be an instance of BaseNPExtractor")
        self.np_extractor = np_extractor if np_extractor else Blobber.np_extractor
        if (pos_tagger is not None and
                not isinstance(pos_tagger, BaseTagger)):
            raise ValueError("pos_tagger must be an instance of BaseTagger")
        self.pos_tagger = pos_tagger if pos_tagger else Blobber.pos_tagger
        if (analyzer is not None and
                not isinstance(analyzer, BaseSentimentAnalyzer)):
            raise ValueError("analyzer must be an instance of BaseSentimentAnalyzer")
        self.analyzer = analyzer if analyzer else BaseBlob.analyzer

    def __call__(self, text):
        '''Return a new TextBlob object with this Blobber's ``np_extractor``,
        ``pos_tagger``, and ``tokenizer``.

        :returns: A new TextBlob.
        '''
        return TextBlob(text, tokenizer=self.tokenizer, pos_tagger=self.pos_tagger,
            np_extractor=self.np_extractor, analyzer=self.analyzer)

    def __repr__(self):
        return ("Blobber(tokenizer={0}(), pos_tagger={1}(), "
                    "np_extractor={2}(), analyzer={3}())")\
                    .format(self.tokenizer.__class__.__name__,
                            self.pos_tagger.__class__.__name__,
                            self.np_extractor.__class__.__name__,
                            self.analyzer.__class__.__name__)

    __str__ = __repr__



