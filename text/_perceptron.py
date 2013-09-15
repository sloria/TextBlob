"""
Averaged perceptron classifier. Implementation geared for simplicity rather than
efficiency.

.. versionadded:: 0.6.3
"""
from collections import defaultdict
import pickle
import random


class AveragedPerceptron(object):

    '''An averaged perceptron, as implemented by Matthew Honnibal.

    See more implementation details here:
        http://honnibal.wordpress.com/2013/09/11/a-good-part-of-speechpos-tagger-in-about-200-lines-of-python/
    '''

    def __init__(self):
        # Each feature gets its own weight vector, so weights is a dict-of-dicts
        self.weights = {}
        self.classes = set()
        # The accumulated values, for the averaging. These will be keyed by
        # feature/clas tuples
        self._totals = defaultdict(int)
        # The last time the feature was changed, for the averaging. Also
        # keyed by feature/clas tuples
        # (tstamps is short for timestamps)
        self._tstamps = defaultdict(int)
        # Number of instances seen
        self.i = 0

    def predict(self, features):
        '''Dot-product the features and current weights and return the best label.'''
        scores = defaultdict(float)
        for feat, value in features.items():
            if feat not in self.weights or value == 0:
                continue
            weights = self.weights[feat]
            for label, weight in weights.items():
                scores[label] += value * weight
        # Do a secondary alphabetic sort, for stability
        return max(self.classes, key=lambda label: (scores[label], label))

    def update(self, truth, guess, features):
        '''Update the feature weights.'''
        def upd_feat(c, f, w, v):
            param = (f, c)
            self._totals[param] += (self.i - self._tstamps[param]) * w
            self._tstamps[param] = self.i
            self.weights[f][c] = w + v

        self.i += 1
        if truth == guess:
            return None
        for f in features:
            weights = self.weights.setdefault(f, {})
            upd_feat(truth, f, weights.get(truth, 0.0), 1.0)
            upd_feat(guess, f, weights.get(guess, 0.0), -1.0)
        return None

    def average_weights(self):
        '''Average weights from all iterations.'''
        for feat, weights in self.weights.items():
            new_feat_weights = {}
            for clas, weight in weights.items():
                param = (feat, clas)
                total = self._totals[param]
                total += (self.i - self._tstamps[param]) * weight
                averaged = round(total / float(self.i), 3)
                if averaged:
                    new_feat_weights[clas] = averaged
            self.weights[feat] = new_feat_weights
        return None

    def save(self, path):
        '''Save the pickled model weights.'''
        return pickle.dump(dict(self.weights), open(path, 'w'))

    def load(self, path):
        '''Load the pickled model weights.'''
        self.weights = pickle.load(open(path))
        return None


def train(nr_iter, examples):
    '''Return an averaged perceptron model trained on ``examples`` for
    ``nr_iter`` iterations.
    '''
    model = AveragedPerceptron()
    for i in range(nr_iter):
        random.shuffle(examples)
        for features, class_ in examples:
            scores = model.predict(features)
            guess, score = max(scores.items(), key=lambda i: i[1])
            if guess != class_:
                model.update(class_, guess, features)
    model.average_weights()
    return model
