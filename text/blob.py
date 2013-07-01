# -*- coding: utf-8 -*-
'''Wrappers for various units of text.'''
import re
import sys
from collections import Counter

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from .np_extractor import NPExtractor
from .decorators import cached_property


class BaseBlob(object):
    '''An abstract base class that all text.blob classes will inherit from.
    Includes words, POS tag, NP, and word count properties. Also includes 
    basic dunder and string methods for making objects like Python strings.
    '''
    
    _REPLACE_REGEX = '(\n|\!|\?|\(|\)|\-|\,|\.|\;|\t|\r)'

    def __init__(self, text):
        self.raw = text
        self.stripped = self._lowerstrip(text)

    @cached_property 
    def words(self):
        '''Returns list of word tokens. These are extracted only once, when
        this property is first accessed, then it is stored in an instance 
        variable.
        '''
        return word_tokenize(self.raw)

    @cached_property
    def noun_phrases(self):
        extractor = NPExtractor(self.raw)
        return [self._lowerstrip(phrase)
                                for phrase in extractor.extract()
                                if len(phrase) > 1]

    @cached_property
    def pos_tags(self):
        '''Returns an array of tuples of the form (word, POS tag).
        
        Example:
            [('At', 'IN'), ('eight', 'CD'), ("o'clock", 'JJ'), ('on', 'IN'),
                    ('Thursday', 'NNP'), ('morning', 'NN')]
        '''
        tokens = word_tokenize(self.stripped)
        return nltk.pos_tag(tokens)

    @cached_property
    def word_counts(self):
        '''Dictionary of word frequencies in this text. Internally
        uses collections.Counter.
        '''
        stripped_words = [self._lowerstrip(word) for word in self.words]
        return Counter(stripped_words)

    @cached_property
    def np_counts(self):
        '''Dictionary of noun phrase frequencies in this text. Internally
        uses collections.Counter.
        '''
        return Counter(self.noun_phrases)

    def __repr__(self):
        '''Returns a string representation for debugging.'''
        class_name = self.__class__.__name__
        if len(self) > 60:
            return "{cls}('{beginning}...{end}')"\
                        .format(cls=class_name,
                                beginning=self.raw[:40], end=self.raw[-20:])
        else:
            return "{cls}('{text}')".format(cls=class_name, text=self.raw)

    def __len__(self):
        '''Returns the length of the raw text.'''
        return len(self.raw)

    def __str__(self):
        '''Returns a string representation used in print statements
        or str(my_blob).'''
        return self.raw

    def __iter__(self):
        '''Makes the object iterable as if it were a string,
        iterating through the raw string's characters.
        '''
        return iter(self.raw)

    def __cmp__(self, other):
        '''Compare to another object. Indirectly supports '==', '<', etc.'''
        return cmp(str(self), str(other))

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
        if isinstance(other, basestring):
            return TextBlob(str(self) + other)
        elif isinstance(other, BaseBlob):
            return TextBlob(str(self) + str(other))
        else:
            raise ValueError('Operands must be either strings or {0} objects'
                                .format(self.__class__.__name__))

    def find(self, sub, start=0, end=sys.maxint):
        '''Behaves like the built-in str.find() method. Returns an integer,
        the index of the first occurrence of the substring argument sub in the
        sub-string given by [start:end]
        '''
        return str(self).find(sub, start, end)

    def upper(self):
        return self.__class__(self.raw.upper())

    def lower(self):
        return self.__class__(self.raw.lower())

    def _lowerstrip(self, text):
        '''Makes text all lowercase and strips punctuation.'''
        return re.sub(BaseBlob._REPLACE_REGEX, '', 
                        text.lower()).strip()


class TextBlob(BaseBlob):
    """A general text block, meant for larger bodies of text (esp. those
    containing sentences.
    """
    def __init__(self, blob):
        '''Initialize a textblob.

        Arguments:
        - `blob`: a string
        '''
        super(TextBlob, self).__init__(blob)

    @cached_property
    def sentences(self):
        '''List of Sentence objects.'''
        return self._create_sentence_objects(self.raw)

    @property
    def raw_sentences(self):
        '''List of strings, the raw sentences in the blob.'''
        return [sentence.raw for sentence in self.sentences]

    @property
    def serialized(self):
        '''Returns a list of each sentences dict representation.'''
        return [sentence.dict for sentence in self.sentences]

    def _create_sentence_objects(self, blob):
        '''Returns a list of Sentence objects given 
        a list of sentence strings. Attempts to handle sentences that
        have more than one puntuation mark at the end of the sentence.
        Examples: "An ellipses is no problem..." or "This is awesome!!!"
        '''
        sentence_objects = []
        sentences = sent_tokenize(blob)  # List of raw sentences
        # if there is only one sentence or string of text
        if len(sentences) <= 1:
            sentence_objects.append(
                Sentence(sentences[0], start_index=0, 
                            end_index=len(sentences[0]) - 1)
            )
        # If there are many sentences 
        else:     
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
                    next = sentences[i + 1]  # the next token
                except IndexError:
                    # Continue if the last token is a punctuation
                    if len(raw_sentence) <= 1:
                        continue
                    pass
                # If the next token has a length of 1, assume it's a punctuation
                if len(next) == 1: 
                    raw_sentence += next  # append the extra punctuation
                    char_index +=1  # also correct the char_index
                # Create a Sentence object and add it the the list
                sentence_objects.append(
                    Sentence(raw_sentence, start_index=start_index, 
                                            end_index=char_index))
        return sentence_objects


class Sentence(BaseBlob):
    '''A sentence within a TextBlob.'''
    def __init__(self, sentence, start_index=0, end_index=None):
        '''Initialize a Sentence.

        Arguments:
        - `sentence`: A string, the raw sentence.
        - `start_index`: An int, the index where this sentence begins
                            in a TextBlob. If not given, defaults to 0.
        - `end_index`: An int, the index where this sentence ends in 
                            a TextBlob. If not given, defaults to the
                            length of the sentence - 1.
        '''
        super(Sentence, self).__init__(sentence)
        self.start_index = start_index
        self.end_index = end_index if end_index else len(sentence) - 1

    @property
    def dict(self):
        '''The dict representation of this sentence.'''
        return {
            "raw_sentence": self.raw,
            "start_index": self.start_index,
            "end_index": self.end_index,
            "stripped_sentence": self.stripped,
            "noun_phrases": self.noun_phrases
        }

