# -*- coding: utf-8 -*-
"""Sentiment analysis implementations.

.. versionadded:: 0.5.0
"""
from __future__ import absolute_import
from text.packages import nltk
from text.en import sentiment as pattern_sentiment
from text.tokenizers import WordTokenizer
from text.exceptions import MissingCorpusException

DISCRETE = 'ds'
CONTINUOUS = 'co'


class BaseSentimentAnalyzer(object):

    '''Abstract base class from which all sentiment analyzers inherit.
    Should implement an ``analyze(text)`` method which returns either the
    results of analysis.
    '''

    kind = DISCRETE

    def __init__(self):
        self._trained = False

    def train(self):
        # Train me
        self._trained = True

    def analyze(self, text):
        '''Return the result of of analysis. Typically returns either a
        tuple, float, or dictionary.'''
        # Lazily train the classifier
        if not self._trained:
            self.train()
        # Analyze text
        return None

class PatternAnalyzer(BaseSentimentAnalyzer):

    '''Sentiment analyzer that uses the same implementation as the
    pattern library. Returns results as a tuple of the form:

    ``(polarity, subjectivity)``
    '''

    kind = CONTINUOUS

    def analyze(self, text):
        """Return the sentiment as a tuple of the form:
        ``(polarity, subjectivity)``
        """
        return pattern_sentiment(text)

class NaiveBayesAnalyzer(BaseSentimentAnalyzer):

    '''Naive Bayes analyzer that is trained on a dataset of movie reviews.
    Returns results as a tuple of the form:

    ``(classification, pos_probability, neg_probability)``
    '''

    kind = DISCRETE

    def __init__(self):
        super(NaiveBayesAnalyzer, self).__init__()
        self._classifier = None

    def train(self):
        '''Train the Naive Bayes classifier on the movie review corpus.'''
        super(NaiveBayesAnalyzer, self).train()
        try:
            neg_ids = nltk.corpus.movie_reviews.fileids('neg')
            pos_ids = nltk.corpus.movie_reviews.fileids('pos')
        except LookupError as e:
            print(e)
            raise MissingCorpusException()
        neg_feats = [(self._extract_feats(
            nltk.corpus.movie_reviews.words(fileids=[f])), 'neg') for f in neg_ids]
        pos_feats = [(self._extract_feats(
            nltk.corpus.movie_reviews.words(fileids=[f])), 'pos') for f in pos_ids]
        train_data = neg_feats + pos_feats
        self._classifier = nltk.classify.NaiveBayesClassifier.train(train_data)

    def _extract_feats(self, words):
        return dict([(word, True) for word in words])

    def analyze(self, text):
        """Return the sentiment as a tuple of the form:
        ``(classification, pos_probability, neg_probability)``
        """
        # Lazily train the classifier
        super(NaiveBayesAnalyzer, self).analyze(text)
        tokenizer = WordTokenizer()
        tokens = tokenizer.tokenize(text, include_punc=False)
        filtered = [t.lower() for t in tokens if len(t) >= 3]
        feats = self._extract_feats(filtered)
        prob_dist = self._classifier.prob_classify(feats)
        # classification, p_pos, p_neg
        return prob_dist.max(), prob_dist.prob('pos'), prob_dist.prob("neg")

