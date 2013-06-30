# -*- coding: utf-8 -*-
"""
Tests for the text processor.
"""
from unittest import TestCase
from datetime import datetime
from nose.tools import *  # PEP8 asserts
from text.blob import TextBlob, Sentence


class SentenceTest(TestCase):
    def setUp(self):
        self.raw_sentence = "Any place with frites and Belgian beer has my vote."
        self.sentence = Sentence(self.raw_sentence)

    def test_stripped_sentence(self):
        assert_equal(self.sentence.stripped, 
                        "any place with frites and belgian beer has my vote")

    def test_len(self):
        assert_equal(len(self.sentence), len(self.raw_sentence))

    def test_dict(self):
        sentence_dict = self.sentence.dict
        assert_equal(sentence_dict, 
                    {
                        "raw_sentence": self.raw_sentence,
                        "start_index": 0,
                        "end_index": len(self.raw_sentence) - 1,
                        "stripped_sentence": "any place with frites and belgian beer has my vote",
                        "noun_phrases": self.sentence.noun_phrases
                    })

    def test_pos_tags(self):
        then1 = datetime.now()
        tagged = self.sentence.pos_tags
        now1 = datetime.now()
        t1 = now1 - then1

        then2 = datetime.now()
        tagged = self.sentence.pos_tags
        now2 = datetime.now()
        t2 = now2 - then2

        # Getting the pos tags the second time should be faster
        # because they were stored as an attribute the first time
        assert_true(t2 < t1)

        print(tagged)
        assert_equal(tagged, 
                    [('any', 'DT'), ('place', 'NN'), ('with', 'IN'), 
                    ('frites', 'NNS'), ('and', 'CC'), ('belgian', 'JJ'), 
                    ('beer', 'NN'), ('has', 'VBZ'), ('my', 'PRP$'), 
                    ('vote', 'NN')])

    def test_noun_phrases(self):
        nps = self.sentence.noun_phrases
        assert_equal(nps, ['belgian beer'])


