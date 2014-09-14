.. _classifiers:

Tutorial: Building a Text Classification System
***********************************************

The ``textblob.classifiers`` module makes it simple to create custom classifiers.

As an example, let's create a custom sentiment analyzer.

Loading Data and Creating a Classifier
======================================

First we'll create some training and test data.


.. doctest::

    >>> train = [
    ...     ('I love this sandwich.', 'pos'),
    ...     ('this is an amazing place!', 'pos'),
    ...     ('I feel very good about these beers.', 'pos'),
    ...     ('this is my best work.', 'pos'),
    ...     ("what an awesome view", 'pos'),
    ...     ('I do not like this restaurant', 'neg'),
    ...     ('I am tired of this stuff.', 'neg'),
    ...     ("I can't deal with this", 'neg'),
    ...     ('he is my sworn enemy!', 'neg'),
    ...     ('my boss is horrible.', 'neg')
    ... ]
    >>> test = [
    ...     ('the beer was good.', 'pos'),
    ...     ('I do not enjoy my job', 'neg'),
    ...     ("I ain't feeling dandy today.", 'neg'),
    ...     ("I feel amazing!", 'pos'),
    ...     ('Gary is a friend of mine.', 'pos'),
    ...     ("I can't believe I'm doing this.", 'neg')
    ... ]

Now we'll create a Naive Bayes classifier, passing the training data into the constructor.

.. doctest::

    >>> from textblob.classifiers import NaiveBayesClassifier
    >>> cl = NaiveBayesClassifier(train)

.. _data_files:

Loading Data from Files
-----------------------

You can also load data from common file formats including CSV, JSON, and TSV.

CSV files should be formatted like so:
::

    I love this sandwich.,pos
    This is an amazing place!,pos
    I do not like this restaurant,neg

JSON files should be formatted like so:

::

    [
        {"text": "I love this sandwich.", "label": "pos"},
        {"text": "This is an amazing place!", "label": "pos"},
        {"text": "I do not like this restaurant", "label": "neg"}
    ]

You can then pass the opened file into the constructor.

::

    >>> with open('train.json', 'r') as fp:
    ...     cl = NaiveBayesClassifier(fp, format="json")

Classifying Text
================

Call the ``classify(text)`` method to use the classifier.

.. doctest::

    >>> cl.classify("This is an amazing library!")
    'pos'

You can get the label probability distribution with the ``prob_classify(text)`` method.

.. doctest::

    >>> prob_dist = cl.prob_classify("This one's a doozy.")
    >>> prob_dist.max()
    'pos'
    >>> round(prob_dist.prob("pos"), 2)
    0.63
    >>> round(prob_dist.prob("neg"), 2)
    0.37

Classifying TextBlobs
=====================

Another way to classify text is to pass a classifier into the constructor of ``TextBlob`` and call its ``classify()`` method.

.. doctest::

    >>> from textblob import TextBlob
    >>> blob = TextBlob("The beer is good. But the hangover is horrible.", classifier=cl)
    >>> blob.classify()
    'pos'

The advantage of this approach is that you can classify sentences within a ``TextBlob``.

.. doctest::

    >>> for s in blob.sentences:
    ...     print(s)
    ...     print(s.classify())
    ...
    The beer is good.
    pos
    But the hangover is horrible.
    neg

Evaluating Classifiers
======================

To compute the accuracy on our test set, use the ``accuracy(test_data)`` method.

.. doctest::

    >>> cl.accuracy(test)
    0.8333333333333334

.. note::

    You can also pass in a file object into the ``accuracy`` method. The file can be in any of the formats listed in the :ref:`Loading Data <data_files>` section.

Use the ``show_informative_features()`` method to display a listing of the most informative features.

.. doctest::

    >>> cl.show_informative_features(5)  # doctest: +SKIP
    Most Informative Features
                contains(my) = True              neg : pos    =      1.7 : 1.0
                contains(an) = False             neg : pos    =      1.6 : 1.0
                 contains(I) = True              neg : pos    =      1.4 : 1.0
                 contains(I) = False             pos : neg    =      1.4 : 1.0
                contains(my) = False             pos : neg    =      1.3 : 1.0

Updating Classifiers with New Data
==================================

Use the ``update(new_data)`` method to update a classifier with new training data.

.. doctest::

    >>> new_data = [('She is my best friend.', 'pos'),
    ...             ("I'm happy to have a new friend.", 'pos'),
    ...             ("Stay thirsty, my friend.", 'pos'),
    ...             ("He ain't from around here.", 'neg')]
    >>> cl.update(new_data)
    True
    >>> cl.accuracy(test)
    1.0

Feature Extractors
==================

By default, the ``NaiveBayesClassifier`` uses a simple feature extractor that indicates which words in the training set are contained in a document.

For example, the sentence *"I feel happy"* might have the features ``contains(happy): True`` or ``contains(angry): False``.

You can override this feature extractor by writing your own. A feature extractor is simply a function with ``document`` (the text to extract features from) as the first argument. The function may include a second argument, ``train_set`` (the training dataset), if necessary.

The function should return a dictionary of features for ``document``.

For example, let's create a feature extractor that just uses the first and last words of a document as its features.

.. doctest::

    >>> def end_word_extractor(document):
    ...     tokens = document.split()
    ...     first_word, last_word = tokens[0], tokens[-1]
    ...     feats = {}
    ...     feats["first({0})".format(first_word)] = True
    ...     feats["last({0})".format(last_word)] = False
    ...     return feats
    >>> features = end_word_extractor("I feel happy")
    >>> assert features == {'last(happy)': False, 'first(I)': True}

We can then use the feature extractor in a classifier by passing it as the second argument of the constructor.

.. doctest::

    >>> cl2 = NaiveBayesClassifier(test, feature_extractor=end_word_extractor)
    >>> blob = TextBlob("I'm excited to try my new classifier.", classifier=cl2)
    >>> blob.classify()
    'pos'

Next Steps
==========

Be sure to check out the :ref:`API Reference <api_classifiers>` for the :ref:`classifiers module <api_classifiers>`.

Want to try different POS taggers or noun phrase chunkers with TextBlobs? Check out the :ref:`Advanced Usage <advanced>` guide.
