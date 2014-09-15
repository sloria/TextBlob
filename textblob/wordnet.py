# -*- coding: utf-8 -*-
'''Wordnet interface. Contains classes for creating Synsets and Lemmas
directly.

.. versionadded:: 0.7.0

.. data:: wordnet

    NLTK's wordnet module.

.. data:: Synset

    Synset constructor.

.. data:: Lemma

    Lemma constructor.
'''
import nltk

wordnet = nltk.corpus.wordnet
Synset = nltk.corpus.wordnet.synset
Lemma = nltk.corpus.wordnet.lemma
# Part of speech constants
VERB, NOUN, ADJ, ADV = wordnet.VERB, wordnet.NOUN, wordnet.ADJ, wordnet.ADV
