# -*- coding: utf-8 -*-
'''Various tokenizer implementations.

.. versionadded:: 0.4.0
'''
from __future__ import absolute_import
from text.packages import nltk
from text.utils import strip_punc
from text.exceptions import MissingCorpusException


class BaseTokenizer(nltk.tokenize.api.TokenizerI):

    '''Abstract base class from which all Tokenizer classes inherit.

    Descendant classes should implement an API like so: ::

        >>> from text.tokenizers import MyTokenizer
        >>> tokenizer = MyTokenizer()
        >>> text = "I am a sentence."
        >>> tokenizer.tokenize(text)
        ['I', 'am', 'a', 'sentence.']

    In other words, descendant classes must implement a ``tokenize(text)`` method
    that returns a list of noun phrases as strings.
    '''

    def tokenize(self, text):
        '''Return a list of tokens (strings) for a body of text.

        :rtype: list
        '''
        raise NotImplementedError('Must implement a tokenize(text) method')

    def itokenize(self, text, *args, **kwargs):
        '''Return a generator that generates tokens "on-demand".

        .. versionadded:: 0.6.0

        :rtype: generator
        '''
        return (t for t in self.tokenize(text, *args, **kwargs))


class WordTokenizer(BaseTokenizer):

    '''NLTK's recommended word tokenizer (currently the TreeBankTokenizer).
    Uses regular expressions to tokenize text. Assumes text has already been
    segmented into sentences.

    Performs the following steps:

    * split standard contractions, e.g. don't -> do n't
    * split commas and single quotes
    * separate periods that appear at the end of line
    '''

    def tokenize(self, text, include_punc=True):
        '''Return a list of word tokens.

        :param text: string of text.
        :param include_punc: (optional) whether to include punctuation as separate tokens. Default to True.
        '''
        tokens = nltk.tokenize.word_tokenize(text)
        if include_punc:
            return tokens
        else:
            # Return each word token
            # Strips punctuation unless the word comes from a contraction
            # e.g. "Let's" => ["Let", "'s"]
            # e.g. "Can't" => ["Ca", "n't"]
            # e.g. "home." => ['home']
            return [word if word.startswith("'") else strip_punc(word, all=False)
                    for word in tokens if strip_punc(word, all=False)]

class SentenceTokenizer(BaseTokenizer):

    '''NLTK's sentence tokenizer (currently PunkSentenceTokenizer).
    Uses an unsupervised algorithm to build a model for abbreviation owrds,
    collocations, and words, collocations, and words, that start sentences,
    then uses that to find sentence boundaries.
    Tweaked slightly to make it more robust to sentences with multiple
    punctuation at the end, e.g. "OMG! I am so LOL!!!"
    '''

    def tokenize(self, text):
        '''Return a list of sentences.'''
        ret = []
        try:
            sentences = nltk.tokenize.sent_tokenize(text)  # Initial tokenization
        except LookupError as err:
            print(err)
            raise MissingCorpusException()
        # If there's only one sentence or string of text
        if len(sentences) <= 1:
            return sentences  # return the 1-element list
        else:
            for i, sentence in enumerate(sentences):
                # Sometimes the NLTK tokenizer misses some punctuation when
                # there are multiple punctuations, e.g. with ellipses ("...")
                # or multiple exclamation points ("!!!")
                try:
                    next_token = sentences[i + 1]
                except IndexError:
                    # Continue if the last token is a punctuation
                    if len(sentence) <= 1:
                        continue
                # If the next token is 1 character, assume it's a punctuation
                if len(next_token) == 1:
                    sentence = "".join([sentence, next_token]) # append the extra punctuation
                ret.append(sentence)
        return ret
