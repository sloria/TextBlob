# -*- coding: utf-8 -*-

"""
Tests for the text processor.
"""
import json
from unittest import TestCase, main
from datetime import datetime
from nose.tools import *  # PEP8 asserts
from text.blob import TextBlob, Sentence, WordList


class WordListTest(TestCase):

    def setUp(self):
        self.words = 'Beautiful is better than ugly'.split()
        self.mixed = ['dog', 'dogs', 'blob', 'Blobs', 'text']

    def test_len(self):
        wl = WordList(['Beautiful', 'is', 'better'])
        assert_equal(len(wl), 3)

    def test_slicing(self):
        wl = WordList(self.words)
        first = wl[0]
        assert_true(isinstance(first, str))
        assert_equal(first, 'Beautiful')

        dogs = wl[0:2]
        assert_true(isinstance(dogs, WordList))
        assert_equal(dogs, WordList(['Beautiful', 'is']))

    def test_repr(self):
        wl = WordList(['Beautiful', 'is', 'better'])
        assert_equal(repr(wl), "WordList(['Beautiful', 'is', 'better'])")

    def test_singularize(self):
        wl = WordList(['dogs', 'cats', 'buffaloes', 'men', 'mice'])
        assert_equal(wl.singularize(), ['dog', 'cat', 'buffalo', 'man', 'mouse'
                     ])

    def test_pluralize(self):
        wl = WordList(['dog', 'cat', 'buffalo'])
        assert_equal(wl.pluralize(), ['dogs', 'cats', 'buffaloes'])

    def test_lower(self):
        wl = WordList(['Zen', 'oF', 'PYTHON'])
        assert_equal(wl.lower(), WordList(['zen', 'of', 'python']))

    def test_count(self):
        wl = WordList(['monty', 'python', 'Python', 'Monty'])
        assert_equal(wl.count('monty'), 2)
        assert_equal(wl.count('monty', case_sensitive=True), 1)
        assert_equal(wl.count('mon'), 0)


