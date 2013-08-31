# -*- coding: utf-8 -*-
'''Various classifier implementations. Also includes basic feature extractor
methods.

Example Usage:
::

    >>> from text.blob import TextBlob
    >>> from text.classifiers import NaiveBayesClassifier
    >>> train = [
    ...     ('I love this sandwich.', 'pos'),
    ...     ('This is an amazing place!', 'pos'),
    ...     ('I feel very good about these beers.', 'pos'),
    ...     ('I do not like this restaurant', 'neg'),
    ...     ('I am tired of this stuff.', 'neg'),
    ...     ("I can't deal with this", 'neg'),
    ...     ("My boss is horrible.", "neg")
    ... ]
    >>> cl = NaiveBayesClassifier(train)
    >>> cl.classify("I feel amazing!")
    'pos'
    >>> blob = TextBlob("The beer is good. But the hangover is horrible.", classifier=cl)
    >>> for s in blob.sentences:
    ...     print(s)
    ...     print(s.classify())
    ...
    The beer is good.
    pos
    But the hangover is horrible.
    neg

.. versionadded:: 0.6.0
'''
from .packages import nltk
from .tokenizers import WordTokenizer
from .compat import basestring, u
from .decorators import cached_property
import formats

##### Basic feature extractors #####

def _get_words_from_dataset(dataset):
    '''Return a set of all words in a dataset.

    :param dataset: A list of tuples of the form ``(words, label)`` where
        ``words`` is either a string of a list of tokens.
    '''
    tokenizer = WordTokenizer()
    all_words = []
    for words, classification in dataset:
        # Words may either be a string or an iterable
        if isinstance(words, basestring):
            all_words.extend(tokenizer.itokenize(words, include_punc=False))
        else:
            all_words.extend(words)
    return set(all_words)

def basic_extractor(document, train_set):
    '''A basic document feature extractor that returns a dict indicating
    what words in ``train_set`` are contained in ``document``.

    :param document: The text to extract features from. Can be a string or an iterable.
    :param train_set: Training data set, a list of tuples of the form
        ``(words, label)``.
    '''
    tokenizer = WordTokenizer()
    word_features = _get_words_from_dataset(train_set)
    if isinstance(document, basestring):
        tokens = set([w.lower()
                    for w in tokenizer.itokenize(document, include_punc=False)])
    else:
        tokens = set((w.lower() for w in document))
    features = dict([(u('contains({0})').format(w), (w in tokens))
                                            for w in word_features])
    return features

##### Classifiers #####

class BaseClassifier(object):

    '''Abstract classifier class from which all classifers inherit. At a
    minimum, descendant classes must implement a ``classify`` method and have
    a ``classifier`` property.

    :param train_set: The training set, either a list of tuples of the form
        ``(text, classification)`` or a filename. ``text`` may be either
        a string or an iterable.
    :param feature_extractor: A feature extractor function that takes one or
        two arguments: ``document`` and ``train_set``.
    :param format: If ``train_set`` is a filename, the file format, e.g.
        ``"csv"`` or ``"json"``. If ``None``, will attempt to detect the
        file format.

    .. versionadded:: 0.6.0
    '''

    def __init__(self, train_set, feature_extractor=basic_extractor, format=None):
        self.feature_extractor = feature_extractor
        if isinstance(train_set, basestring): # train_set is a filename
            self.train_set = self._read_data(train_set, format)
        else: # train_set is a list of tuples
            self.train_set = train_set
        self.train_features = None

    def _read_data(self, dataset, format=None):
        '''Reads a data file and returns and iterable that can be used
        as testing or training data.
        '''
        # Attempt to detect file format if "format" isn't specified
        if not format:
            format_class = formats.detect(dataset)
        else:
            if format not in formats.AVAILABLE.keys():
                raise ValueError("'{0}' format not supported.".format(format))
            format_class = formats.AVAILABLE[format]
        return format_class(dataset).to_iterable()

    @cached_property
    def classifier(self):
        '''The classifier object.'''
        raise NotImplementedError('Must implement the "classifier" property.')

    def classify(self, text):
        '''Classifies a string of text.'''
        raise NotImplementedError('Must implement a "classify" method.')

    def extract_features(self, text):
        '''Extracts features from a body of text.

        :rtype: dictionary of features
        '''
        try:
            return self.feature_extractor(text, self.train_set)
        except TypeError:
            return self.feature_extractor(text)

    def accuracy(self, test_set, format=None):
        '''Compute the accuracy on a test set.

        :param test_set: A list of tuples of the form ``(text, label)``, or a
            filename.
        :param format: If ``test_set`` is a filename, the file format, e.g.
            ``"csv"`` or ``"json"``. If ``None``, will attempt to detect the
            file format.
        '''
        if isinstance(test_set, basestring):  # test_set is a filename
            test_data = self._read_data(test_set)
        else:  # test_set is a list of tuples
            test_data = test_set
        test_features = [(self.extract_features(d), c) for d, c in test_data]
        return nltk.classify.accuracy(self.classifier, test_features)


class NaiveBayesClassifier(BaseClassifier):

    '''A classifier based on the Naive Bayes algorithm, as implemented in
    NLTK.

    :param train_set: The training set, a list of tuples of the form
        ``(text, classification)`` where text may be either a string or an iterable.
    :param feature_extractor: (optional) A feature extractor function that
        must take two arguments: ``document`` and ``train_set``.

    .. versionadded:: 0.6.0
    '''

    @cached_property
    def classifier(self):
        '''The Naive Bayes classifier.'''
        self.train_features = [(self.extract_features(d), c) for d, c in self.train_set]
        return nltk.classify.NaiveBayesClassifier.train(self.train_features)

    def classify(self, text):
        '''Classifies the text.

        :param text: A string of text.
        '''
        text_features = self.extract_features(text)
        return self.classifier.classify(text_features)

    def prob_classify(self, text):
        '''Return the label probability distribution for classifying a string
        of text.

        Example:
        ::

            >>> classifier = NaiveBayesClassifier(train_data)
            >>> prob_dist = classifier.prob_classify("I feel happy this morning.")
            >>> prob_dist.max()
            'positive'
            >>> prob_dist.prob("positive")
            0.7

        :rtype: nltk.probability.DictionaryProbDist
        '''
        text_features = self.extract_features(text)
        return self.classifier.prob_classify(text_features)

    def informative_features(self, *args, **kwargs):
        '''Return the most informative features as a list of tuples of the
        form ``(feature_name, feature_value)``.
        '''
        return self.classifier.most_informative_features(*args, **kwargs)

    def show_informative_features(self, *args, **kwargs):
        '''Displays a listing of the most informative features for this
        classifier.
        '''
        return self.classifier.show_most_informative_features(*args, **kwargs)

    def update(self, new_data):
        '''Update the classifier with new training data and re-trains the
        classifier.

        :param new_data: New data as a list of tuples of the form
            ``(text, label)``.
        '''
        self.train_set += new_data
        self.train_features = [(self.extract_features(d), c)
                                for d, c in self.train_set]
        self.classifier = nltk.classify.NaiveBayesClassifier.train(self.train_features)
        return True
