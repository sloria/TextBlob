# -*- coding: utf-8 -*-
'''Various classifier implementations. Also includes basic feature extractor
methods.

Example Usage:
::

    >>> from textblob import TextBlob
    >>> from textblob.classifiers import NaiveBayesClassifier
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
from __future__ import absolute_import
from textblob.packages import nltk
from textblob.tokenizers import WordTokenizer
from textblob.compat import basestring
import textblob.formats as formats
from textblob.utils import strip_punc
from textblob.decorators import cached_property

### Basic feature extractors ###


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
        tokens = set([strip_punc(w, all=False)
                    for w in tokenizer.itokenize(document, include_punc=False)])
    else:
        tokens = set(strip_punc(w, all=False) for w in document)
    features = dict([(u'contains({0})'.format(word), (word in tokens))
                                            for word in word_features])
    return features


def contains_extractor(document):
    '''A basic document feature extractor that returns a dict of words that
    the document contains.
    '''
    tokenizer = WordTokenizer()
    if isinstance(document, basestring):
        tokens = set([strip_punc(w, all=False)
                    for w in tokenizer.itokenize(document, include_punc=False)])
    else:
        tokens = set((strip_punc(w, all=False) for w in document))
    features = dict((u'contains({0})'.format(w), True) for w in tokens)
    return features

##### CLASSIFIERS #####

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
        if isinstance(train_set, basestring):  # train_set is a filename
            self.train_set = self._read_data(train_set, format)
        else:  # train_set is a list of tuples
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

    def train(self, labeled_featureset):
        '''Trains the classifier.'''
        raise NotImplementedError('Must implement a "train" method.')

    def labels(self):
        '''Returns an iterable containing the possible labels.'''
        raise NotImplementedError('Must implement a "labels" method.')

    def extract_features(self, text):
        '''Extracts features from a body of text.

        :rtype: dictionary of features
        '''
        try:
            return self.feature_extractor(text, self.train_set)
        except (TypeError, AttributeError):
            return self.feature_extractor(text)


class NLTKClassifier(BaseClassifier):

    """An abstract class that wraps around the nltk.classify module.

    Expects that descendant classes include a class variable ``nltk_class``
    which is the class in the nltk.classify module to be wrapped.

    Example: ::

        class MyClassifier(NLTKClassifier):
            nltk_class = nltk.classify.svm.SvmClassifier

    """

    nltk_class = None  # This must be a class within nltk.classify

    def __init__(self, train_set,
                 feature_extractor=basic_extractor, format=None):
        super(NLTKClassifier, self).__init__(train_set, feature_extractor, format)
        self.train_features = [(self.extract_features(d), c) for d, c in self.train_set]

    def __repr__(self):
        class_name = self.__class__.__name__
        return "<{cls} trained on {n} instances>".format(cls=class_name,
                                                        n=len(self.train_set))

    @cached_property
    def classifier(self):
        '''The classifier.'''
        try:
            return self.train()
        except AttributeError:  # nltk_class has not been defined
            raise ValueError("NLTKClassifier must have a nltk_class"
                            " variable that is not None.")

    def train(self, *args, **kwargs):
        '''Train the classifier with a labeled feature set and return
        the classifier. Takes the same arguments as the wrapped NLTK class.
        This method is implicitly called when calling ``classify`` or
        ``accuracy`` methods and is included only to allow passing in arguments
        to the ``train`` method of the wrapped NLTK class.

        .. versionadded:: 0.6.2

        :rtype: A classifier
        '''
        try:
            self.classifier = self.nltk_class.train(self.train_features,
                                                    *args, **kwargs)
            return self.classifier
        except AttributeError:
            raise ValueError("NLTKClassifier must have a nltk_class"
                            " variable that is not None.")

    def labels(self):
        '''Return an iterable of possible labels.'''
        return self.classifier.labels()

    def classify(self, text):
        '''Classifies the text.

        :param text: A string of text.
        '''
        text_features = self.extract_features(text)
        return self.classifier.classify(text_features)

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

    def update(self, new_data, *args, **kwargs):
        '''Update the classifier with new training data and re-trains the
        classifier.

        :param new_data: New data as a list of tuples of the form
            ``(text, label)``.
        '''
        self.train_set += new_data
        self.train_features = [(self.extract_features(d), c)
                                for d, c in self.train_set]
        try:
            self.classifier = self.nltk_class.train(self.train_features,
                                                    *args, **kwargs)
        except AttributeError:  # Descendant has not defined nltk_class
            raise ValueError("NLTKClassifier must have a nltk_class"
                            " variable that is not None.")
        return True


class NaiveBayesClassifier(NLTKClassifier):

    '''A classifier based on the Naive Bayes algorithm, as implemented in
    NLTK.

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

    nltk_class = nltk.classify.NaiveBayesClassifier

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

        :rtype: list
        '''
        return self.classifier.most_informative_features(*args, **kwargs)

    def show_informative_features(self, *args, **kwargs):
        '''Displays a listing of the most informative features for this
        classifier.

        :rtype: None
        '''
        return self.classifier.show_most_informative_features(*args, **kwargs)


class DecisionTreeClassifier(NLTKClassifier):

    '''A classifier based on the decision tree algorithm, as implemented in
    NLTK.

    :param train_set: The training set, either a list of tuples of the form
        ``(text, classification)`` or a filename. ``text`` may be either
        a string or an iterable.
    :param feature_extractor: A feature extractor function that takes one or
        two arguments: ``document`` and ``train_set``.
    :param format: If ``train_set`` is a filename, the file format, e.g.
        ``"csv"`` or ``"json"``. If ``None``, will attempt to detect the
        file format.

    .. versionadded:: 0.6.2
    '''

    nltk_class = nltk.classify.decisiontree.DecisionTreeClassifier

    def pprint(self, *args, **kwargs):
        '''Return a string containing a pretty-printed version of this decision
        tree. Each line in the string corresponds to a single decision tree node
        or leaf, and indentation is used to display the structure of the tree.

        :rtype: str
        '''
        return self.classifier.pp(*args, **kwargs)

    def pseudocode(self, *args, **kwargs):
        '''Return a string representation of this decision tree that expresses
        the decisions it makes as a nested set of pseudocode if statements.

        :rtype: str
        '''
        return self.classifier.pseudocode(*args, **kwargs)


class PositiveNaiveBayesClassifier(NLTKClassifier):

    '''A variant of the Naive Bayes Classifier that performs binary
    classification with partially-labeled training sets, i.e. when only
    one class is labeled and the other is not. Assuming a prior distribution
    on the two labels, uses the unlabeled set to estimate the frequencies of
    the features.

    Example usage:
    ::

        >>> from text.classifiers import PositiveNaiveBayesClassifier
        >>> sports_sentences = ['The team dominated the game',
        ...                   'They lost the ball',
        ...                   'The game was intense',
        ...                   'The goalkeeper catched the ball',
        ...                   'The other team controlled the ball']
        >>> various_sentences = ['The President did not comment',
        ...                        'I lost the keys',
        ...                        'The team won the game',
        ...                        'Sara has two kids',
        ...                        'The ball went off the court',
        ...                        'They had the ball for the whole game',
        ...                        'The show is over']
        >>> classifier = PositiveNaiveBayesClassifier(positive_set=sports_sentences,
        ...                                           unlabeled_set=various_sentences)
        >>> classifier.classify("My team lost the game")
        True
        >>> classifier.classify("And now for something completely different.")
        False


    :param positive_set: A collection of strings that have the positive label.
    :param unlabeled_set: A collection of unlabeled strings.
    :param feature_extractor: A feature extractor function.
    :param positive_prob_prior: A prior estimate of the probability of the
        label ``True``.

    .. versionadded:: 0.7.0
    '''

    nltk_class = nltk.classify.PositiveNaiveBayesClassifier

    def __init__(self, positive_set, unlabeled_set,
                feature_extractor=contains_extractor,
                positive_prob_prior=0.5):
        self.feature_extractor = feature_extractor
        self.positive_set = positive_set
        self.unlabeled_set = unlabeled_set
        self.positive_features = [self.extract_features(d)
                                    for d in self.positive_set]
        self.unlabeled_features = [self.extract_features(d)
                                    for d in self.unlabeled_set]
        self.positive_prob_prior = positive_prob_prior

    def __repr__(self):
        class_name = self.__class__.__name__
        return "<{cls} trained on {n_pos} labeled and {n_unlabeled} unlabeled instances>"\
                        .format(cls=class_name, n_pos=len(self.positive_set),
                                n_unlabeled=len(self.unlabeled_set))

    def train(self, *args, **kwargs):
        '''Train the classifier with a labeled and unlabeled feature sets and return
        the classifier. Takes the same arguments as the wrapped NLTK class.
        This method is implicitly called when calling ``classify`` or
        ``accuracy`` methods and is included only to allow passing in arguments
        to the ``train`` method of the wrapped NLTK class.

        :rtype: A classifier
        '''
        self.classifier = self.nltk_class.train(self.positive_features,
                                                self.unlabeled_features,
                                                self.positive_prob_prior)
        return self.classifier

    def update(self, new_positive_data=None,
               new_unlabeled_data=None, positive_prob_prior=0.5,
               *args, **kwargs):
        '''Update the classifier with new data and re-trains the
        classifier.

        :param new_positive_data: List of new, labeled strings.
        :param new_unlabeled_data: List of new, unlabeled strings.
        '''
        self.positive_prob_prior = positive_prob_prior
        if new_positive_data:
            self.positive_set += new_positive_data
            self.positive_features += [self.extract_features(d)
                                            for d in new_positive_data]
        if new_unlabeled_data:
            self.unlabeled_set += new_unlabeled_data
            self.unlabeled_features += [self.extract_features(d)
                                            for d in new_unlabeled_data]
        self.classifier = self.nltk_class.train(self.positive_features,
                                                self.unlabeled_features,
                                                self.positive_prob_prior,
                                                *args, **kwargs)
        return True