class SentenceTest(TestCase):

    def setUp(self):
        self.raw_sentence = \
            'Any place with frites and Belgian beer has my vote.'
        self.sentence = Sentence(self.raw_sentence)

    def test_repr(self):
        assert_equal(repr(self.sentence),
                     "Sentence('{0}')".format(self.raw_sentence))

    def test_stripped_sentence(self):
        assert_equal(self.sentence.stripped,
                     'any place with frites and belgian beer has my vote')

    def test_len(self):
        assert_equal(len(self.sentence), len(self.raw_sentence))

    def test_dict(self):
        sentence_dict = self.sentence.dict
        assert_equal(sentence_dict, {
            'raw': self.raw_sentence,
            'start_index': 0,
            'sentiment': (0.0, 0.0),
            'end_index': len(self.raw_sentence) - 1,
            'stripped': 'any place with frites and belgian beer has my vote',
            'noun_phrases': self.sentence.noun_phrases,
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
        assert_equal(tagged,
                [(u'Any', u'DT'), (u'place', u'NN'), (u'with', u'IN'),
                (u'frites', u'NNS'), (u'and', u'CC'), (u'Belgian', u'JJ'),
                (u'beer', u'NN'), (u'has', u'VBZ'), (u'my', u'PRP$'),
                (u'vote', u'NN')]
        )

    def test_noun_phrases(self):
        nps = self.sentence.noun_phrases
        assert_equal(nps, ['belgian beer'])


class TextBlobTest(TestCase):

    def setUp(self):
        self.text = \
            """Beautiful is better than ugly.
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
        blob = TextBlob('Wow I love this place. It really rocks my socks!!!')
        assert_equal(len(blob.sentences), 2)
        assert_equal(blob.sentences[1].stripped, 'it really rocks my socks')

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
        blob = TextBlob('lorem ipsum')
        assert_equal(len(blob), len('lorem ipsum'))

    def test_repr(self):
        blob1 = TextBlob('lorem ipsum')
        assert_equal(repr(blob1), "TextBlob('lorem ipsum')")
        big_blob = TextBlob(self.text)
        assert_equal(repr(big_blob),
                     "TextBlob('Beautiful is better than ugly.\nExplicit ...'s do more of those!')"
                     )

    def test_cmp(self):
        blob1 = TextBlob('lorem ipsum')
        blob2 = TextBlob('lorem ipsum')
        blob3 = TextBlob('dolor sit amet')

        assert_true(blob1 == blob2)  # test ==
        assert_true(blob1 > blob3)  # test >
        assert_true(blob3 < blob2)  # test <

    def test_words(self):
        blob = \
            TextBlob('Beautiful is better than ugly. Explicit is better than implicit.'
                     )
        assert_true(isinstance(blob.words, WordList))
        assert_equal(blob.words, WordList([
            'Beautiful',
            'is',
            'better',
            'than',
            'ugly',
            'Explicit',
            'is',
            'better',
            'than',
            'implicit',
            ]))

    def test_pos_tags(self):
        blob = \
            TextBlob('Simple is better than complex. Complex is better than complicated.'
                     )
        print(blob.pos_tags)
        assert_equal(blob.pos_tags, WordList([
            (u'Simple', u'NN'),
            (u'is', u'NNS'),
            (u'better', u'JJR'),
            (u'than', u'IN'),
            (u'complex', u'NN'),
            (u'Complex', u'NNP'),
            (u'is', u'VBZ'),
            (u'better', u'RBR'),
            (u'than', u'IN'),
            (u'complicated', u'VBN'),
            ]))

    def test_getitem(self):
        blob = TextBlob('lorem ipsum')
        assert_equal(blob[0], 'l')
        assert_equal(blob[0:5], TextBlob('lorem'))

    def test_upper(self):
        blob = TextBlob('lorem ipsum')
        assert_true(is_blob(blob.upper()))
        assert_equal(blob.upper(), TextBlob('LOREM IPSUM'))

    def test_upper_and_words(self):
        blob = TextBlob('beautiful is better')
        assert_equal(blob.upper().words, WordList(['BEAUTIFUL', 'IS', 'BETTER'
                     ]))

    def test_lower(self):
        blob = TextBlob('Lorem Ipsum')
        assert_true(is_blob(blob.lower()))
        assert_equal(blob.lower(), TextBlob('lorem ipsum'))

    def test_find(self):
        text = 'Beautiful is better than ugly.'
        blob = TextBlob(text)
        assert_equal(blob.find('better', 5, len(blob)), text.find('better', 5,
                     len(text)))

    def test_rfind(self):
        text = 'Beautiful is better than ugly. '
        blob = TextBlob(text)
        assert_equal(blob.rfind('better'), text.rfind('better'))

    def test_startswith(self):
        blob = TextBlob(self.text)
        assert_true(blob.startswith('Beautiful'))
        assert_true(blob.starts_with('Beautiful'))

    def test_endswith(self):
        blob = TextBlob(self.text)
        assert_true(blob.endswith('of those!'))
        assert_true(blob.ends_with('of those!'))

    def test_split(self):
        blob = TextBlob('Beautiful is better')
        assert_equal(blob.split(), WordList(['Beautiful', 'is', 'better']))

    def test_title(self):
        blob = TextBlob('Beautiful is better')
        assert_equal(blob.title(), TextBlob('Beautiful Is Better'))

    def test_format(self):
        blob = TextBlob('1 + 1 = {0}')
        assert_equal(blob.format(1 + 1), TextBlob('1 + 1 = 2'))
        assert_equal('1 + 1 = {0}'.format(TextBlob('2')), '1 + 1 = 2')

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

    def test_indices_short_names(self):
        blob = TextBlob(self.text)
        last_sentence = blob.sentences[len(blob.sentences) - 1]
        assert_equal(last_sentence.start, 740)
        assert_equal(last_sentence.end, 804)

    def test_replace(self):
        blob = TextBlob('textblob is a blobby blob')
        assert_equal(blob.replace('blob', 'bro'),
                     TextBlob('textbro is a broby bro'))
        assert_equal(blob.replace('blob', 'bro', 1),
                     TextBlob('textbro is a blobby blob'))

    def test_join(self):
        l = ['explicit', 'is', 'better']
        wl = WordList(l)
        assert_equal(TextBlob(' ').join(l), TextBlob('explicit is better'))
        assert_equal(TextBlob(' ').join(wl), TextBlob('explicit is better'))

    def test_multiple_punctuation_at_end_of_sentence(self):
        '''Test sentences that have multiple punctuation marks
        at the end of the sentence.'''
        blob = TextBlob('Get ready! This has an ellipses...')
        assert_equal(len(blob.sentences), 2)
        assert_equal(blob.sentences[1].raw, 'This has an ellipses...')
        blob2 = TextBlob('OMG! I am soooo LOL!!!')
        assert_equal(len(blob2.sentences), 2)
        assert_equal(blob2.sentences[1].raw, 'I am soooo LOL!!!')

    def test_blob_noun_phrases(self):
        blob = TextBlob(self.text)
        assert_true(isinstance(blob.noun_phrases, WordList))
        assert_equal(blob.noun_phrases, WordList([
            'beautiful',
            'explicit',
            'simple',
            'complex',
            'flat',
            'sparse',
            'readability',
            'special cases',
            'practicality beats purity',
            'errors',
            'unless',
            'obvious way',
            'dutch',
            'right now',
            'bad idea',
            'good idea',
            'namespaces',
            'great idea',
            ]))

    def test_word_counts(self):
        blob = TextBlob('Buffalo buffalo ate my blue buffalo.')
        assert_equal(blob.word_counts['buffalo'], 3)
        assert_equal(blob.words.count('buffalo'), 3)
        assert_equal(blob.words.count('buffalo', case_sensitive=True), 2)
        assert_equal(blob.word_counts['blue'], 1)
        assert_equal(blob.words.count('blue'), 1)
        assert_equal(blob.word_counts['ate'], 1)
        assert_equal(blob.words.count('ate'), 1)
        assert_equal(blob.word_counts['buff'], 0)
        assert_equal(blob.words.count('buff'), 0)

        blob2 = TextBlob(self.text)
        assert_equal(blob2.words.count('special'), 2)
        assert_equal(blob2.words.count('special', case_sensitive=True), 1)

    def test_np_counts(self):
        # Add some text so that we have a noun phrase that
        # has a frequency greater than 1
        blob = TextBlob(self.text + "That's a great idea.")
        assert_equal(blob.noun_phrases.count('namespaces'), 1)
        assert_equal(blob.noun_phrases.count('great idea'), 2)
        assert_equal(blob.np_counts['not_found'], 0)
        assert_equal(blob.noun_phrases.count('not found'), 0)

    def test_add(self):
        blob1 = TextBlob('Hello, world! ')
        blob2 = TextBlob('Hola mundo!')
        # Can add two text blobs
        assert_equal(blob1 + blob2, TextBlob('Hello, world! Hola mundo!'))
        # Can also add a string to a TextBlob
        assert_equal(blob1 + 'Hola mundo!',
                     TextBlob('Hello, world! Hola mundo!'))
        # Or both
        assert_equal(blob1 + blob2 + ' Goodbye!',
                     TextBlob('Hello, world! Hola mundo! Goodbye!'))

    def test_unicode(self):
        blob = TextBlob(self.text)
        assert_equal(str(blob), str(self.text))

    def test_strip(self):
        text = 'Beautiful is better than ugly. '
        blob = TextBlob(text)
        assert_true(is_blob(blob))
        assert_equal(blob.strip(), TextBlob(text.strip()))

    def test_strip_and_words(self):
        blob = TextBlob('Beautiful is better! ')
        assert_equal(blob.strip().words, WordList(['Beautiful', 'is', 'better'
                     ]))

    def test_index(self):
        blob = TextBlob(self.text)
        assert_equal(blob.index('Namespaces'), self.text.index('Namespaces'))

    def test_sentences_after_concatenation(self):
        blob1 = TextBlob('Beautiful is better than ugly. ')
        blob2 = TextBlob('Explicit is better than implicit.')

        concatenated = blob1 + blob2
        assert_equal(len(concatenated.sentences), 2)

    def test_sentiment(self):
        positive = \
            TextBlob('This is the best, most amazing text-processing library ever!'
                     )
        assert_true(positive.sentiment[0] > 0.0)
        negative = TextBlob("bad bad bitches that's my muthufuckin problem.")
        assert_true(negative.sentiment[0] < 0.0)
        zen = TextBlob(self.text)
        assert_equal(round(zen.sentiment[0], 2), 0.20)
        assert_equal(round(zen.sentiment[1], 2), 0.58)

    def test_bad_init(self):
        assert_raises(TypeError, TextBlob.__init__, ['bad'])

    def test_in(self):
        blob = TextBlob('Beautiful is better than ugly. ')
        assert_true('better' in blob)
        assert_true('fugly' not in blob)

    def test_json(self):
        blob = TextBlob('Beautiful is better than ugly. ')
        blob_dict = json.loads(blob.json)[0]
        assert_equal(blob_dict['stripped'], 'beautiful is better than ugly')
        assert_equal(blob_dict['noun_phrases'], blob.sentences[0].noun_phrases)
        assert_equal(blob_dict['start_index'], blob.sentences[0].start)
        assert_equal(blob_dict['end_index'], blob.sentences[0].end)
        assert_almost_equal(blob_dict['sentiment'][0],
                            blob.sentences[0].sentiment[0], places=4)


def is_blob(obj):
    return isinstance(obj, TextBlob)


if __name__ == '__main__':
    main()