class TextBlobTest(TestCase):
    def setUp(self):
        self.text = """Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""

    def tearDown(self):
        pass

    def test_init(self):
        blob = TextBlob("Wow I love this place. It really rocks my socks!!!")
        assert_equal(len(blob.sentences), 2)
        assert_equal(blob.sentences[1].stripped,
                        'it really rocks my socks')

    def test_sentences(self):
        blob = TextBlob(self.text)
        assert_equal(len(blob.sentences), 19)

        assert_true(isinstance(blob.sentences[0], Sentence))

    def test_blob_with_no_sentences(self):
        text = "this isn't really a sentence it's just a long string of words"
        blob = TextBlob(text)
        # the blob just has one sentence
        assert_equal(len(blob.sentences), 1)
        # the start index is 0, the end index is len(text) - 1
        assert_equal(blob.sentences[0].start_index, 0)
        assert_equal(blob.sentences[0].end_index, len(text) - 1)

    def test_len(self):
        blob = TextBlob("lorem ipsum")
        assert_equal(len(blob), len("lorem ipsum"))

    def test_repr(self):
        blob1 = TextBlob('lorem ipsum')
        assert_equal(repr(blob1), "TextBlob('lorem ipsum')")
        big_blob = TextBlob(self.text)
        print(repr(big_blob))
        assert_equal(repr(big_blob), 
                    "TextBlob('Beautiful is better than ugly.\nExplicit ...'s"
                    " do more of those!')")

    def test_cmp(self):
        blob1 = TextBlob('lorem ipsum')
        blob2 = TextBlob('lorem ipsum')
        blob3 = TextBlob('dolor sit amet')

        assert_true(blob1 == blob2) # test ==
        assert_true(blob1 > blob3)  # test >
        assert_true(blob3 < blob2)  # test <    

    def test_words(self):
        blob = TextBlob("Beautiful is better than ugly. Explicit is better "
                        "than implicit.")
        assert_equal(blob.words, ['Beautiful', 'is', 'better', 'than', 'ugly.', 
                        'Explicit', 'is', 'better', 'than', 'implicit', '.'])

    def test_pos_tags(self):
        blob = TextBlob("Simple is better than complex. Complex is better "
                        "than complicated.")
        
        assert_equal(blob.pos_tags,
            [('simple', 'NN'), ('is', 'VBZ'), ('better', 'RBR'), ('than', 'IN'),
             ('complex', 'JJ'), ('complex', 'NN'), ('is', 'VBZ'), 
             ('better', 'RBR'), ('than', 'IN'), ('complicated', 'VBN')])

    def test_getitem(self):
        blob = TextBlob('lorem ipsum')
        assert_equal(blob[0], 'l')
        assert_equal(blob[0:5], TextBlob('lorem'))

    def test_upper(self):
        blob = TextBlob('lorem ipsum')
        assert_equal(blob.upper(), TextBlob("LOREM IPSUM"))

    def test_lower(self):
        blob = TextBlob('Lorem Ipsum')
        assert_equal(blob.lower(), TextBlob('lorem ipsum'))

    def test_find(self):
        text = 'Beautiful is better than ugly.'
        blob = TextBlob(text)
        assert_equal(blob.find("better", 5, len(blob)),
                    text.find("better", 5, len(text)))

    def test_indices(self):
        blob = TextBlob(self.text)
        first_sentence = blob.sentences[0]
        second_sentence = blob.sentences[1]
        last_sentence = blob.sentences[len(blob.sentences) - 1]
        assert_equal(first_sentence.start_index, 0)
        assert_equal(first_sentence.end_index, 30)

        assert_equal(second_sentence.start_index, 30)
        assert_equal(second_sentence.end_index, 63)

        assert_equal(last_sentence.start_index, 740)
        assert_equal(last_sentence.end_index, 804)

    def test_multiple_punctuation_at_end_of_sentence(self):
        '''Test sentences that have multiple punctuation marks
        at the end of the sentence.'''
        blob = TextBlob("Get ready! This has an ellipses...")
        assert_equal(len(blob.sentences), 2)
        assert_equal(blob.sentences[1].raw,
                    "This has an ellipses...")
        blob2 = TextBlob("OMG! I am soooo LOL!!!")
        assert_equal(len(blob2.sentences), 2)
        assert_equal(blob2.sentences[1].raw,
                    "I am soooo LOL!!!")

    def test_blob_noun_phrases(self):
        blob = TextBlob(self.text)
        assert_equal(blob.noun_phrases,
                    ['beautiful', 'explicit', 'simple', 
                    'complex', 'flat', 'sparse', 'readability', 
                    'special cases', 'practicality beats purity', 'errors', 
                    'unless', 'obvious way', 'dutch', '*right* now', 
                    'bad idea', 'good idea', 'namespaces', 'great idea'])

    def test_word_counts(self):
        blob = TextBlob("Buffalo buffalo ate my blue buffalo.")
        assert_equal(blob.word_counts['buffalo'], 3)
        assert_equal(blob.word_counts['blue'], 1)
        assert_equal(blob.word_counts['ate'], 1)
        assert_equal(blob.word_counts['buff'], 0)

    def test_np_counts(self):
        # Add some text so that we have a noun phrase that
        # has a frequency greater than 1
        blob = TextBlob(self.text + "That's a great idea.")
        assert_equal(blob.np_counts['namespaces'], 1)
        assert_equal(blob.np_counts['great idea'], 2)

    def test_add(self):
        blob1 = TextBlob("Hello, world! ")
        blob2 = TextBlob("Hola mundo!")
        # Can add two text blobs
        assert_equal(blob1 + blob2, TextBlob("Hello, world! Hola mundo!"))
        # Can also add a string to a TextBlob
        assert_equal(blob1 + 'Hola mundo!', 
                    TextBlob("Hello, world! Hola mundo!"))
        # Or both
        assert_equal(blob1 + blob2 + " Goodbye!",
             TextBlob("Hello, world! Hola mundo! Goodbye!"))

    def test_sentences_after_concatenation(self):
        blob1 = TextBlob("Beautiful is better than ugly. ")
        blob2 = TextBlob("Explicit is better than implicit.")

        concatenated = blob1 + blob2
        print(concatenated)
        assert_equal(len(concatenated.sentences), 2)

