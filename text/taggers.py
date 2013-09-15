# -*- coding: utf-8 -*-
'''Parts-of-speech tagger implementations.'''
from __future__ import absolute_import
import random
import logging
import os.path
from collections import defaultdict
import pickle

import text
from text.packages import nltk
from text.en import tag as pattern_tag
from text.exceptions import MissingCorpusException
from text._perceptron import AveragedPerceptron


class BaseTagger(object):

    '''Abstract tagger class from which all taggers
    inherit from. All descendants must implement a
    `tag()` method.
    '''

    def tag(self, sentence, tokenize=True):
        '''Return a list of tuples of the form (word, tag)
        for a given set of text.
        '''
        raise NotImplementedError('Must implement a tag() method')


class PatternTagger(BaseTagger):

    '''Tagger that uses the implementation in
    Tom de Smedt's pattern library
    (http://www.clips.ua.ac.be/pattern).
    '''

    def tag(self, sentence, tokenize=True):
        '''Tag a string `sentence`.'''
        return pattern_tag(sentence, tokenize)

class NLTKTagger(BaseTagger):

    '''Tagger that uses NLTK's standard TreeBank tagger.
    NOTE: Currently supported on Python 2 only, and requires numpy.
    '''

    def tag(self, sentence, tokenize=True):
        '''Tag a string `sentence`.'''
        if tokenize:
            sentence = nltk.tokenize.word_tokenize(sentence)
        try:
            tagged = nltk.tag.pos_tag(sentence)
        except LookupError as e:
            print(e)
            raise MissingCorpusException()
        return tagged


class PerceptronTagger(BaseTagger):

    '''Greedy Averaged Perceptron tagger, as implemented by Matthew Honnibal.
    Requires that ``trontagger.pickle`` exists in the text/ package directory.
    For more information on how to get and install the pickled model, see
    the install guide here:

        https://textblob.readthedocs.org/en/latest/install.html

    See more info about the Averaged Perceptron Tagger at this blog post:

        http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/

    The tagger is about 96.8%% accurate.

    :param load: Load the pickled model upon initiation.

    .. versionadded:: 0.6.3
    '''

    START = ['-START-', '-START2-']
    END = ['-END-', '-END2-']
    AP_MODEL_LOC = os.path.join(os.path.dirname(__file__), 'trontagger.pickle')

    def __init__(self, load=True):
        self.model = AveragedPerceptron()
        self.tagdict = {}
        self.classes = set()
        if load:
            self.load(self.AP_MODEL_LOC)

    def tag(self, corpus, tokenize=True):
        '''Tags a string `corpus`.'''
        # Assume untokenized corpus has \n between sentences and ' ' between words
        s_split = nltk.sent_tokenize if tokenize else lambda t: t.split('\n')
        w_split = nltk.word_tokenize if tokenize else lambda s: s.split()
        def split_sents(corpus):
            for s in s_split(corpus):
                yield w_split(s)

        prev, prev2 = self.START
        tokens = []
        for words in split_sents(corpus):
            context = self.START + [self._normalize(w) for w in words] + self.END
            for i, word in enumerate(words):
                tag = self.tagdict.get(word)
                if not tag:
                    features = self._get_features(i, word, context, prev, prev2)
                    tag = self.model.predict(features)
                tokens.append((word, tag))
                prev2 = prev
                prev = tag
        return tokens

    def train(self, sentences, save_loc=None, nr_iter=5):
        '''Train a model from sentences, and save it at ``save_loc``. ``nr_iter``
        controls the number of Perceptron training iterations.

        :param sentences: A list of (words, tags) tuples.
        :param save_loc: If not ``None``, saves a pickled model in this location.
        :param nr_iter: Number of training iterations.
        '''
        self._make_tagdict(sentences)
        self.model.classes = self.classes
        prev, prev2 = self.START
        for iter_ in range(nr_iter):
            c = 0
            n = 0
            for words, tags in sentences:
                context = self.START + [self._normalize(w) for w in words] \
                                                                    + self.END
                for i, word in enumerate(words):
                    guess = self.tagdict.get(word)
                    if not guess:
                        feats = self._get_features(i, word, context, prev, prev2)
                        guess = self.model.predict(feats)
                        self.model.update(tags[i], guess, feats)
                    prev2 = prev
                    prev = guess
                    c += guess == tags[i]
                    n += 1
            random.shuffle(sentences)
            logging.info("Iter {0}: {1}/{2}={3}".format(iter_, c, n, _pc(c, n)))
        self.model.average_weights()
        # Pickle as a binary file
        if save_loc is not None:
            pickle.dump((self.model.weights, self.tagdict, self.classes),
                         open(save_loc, 'wb'), -1)
        return None

    def load(self, loc):
        '''Load a pickled model.'''
        try:
            w_td_c = pickle.load(open(loc, 'rb'))
        except IOError:
            package_dir = text.PACKAGE_DIR
            msg = ("Missing trontagger.pickle. Download it from the TextBlob "
                    "release page: https://github.com/sloria/TextBlob/releases"
                    " and add it to your textblob package "
                    "directory: {0}".format(package_dir))
            raise MissingCorpusException(msg)
        self.model.weights, self.tagdict, self.classes = w_td_c
        self.model.classes = self.classes
        return None

    def _normalize(self, word):
        '''Normalization used in pre-processing.

        - All words are lower cased
        - Digits in the range 1800-2100 are represented as !YEAR;
        - Other digits are represented as !DIGITS

        :rtype: str
        '''
        if '-' in word and word[0] != '-':
            return '!HYPHEN'
        elif word.isdigit() and len(word) == 4:
            return '!YEAR'
        elif word[0].isdigit():
            return '!DIGITS'
        else:
            return word.lower()

    def _get_features(self, i, word, context, prev, prev2):
        '''Map tokens into a feature representation, implemented as a
        {hashable: float} dict. If the features change, a new model must be
        trained.
        '''
        def add(name, *args):
            features[' '.join((name,) + tuple(args))] += 1

        i += len(self.START)
        features = defaultdict(int)
        # It's useful to have a constant feature, which acts sort of like a prior
        add('bias')
        add('i suffix', word[-3:])
        add('i pref1', word[0])
        add('i-1 tag', prev)
        add('i-2 tag', prev2)
        add('i tag+i-2 tag', prev, prev2)
        add('i word', context[i])
        add('i-1 tag+i word', prev, context[i])
        add('i-1 word', context[i-1])
        add('i-1 suffix', context[i-1][-3:])
        add('i-2 word', context[i-2])
        add('i+1 word', context[i+1])
        add('i+1 suffix', context[i+1][-3:])
        add('i+2 word', context[i+2])
        return features

    def _make_tagdict(self, sentences):
        '''Make a tag dictionary for single-tag words.'''
        counts = defaultdict(lambda: defaultdict(int))
        for words, tags in sentences:
            for word, tag in zip(words, tags):
                counts[word][tag] += 1
                self.classes.add(tag)
        freq_thresh = 20
        ambiguity_thresh = 0.97
        for word, tag_freqs in counts.items():
            tag, mode = max(tag_freqs.items(), key=lambda item: item[1])
            n = sum(tag_freqs.values())
            # Don't add rare words to the tag dictionary
            # Only add quite unambiguous words
            if n >= freq_thresh and (float(mode) / n) >= ambiguity_thresh:
                self.tagdict[word] = tag

def _pc(n, d):
    return (float(n) / d) * 100
