# -*- coding: utf-8 -*-
'''Parts-of-speech tagger implementations.'''
import random
import os.path
from collections import defaultdict
import pickle

from .packages import nltk
from .en import tag as pattern_tag
from .exceptions import MissingCorpusException
from _perceptron import Perceptron


class BaseTagger(object):

    '''Abstract tagger class from which all taggers
    inherit from. All descendants must implement a
    `tag()` method.
    '''

    def tag(self, sentence):
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
        return pattern_tag(sentence, tokenize)

class NLTKTagger(BaseTagger):

    '''Tagger that uses NLTK's standard TreeBank tagger.
    NOTE: Currently supported on Python 2 only, and requires numpy.
    '''

    def tag(self, sentence, tokenize=True):
        if tokenize:
            sentence = nltk.tokenize.word_tokenize(sentence)
        try:
            tagged = nltk.tag.pos_tag(sentence)
        except LookupError as e:
            print(e)
            raise MissingCorpusException()
        return tagged


START = ['-START-', '-START2-']
END = ['-END-', '-END2-']
AP_MODEL_LOC = os.path.join(os.path.dirname(__file__), 'trontagger.pickle')


class PerceptronTagger(BaseTagger):
    '''Greedy Averaged Perceptron tagger'''
    def __init__(self, load=True):
        self.model = Perceptron()
        self.tagdict = {}
        self.classes = set()
        if load:
            self.load(AP_MODEL_LOC)

    def tag(self, text, tokenize=True):
        # Assume untokenized text has \n between sentences and ' ' between words
        s_split = nltk.sent_tokenize if tokenize else lambda t: t.split('\n')
        w_split = nltk.word_tokenize if tokenize else lambda s: s.split()
        def split_sents(text):
           for s in s_split(text):
                yield w_split(s)
        
        prev, prev2 = START
        tokens = []
        for words in split_sents(text):
            context = START + [self._normalize(w) for w in words] + END
            for i, word in enumerate(words):
                tag = self.tagdict.get(word)
                if not tag:
                    features = self._get_features(i, word, context, prev, prev2)
                    tag = self.model.predict(features)
                tokens.append((word, tag))
                prev2 = prev; prev = tag
        return tokens 

    def train(self, sentences, save_loc=None, nr_iter=5, quiet=False):
        '''Train a model from sentences, and save it at save_loc. nr_iter
        controls the number of Perceptron training iterations.'''
        self._make_tagdict(sentences, quiet=quiet)
        self.model.classes = self.classes
        prev, prev2 = START
        for iter_ in range(nr_iter):
            c = 0; n = 0
            for words, tags in sentences:
                context = START + [self._normalize(w) for w in words] + END
                for i, word in enumerate(words):
                    guess = self.tagdict.get(word)
                    if not guess:
                        feats = self._get_features(i, word, context, prev, prev2)
                        guess = self.model.predict(feats)
                        self.model.update(tags[i], guess, feats)
                    prev2 = prev; prev = guess
                    c += guess == tags[i]; n += 1
            random.shuffle(sentences)
            if not quiet:
                print("Iter %d: %d/%d=%.3f" % (iter_, c, n, _pc(c, n)))
        self.model.average_weights()
        # Pickle as a binary file
        if save_loc is not None:
            pickle.dump((self.model.weights, self.tagdict, self.classes),
                         open(save_loc, 'wb'), -1)

    def load(self, loc):
        w_td_c = pickle.load(open(loc, 'rb'))
        self.model.weights, self.tagdict, self.classes = w_td_c
        self.model.classes = self.classes

    def _normalize(self, word):
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
        trained.'''
        def add(name, *args):
            features[' '.join((name,) + tuple(args))] += 1

        i += len(START)
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

    def _make_tagdict(self, sentences, quiet=False):
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
