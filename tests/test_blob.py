"""
Tests for the text processor.
"""

import json
from datetime import datetime
from unittest import TestCase

import nltk
import pytest

import textblob as tb
import textblob.wordnet as wn
from textblob.classifiers import NaiveBayesClassifier
from textblob.np_extractors import ConllExtractor, FastNPExtractor
from textblob.parsers import PatternParser
from textblob.sentiments import NaiveBayesAnalyzer, PatternAnalyzer
from textblob.taggers import NLTKTagger, PatternTagger
from textblob.tokenizers import SentenceTokenizer, WordTokenizer

Synset = nltk.corpus.reader.Synset

train = [
    ("I love this sandwich.", "pos"),
    ("This is an amazing place!", "pos"),
    ("What a truly amazing dinner.", "pos"),
    ("I feel very good about these beers.", "pos"),
    ("This is my best work.", "pos"),
    ("What an awesome view", "pos"),
    ("I do not like this restaurant", "neg"),
    ("I am tired of this stuff.", "neg"),
    ("I can't deal with this", "neg"),
    ("He is my sworn enemy!", "neg"),
    ("My boss is horrible.", "neg"),
]

test = [
    ("The beer was good.", "pos"),
    ("I do not enjoy my job", "neg"),
    ("I ain't feeling dandy today.", "neg"),
    ("I feel amazing!", "pos"),
    ("Gary is a friend of mine.", "pos"),
    ("I can't believe I'm doing this.", "neg"),
]

classifier = NaiveBayesClassifier(train)


class WordListTest(TestCase):
    def setUp(self):
        self.words = "Beautiful is better than ugly".split()
        self.mixed = ["dog", "dogs", "blob", "Blobs", "text"]

    def test_len(self):
        wl = tb.WordList(["Beautiful", "is", "better"])
        assert len(wl) == 3

    def test_slicing(self):
        wl = tb.WordList(self.words)
        first = wl[0]
        assert isinstance(first, tb.Word)
        assert first == "Beautiful"

        dogs = wl[0:2]
        assert isinstance(dogs, tb.WordList)
        assert dogs == tb.WordList(["Beautiful", "is"])

    def test_repr(self):
        wl = tb.WordList(["Beautiful", "is", "better"])
        assert repr(wl) == "WordList(['Beautiful', 'is', 'better'])"

    def test_slice_repr(self):
        wl = tb.WordList(["Beautiful", "is", "better"])
        assert repr(wl[:2]) == "WordList(['Beautiful', 'is'])"

    def test_str(self):
        wl = tb.WordList(self.words)
        assert str(wl) == str(self.words)

    def test_singularize(self):
        wl = tb.WordList(["dogs", "cats", "buffaloes", "men", "mice", "offspring"])
        assert wl.singularize() == tb.WordList(
            ["dog", "cat", "buffalo", "man", "mouse", "offspring"]
        )

    def test_pluralize(self):
        wl = tb.WordList(["dog", "cat", "buffalo", "antelope"])
        assert wl.pluralize() == tb.WordList(["dogs", "cats", "buffaloes", "antelope"])

    @pytest.mark.slow
    def test_lemmatize(self):
        wl = tb.WordList(["cat", "dogs", "oxen"])
        assert wl.lemmatize() == tb.WordList(["cat", "dog", "ox"])

    def test_stem(self):  # only PorterStemmer tested
        wl = tb.WordList(["cat", "dogs", "oxen"])
        assert wl.stem() == tb.WordList(["cat", "dog", "oxen"])

    def test_upper(self):
        wl = tb.WordList(self.words)
        assert wl.upper() == tb.WordList([w.upper() for w in self.words])

    def test_lower(self):
        wl = tb.WordList(["Zen", "oF", "PYTHON"])
        assert wl.lower() == tb.WordList(["zen", "of", "python"])

    def test_count(self):
        wl = tb.WordList(["monty", "python", "Python", "Monty"])
        assert wl.count("monty") == 2
        assert wl.count("monty", case_sensitive=True) == 1
        assert wl.count("mon") == 0

    def test_convert_to_list(self):
        wl = tb.WordList(self.words)
        assert list(wl) == self.words

    def test_append(self):
        wl = tb.WordList(["dog"])
        wl.append("cat")
        assert isinstance(wl[1], tb.Word)
        wl.append(("a", "tuple"))
        assert isinstance(wl[2], tuple)

    def test_extend(self):
        wl = tb.WordList(["cats", "dogs"])
        wl.extend(["buffalo", 4])
        assert isinstance(wl[2], tb.Word)
        assert isinstance(wl[3], int)

    def test_pop(self):
        wl = tb.WordList(["cats", "dogs"])
        assert wl.pop() == tb.Word("dogs")
        with pytest.raises(IndexError):
            wl[1]
        assert wl.pop() == tb.Word("cats")
        assert len(wl) == 0
        with pytest.raises(IndexError):
            wl.pop()

    def test_setitem(self):
        wl = tb.WordList(["I", "love", "JavaScript"])
        wl[2] = tb.Word("Python")
        assert wl[2] == tb.Word("Python")

    def test_reverse(self):
        wl = tb.WordList(["head", "shoulders", "knees", "toes"])
        wl.reverse()
        assert list(wl) == ["toes", "knees", "shoulders", "head"]


class SentenceTest(TestCase):
    def setUp(self):
        self.raw_sentence = "Any place with frites and Belgian beer has my vote."
        self.sentence = tb.Sentence(self.raw_sentence)

    def test_repr(self):
        assert repr(self.sentence) == f'Sentence("{self.raw_sentence}")'

    def test_stripped_sentence(self):
        assert (
            self.sentence.stripped
            == "any place with frites and belgian beer has my vote"
        )

    def test_len(self):
        assert len(self.sentence) == len(self.raw_sentence)

    @pytest.mark.slow
    def test_dict(self):
        sentence_dict = self.sentence.dict
        assert sentence_dict == {
            "raw": self.raw_sentence,
            "start_index": 0,
            "polarity": 0.0,
            "subjectivity": 0.0,
            "end_index": len(self.raw_sentence) - 1,
            "stripped": "any place with frites and belgian beer has my vote",
            "noun_phrases": self.sentence.noun_phrases,
        }

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
        assert t2 < t1
        assert tagged == [
            ("Any", "DT"),
            ("place", "NN"),
            ("with", "IN"),
            ("frites", "NNS"),
            ("and", "CC"),
            ("Belgian", "JJ"),
            ("beer", "NN"),
            ("has", "VBZ"),
            ("my", "PRP$"),
            ("vote", "NN"),
        ]

    @pytest.mark.slow
    def test_noun_phrases(self):
        nps = self.sentence.noun_phrases
        assert nps == ["belgian beer"]

    def test_words_are_word_objects(self):
        words = self.sentence.words
        assert isinstance(words[0], tb.Word)
        assert words[1].pluralize() == "places"

    def test_string_equality(self):
        assert self.sentence == "Any place with frites and Belgian beer has my vote."

    def test_correct(self):
        blob = tb.Sentence("I havv bad speling.")
        assert isinstance(blob.correct(), tb.Sentence)
        assert blob.correct() == tb.Sentence("I have bad spelling.")
        blob = tb.Sentence("I havv \ngood speling.")
        assert isinstance(blob.correct(), tb.Sentence)
        assert blob.correct() == tb.Sentence("I have \ngood spelling.")


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
        self.blob = tb.TextBlob(self.text)

        self.np_test_text = """
Python is a widely used general-purpose, high-level programming language.
Its design philosophy emphasizes code readability, and its syntax allows
programmers to express concepts in fewer
lines of code than would be possible in languages such as C.
The language provides constructs intended to enable clear programs on both a small and large scale.
Python supports multiple programming paradigms, including object-oriented,
imperative and functional programming or procedural styles.
It features a dynamic type system and automatic memory management and
has a large and comprehensive standard library. Like other dynamic languages, Python is often used as a scripting language,
but is also used in a wide range of non-scripting contexts.
Using third-party tools, Python code can be packaged into standalone executable
programs. Python interpreters are available for many operating systems. CPython, the reference implementation of Python, is free and open source software and h
as a community-based development model, as do nearly all of its alternative implementations. CPython
is managed by the non-profit Python Software Foundation."""  # noqa: E501
        self.np_test_blob = tb.TextBlob(self.np_test_text)

        self.short = "Beautiful is better than ugly. "
        self.short_blob = tb.TextBlob(self.short)

    def test_init(self):
        blob = tb.TextBlob("Wow I love this place. It really rocks my socks!")
        assert len(blob.sentences) == 2
        assert blob.sentences[1].stripped == "it really rocks my socks"
        assert blob.string == blob.raw

        # Must initialize with a string
        with pytest.raises(TypeError):
            tb.TextBlob(["invalid"])

    def test_string_equality(self):
        blob = tb.TextBlob("Textblobs should be equal to strings.")
        assert blob == "Textblobs should be equal to strings."

    def test_string_comparison(self):
        blob = tb.TextBlob("apple")
        assert blob < "banana"
        assert blob > "aardvark"

    def test_hash(self):
        blob = tb.TextBlob("apple")
        assert hash(blob) == hash("apple")
        assert hash(blob) != hash("banana")

    def test_stripped(self):
        blob = tb.TextBlob("Um... well this ain't right.!..")
        assert blob.stripped == "um well this aint right"

    def test_ngrams(self):
        blob = tb.TextBlob("I am eating a pizza.")
        three_grams = blob.ngrams()
        assert three_grams == [
            tb.WordList(("I", "am", "eating")),
            tb.WordList(("am", "eating", "a")),
            tb.WordList(("eating", "a", "pizza")),
        ]
        four_grams = blob.ngrams(n=4)
        assert four_grams == [
            tb.WordList(("I", "am", "eating", "a")),
            tb.WordList(("am", "eating", "a", "pizza")),
        ]

    def test_clean_html(self):
        html = (
            "<b>Python</b> is a widely used "
            '<a href="/wiki/General-purpose_programming_language" '
            'title="General-purpose programming language">general-purpose</a>, '
            '<a href="/wiki/High-level_programming_language" '
            'title="High-level programming language">'
            "high-level programming language</a>."
        )
        with pytest.raises(NotImplementedError):
            tb.TextBlob(html, clean_html=True)

    def test_sentences(self):
        blob = self.blob
        assert len(blob.sentences) == 19
        assert isinstance(blob.sentences[0], tb.Sentence)

    def test_senences_with_space_before_punctuation(self):
        text = "Uh oh. This sentence might cause some problems. : Now we're ok."
        b = tb.TextBlob(text)
        assert len(b.sentences) == 3

    def test_sentiment_of_foreign_text(self):
        blob = tb.TextBlob(
            "Nous avons cherch\xe9 un motel dans la r\xe9gion de "
            "Madison, mais les motels ne sont pas nombreux et nous avons "
            "finalement choisi un Motel 6, attir\xe9s par le bas "
            "prix de la chambre."
        )
        assert isinstance(blob.sentiment[0], float)

    def test_iter(self):
        for i, letter in enumerate(self.short_blob):
            assert letter == self.short[i]

    def test_raw_sentences(self):
        blob = tb.TextBlob(self.text)
        assert len(blob.raw_sentences) == 19
        assert blob.raw_sentences[0] == "Beautiful is better than ugly."

    def test_blob_with_no_sentences(self):
        text = "this isn't really a sentence it's just a long string of words"
        blob = tb.TextBlob(text)
        # the blob just has one sentence
        assert len(blob.sentences) == 1
        # the start index is 0, the end index is len(text) - 1
        assert blob.sentences[0].start_index == 0
        assert blob.sentences[0].end_index == len(text)

    def test_len(self):
        blob = tb.TextBlob("lorem ipsum")
        assert len(blob) == len("lorem ipsum")

    def test_repr(self):
        blob1 = tb.TextBlob("lorem ipsum")
        assert repr(blob1) == 'TextBlob("{}")'.format("lorem ipsum")

    def test_cmp(self):
        blob1 = tb.TextBlob("lorem ipsum")
        blob2 = tb.TextBlob("lorem ipsum")
        blob3 = tb.TextBlob("dolor sit amet")

        assert blob1 == blob2  # test ==
        assert blob1 > blob3  # test >
        assert blob1 >= blob3  # test >=
        assert blob3 < blob2  # test <
        assert blob3 <= blob2  # test <=

    def test_invalid_comparison(self):
        blob = tb.TextBlob("one")
        # invalid comparison raises Error
        with pytest.raises(TypeError):
            blob < 2  # noqa: B015

    def test_words(self):
        blob = tb.TextBlob(
            "Beautiful is better than ugly. " "Explicit is better than implicit."
        )
        assert isinstance(blob.words, tb.WordList)
        assert blob.words == tb.WordList(
            [
                "Beautiful",
                "is",
                "better",
                "than",
                "ugly",
                "Explicit",
                "is",
                "better",
                "than",
                "implicit",
            ]
        )
        short = tb.TextBlob("Just a bundle of words")
        assert short.words == tb.WordList(["Just", "a", "bundle", "of", "words"])

    def test_words_includes_apostrophes_in_contractions(self):
        blob = tb.TextBlob("Let's test this.")
        assert blob.words == tb.WordList(["Let", "'s", "test", "this"])
        blob2 = tb.TextBlob("I can't believe it's not butter.")
        assert blob2.words == tb.WordList(
            ["I", "ca", "n't", "believe", "it", "'s", "not", "butter"]
        )

    def test_pos_tags(self):
        blob = tb.TextBlob(
            "Simple is better than complex. " "Complex is better than complicated."
        )
        assert blob.pos_tags == [
            ("Simple", "NN"),
            ("is", "VBZ"),
            ("better", "JJR"),
            ("than", "IN"),
            ("complex", "JJ"),
            ("Complex", "NNP"),
            ("is", "VBZ"),
            ("better", "JJR"),
            ("than", "IN"),
            ("complicated", "VBN"),
        ]

    def test_tags(self):
        assert self.blob.tags == self.blob.pos_tags

    def test_tagging_nonascii(self):
        b = tb.TextBlob(
            "Learn how to make the five classic French mother sauces: "
            "Béchamel, Tomato Sauce, Espagnole, Velouté and Hollandaise."
        )
        tags = b.tags
        assert isinstance(tags[0][0], str)

    def test_pos_tags_includes_one_letter_articles(self):
        blob = tb.TextBlob("This is a sentence.")
        assert blob.pos_tags[2][0] == "a"

    @pytest.mark.slow
    def test_np_extractor_defaults_to_fast_tagger(self):
        text = "Python is a high-level scripting language."
        blob1 = tb.TextBlob(text)
        assert isinstance(blob1.np_extractor, FastNPExtractor)

    def test_np_extractor_is_shared_among_instances(self):
        blob1 = tb.TextBlob("This is one sentence")
        blob2 = tb.TextBlob("This is another sentence")
        assert blob1.np_extractor is blob2.np_extractor

    @pytest.mark.slow
    def test_can_use_different_np_extractors(self):
        e = ConllExtractor()
        text = "Python is a high-level scripting language."
        blob = tb.TextBlob(text)
        blob.np_extractor = e
        assert isinstance(blob.np_extractor, ConllExtractor)

    def test_can_use_different_sentanalyzer(self):
        blob = tb.TextBlob("I love this car", analyzer=NaiveBayesAnalyzer())
        assert isinstance(blob.analyzer, NaiveBayesAnalyzer)

    @pytest.mark.slow
    def test_discrete_sentiment(self):
        blob = tb.TextBlob("I feel great today.", analyzer=NaiveBayesAnalyzer())
        assert blob.sentiment[0] == "pos"

    def test_can_get_subjectivity_and_polarity_with_different_analyzer(self):
        blob = tb.TextBlob("I love this car.", analyzer=NaiveBayesAnalyzer())
        pattern = PatternAnalyzer()
        assert blob.polarity == pattern.analyze(str(blob))[0]
        assert blob.subjectivity == pattern.analyze(str(blob))[1]

    def test_pos_tagger_defaults_to_pattern(self):
        blob = tb.TextBlob("some text")
        assert isinstance(blob.pos_tagger, NLTKTagger)

    def test_pos_tagger_is_shared_among_instances(self):
        blob1 = tb.TextBlob("This is one sentence")
        blob2 = tb.TextBlob("This is another sentence.")
        assert blob1.pos_tagger is blob2.pos_tagger

    def test_can_use_different_pos_tagger(self):
        tagger = NLTKTagger()
        blob = tb.TextBlob("this is some text", pos_tagger=tagger)
        assert isinstance(blob.pos_tagger, NLTKTagger)

    @pytest.mark.slow
    def test_can_pass_np_extractor_to_constructor(self):
        e = ConllExtractor()
        blob = tb.TextBlob("Hello world!", np_extractor=e)
        assert isinstance(blob.np_extractor, ConllExtractor)

    def test_getitem(self):
        blob = tb.TextBlob("lorem ipsum")
        assert blob[0] == "l"
        assert blob[0:5] == tb.TextBlob("lorem")

    def test_upper(self):
        blob = tb.TextBlob("lorem ipsum")
        assert is_blob(blob.upper())
        assert blob.upper() == tb.TextBlob("LOREM IPSUM")

    def test_upper_and_words(self):
        blob = tb.TextBlob("beautiful is better")
        assert blob.upper().words == tb.WordList(["BEAUTIFUL", "IS", "BETTER"])

    def test_lower(self):
        blob = tb.TextBlob("Lorem Ipsum")
        assert is_blob(blob.lower())
        assert blob.lower() == tb.TextBlob("lorem ipsum")

    def test_find(self):
        text = "Beautiful is better than ugly."
        blob = tb.TextBlob(text)
        assert blob.find("better", 5, len(blob)) == text.find("better", 5, len(text))

    def test_rfind(self):
        text = "Beautiful is better than ugly. "
        blob = tb.TextBlob(text)
        assert blob.rfind("better") == text.rfind("better")

    def test_startswith(self):
        blob = tb.TextBlob(self.text)
        assert blob.startswith("Beautiful")
        assert blob.starts_with("Beautiful")

    def test_endswith(self):
        blob = tb.TextBlob(self.text)
        assert blob.endswith("of those!")
        assert blob.ends_with("of those!")

    def test_split(self):
        blob = tb.TextBlob("Beautiful is better")
        assert blob.split() == tb.WordList(["Beautiful", "is", "better"])

    def test_title(self):
        blob = tb.TextBlob("Beautiful is better")
        assert blob.title() == tb.TextBlob("Beautiful Is Better")

    def test_format(self):
        blob = tb.TextBlob("1 + 1 = {0}")
        assert blob.format(1 + 1) == tb.TextBlob("1 + 1 = 2")
        assert "1 + 1 = {}".format(tb.TextBlob("2")) == "1 + 1 = 2"

    def test_using_indices_for_slicing(self):
        blob = tb.TextBlob("Hello world. How do you do?")
        sent1, sent2 = blob.sentences
        assert blob[sent1.start : sent1.end] == tb.TextBlob(str(sent1))
        assert blob[sent2.start : sent2.end] == tb.TextBlob(str(sent2))

    def test_indices_with_only_one_sentences(self):
        blob = tb.TextBlob("Hello world.")
        sent1 = blob.sentences[0]
        assert blob[sent1.start : sent1.end] == tb.TextBlob(str(sent1))

    def test_indices_with_multiple_puncutations(self):
        blob = tb.TextBlob("Hello world. How do you do?! This has an ellipses...")
        sent1, sent2, sent3 = blob.sentences
        assert blob[sent2.start : sent2.end] == tb.TextBlob("How do you do?!")
        assert blob[sent3.start : sent3.end] == tb.TextBlob("This has an ellipses...")

    def test_indices_short_names(self):
        blob = tb.TextBlob(self.text)
        last_sentence = blob.sentences[len(blob.sentences) - 1]
        assert last_sentence.start == last_sentence.start_index
        assert last_sentence.end == last_sentence.end_index

    def test_replace(self):
        blob = tb.TextBlob("textblob is a blobby blob")
        assert blob.replace("blob", "bro") == tb.TextBlob("textbro is a broby bro")
        assert blob.replace("blob", "bro", 1) == tb.TextBlob("textbro is a blobby blob")

    def test_join(self):
        lst = ["explicit", "is", "better"]
        wl = tb.WordList(lst)
        assert tb.TextBlob(" ").join(lst) == tb.TextBlob("explicit is better")
        assert tb.TextBlob(" ").join(wl) == tb.TextBlob("explicit is better")

    @pytest.mark.slow
    def test_blob_noun_phrases(self):
        noun_phrases = self.np_test_blob.noun_phrases
        assert "python" in noun_phrases
        assert "design philosophy" in noun_phrases

    def test_word_counts(self):
        blob = tb.TextBlob("Buffalo buffalo ate my blue buffalo.")
        assert dict(blob.word_counts) == {"buffalo": 3, "ate": 1, "my": 1, "blue": 1}
        assert blob.word_counts["buffalo"] == 3
        assert blob.words.count("buffalo") == 3
        assert blob.words.count("buffalo", case_sensitive=True) == 2
        assert blob.word_counts["blue"] == 1
        assert blob.words.count("blue") == 1
        assert blob.word_counts["ate"] == 1
        assert blob.words.count("ate") == 1
        assert blob.word_counts["buff"] == 0
        assert blob.words.count("buff") == 0

        blob2 = tb.TextBlob(self.text)
        assert blob2.words.count("special") == 2
        assert blob2.words.count("special", case_sensitive=True) == 1

    @pytest.mark.slow
    def test_np_counts(self):
        # Add some text so that we have a noun phrase that
        # has a frequency greater than 1
        noun_phrases = self.np_test_blob.noun_phrases
        assert noun_phrases.count("python") == 6
        assert self.np_test_blob.np_counts["python"] == noun_phrases.count("python")
        assert noun_phrases.count("cpython") == 2
        assert noun_phrases.count("not found") == 0

    def test_add(self):
        blob1 = tb.TextBlob("Hello, world! ")
        blob2 = tb.TextBlob("Hola mundo!")
        # Can add two text blobs
        assert blob1 + blob2 == tb.TextBlob("Hello, world! Hola mundo!")
        # Can also add a string to a tb.TextBlob
        assert blob1 + "Hola mundo!" == tb.TextBlob("Hello, world! Hola mundo!")
        # Or both
        assert blob1 + blob2 + " Goodbye!" == tb.TextBlob(
            "Hello, world! Hola mundo! Goodbye!"
        )

        # operands must be strings
        with pytest.raises(TypeError):
            blob1 + ["hello"]

    def test_unicode(self):
        blob = tb.TextBlob(self.text)
        assert str(blob) == str(self.text)

    def test_strip(self):
        text = "Beautiful is better than ugly. "
        blob = tb.TextBlob(text)
        assert is_blob(blob)
        assert blob.strip() == tb.TextBlob(text.strip())

    def test_strip_and_words(self):
        blob = tb.TextBlob("Beautiful is better! ")
        assert blob.strip().words == tb.WordList(["Beautiful", "is", "better"])

    def test_index(self):
        blob = tb.TextBlob(self.text)
        assert blob.index("Namespaces") == self.text.index("Namespaces")

    def test_sentences_after_concatenation(self):
        blob1 = tb.TextBlob("Beautiful is better than ugly. ")
        blob2 = tb.TextBlob("Explicit is better than implicit.")

        concatenated = blob1 + blob2
        assert len(concatenated.sentences) == 2

    def test_sentiment(self):
        positive = tb.TextBlob(
            "This is the best, most amazing " "text-processing library ever!"
        )
        assert positive.sentiment[0] > 0.0
        negative = tb.TextBlob("bad bad bitches that's my muthufuckin problem.")
        assert negative.sentiment[0] < 0.0
        zen = tb.TextBlob(self.text)
        assert round(zen.sentiment[0], 1) == 0.2

    def test_subjectivity(self):
        positive = tb.TextBlob("Oh my god this is so amazing! I'm so happy!")
        assert isinstance(positive.subjectivity, float)
        assert positive.subjectivity > 0

    def test_polarity(self):
        positive = tb.TextBlob("Oh my god this is so amazing! I'm so happy!")
        assert isinstance(positive.polarity, float)
        assert positive.polarity > 0

    def test_sentiment_of_emoticons(self):
        b1 = tb.TextBlob("Faces have values =)")
        b2 = tb.TextBlob("Faces have values")
        assert b1.sentiment[0] > b2.sentiment[0]

    def test_bad_init(self):
        with pytest.raises(TypeError):
            tb.TextBlob(["bad"])
        with pytest.raises(ValueError):
            tb.TextBlob("this is fine", np_extractor="this is not fine")
        with pytest.raises(ValueError):
            tb.TextBlob("this is fine", pos_tagger="this is not fine")

    def test_in(self):
        blob = tb.TextBlob("Beautiful is better than ugly. ")
        assert "better" in blob
        assert "fugly" not in blob

    @pytest.mark.slow
    def test_json(self):
        blob = tb.TextBlob("Beautiful is better than ugly. ")
        assert blob.json == blob.to_json()
        blob_dict = json.loads(blob.json)[0]
        assert blob_dict["stripped"] == "beautiful is better than ugly"
        assert blob_dict["noun_phrases"] == blob.sentences[0].noun_phrases
        assert blob_dict["start_index"] == blob.sentences[0].start
        assert blob_dict["end_index"] == blob.sentences[0].end
        assert blob_dict["polarity"] == pytest.approx(
            blob.sentences[0].polarity, abs=1e-4
        )
        assert blob_dict["subjectivity"] == pytest.approx(
            blob.sentences[0].subjectivity, abs=1e-4
        )

    def test_words_are_word_objects(self):
        words = self.blob.words
        assert isinstance(words[0], tb.Word)

    def test_words_have_pos_tags(self):
        blob = tb.TextBlob(
            "Simple is better than complex. " "Complex is better than complicated."
        )
        first_word, first_tag = blob.pos_tags[0]
        assert isinstance(first_word, tb.Word)
        assert first_word.pos_tag == first_tag

    def test_tokenizer_defaults_to_word_tokenizer(self):
        assert isinstance(self.blob.tokenizer, WordTokenizer)

    def test_tokens_property(self):
        assert self.blob.tokens, tb.WordList(WordTokenizer().tokenize(self.text))

    def test_can_use_an_different_tokenizer(self):
        tokenizer = nltk.tokenize.TabTokenizer()
        blob = tb.TextBlob("This is\ttext.", tokenizer=tokenizer)
        assert blob.tokens == tb.WordList(["This is", "text."])

    def test_tokenize_method(self):
        tokenizer = nltk.tokenize.TabTokenizer()
        blob = tb.TextBlob("This is\ttext.")
        # If called without arguments, should default to WordTokenizer
        assert blob.tokenize() == tb.WordList(["This", "is", "text", "."])
        # Pass in the TabTokenizer
        assert blob.tokenize(tokenizer) == tb.WordList(["This is", "text."])

    def test_tags_uses_custom_tokenizer(self):
        tokenizer = nltk.tokenize.regexp.WordPunctTokenizer()
        blob = tb.TextBlob("Good muffins cost $3.88\nin New York.", tokenizer=tokenizer)
        assert blob.tags == [
            ("Good", "JJ"),
            ("muffins", "NNS"),
            ("cost", "VBP"),
            ("3", "CD"),
            ("88", "CD"),
            ("in", "IN"),
            ("New", "NNP"),
            ("York", "NNP"),
        ]

    def test_tags_with_custom_tokenizer_and_tagger(self):
        tokenizer = nltk.tokenize.regexp.WordPunctTokenizer()
        tagger = tb.taggers.PatternTagger()
        blob = tb.TextBlob(
            "Good muffins cost $3.88\nin New York.",
            tokenizer=tokenizer,
            pos_tagger=tagger,
        )
        # PatterTagger takes raw text (not tokens), and handles tokenization itself.
        assert blob.tags == [
            ("Good", "JJ"),
            ("muffins", "NNS"),
            ("cost", "NN"),
            ("3.88", "CD"),
            ("in", "IN"),
            ("New", "NNP"),
            ("York", "NNP"),
        ]

    def test_correct(self):
        blob = tb.TextBlob("I havv bad speling.")
        assert isinstance(blob.correct(), tb.TextBlob)
        assert blob.correct() == tb.TextBlob("I have bad spelling.")
        blob2 = tb.TextBlob("I am so exciited!!!")
        assert blob2.correct() == "I am so excited!!!"
        blob3 = tb.TextBlob("The meaning of life is 42.0.")
        assert blob3.correct() == "The meaning of life is 42.0."
        blob4 = tb.TextBlob("?")
        assert blob4.correct() == "?"

        blob5 = tb.TextBlob("I can't spel")
        assert blob5.correct() == "I can't spell"

        blob6 = tb.TextBlob("I cann't \nspel")
        assert blob6.correct() == "I can't \nspell"

        # From a user-submitted bug
        text = (
            "Before you embark on any of this journey, write a quick "
            + "high-level test that demonstrates the slowness. "
            + "You may need to introduce some minimum set of data to "
            + "reproduce a significant enough slowness."
        )
        blob5 = tb.TextBlob(text)
        assert blob5.correct() == text
        text = "Word list!  :\n" + "\t* spelling\n" + "\t* well"
        blob6 = tb.TextBlob(text)
        assert blob6.correct() == text

    def test_parse(self):
        blob = tb.TextBlob("And now for something completely different.")
        assert blob.parse() == PatternParser().parse(blob.string)

    def test_passing_bad_init_params(self):
        tagger = PatternTagger()
        with pytest.raises(ValueError):
            tb.TextBlob("blah", parser=tagger)
        with pytest.raises(ValueError):
            tb.TextBlob("blah", np_extractor=tagger)
        with pytest.raises(ValueError):
            tb.TextBlob("blah", tokenizer=tagger)
        with pytest.raises(ValueError):
            tb.TextBlob("blah", analyzer=tagger)
        with pytest.raises(ValueError):
            tb.TextBlob("blah", pos_tagger=PatternAnalyzer)

    def test_classify(self):
        blob = tb.TextBlob(
            "This is an amazing library. What an awesome classifier!",
            classifier=classifier,
        )
        assert blob.classify() == "pos"
        for s in blob.sentences:
            assert s.classify() == "pos"

    def test_classify_without_classifier(self):
        blob = tb.TextBlob("This isn't gonna be good")
        with pytest.raises(NameError):
            blob.classify()

    def test_word_string_type_after_pos_tags_is_str(self):
        text = "John is a cat"
        blob = tb.TextBlob(text)
        for word, _ in blob.pos_tags:
            assert type(word.string) is str


class WordTest(TestCase):
    def setUp(self):
        self.cat = tb.Word("cat")
        self.cats = tb.Word("cats")

    def test_init(self):
        tb.Word("cat")
        assert isinstance(self.cat, tb.Word)
        word = tb.Word("cat", "NN")
        assert word.pos_tag == "NN"

    def test_singularize(self):
        singular = self.cats.singularize()
        assert singular == "cat"
        assert self.cat.singularize() == "cat"
        assert isinstance(self.cat.singularize(), tb.Word)

    def test_pluralize(self):
        plural = self.cat.pluralize()
        assert self.cat.pluralize() == "cats"
        assert isinstance(plural, tb.Word)

    def test_repr(self):
        assert repr(self.cat) == repr("cat")

    def test_str(self):
        assert str(self.cat) == "cat"

    def test_has_str_methods(self):
        assert self.cat.upper() == "CAT"
        assert self.cat.lower() == "cat"
        assert self.cat[0:2] == "ca"

    def test_spellcheck(self):
        blob = tb.Word("speling")
        suggestions = blob.spellcheck()
        assert suggestions[0][0] == "spelling"

    def test_spellcheck_special_cases(self):
        # Punctuation
        assert tb.Word("!").spellcheck() == [("!", 1.0)]
        # Numbers
        assert tb.Word("42").spellcheck() == [("42", 1.0)]
        assert tb.Word("12.34").spellcheck() == [("12.34", 1.0)]
        # One-letter words
        assert tb.Word("I").spellcheck() == [("I", 1.0)]
        assert tb.Word("A").spellcheck() == [("A", 1.0)]
        assert tb.Word("a").spellcheck() == [("a", 1.0)]

    def test_correct(self):
        w = tb.Word("speling")
        correct = w.correct()
        assert correct == tb.Word("spelling")
        assert isinstance(correct, tb.Word)

    @pytest.mark.slow
    def test_lemmatize(self):
        w = tb.Word("cars")
        assert w.lemmatize() == "car"
        w = tb.Word("wolves")
        assert w.lemmatize() == "wolf"
        w = tb.Word("went")
        assert w.lemmatize("v") == "go"  # wordnet tagset
        assert w.lemmatize("VBD") == "go"  # penn treebank tagset

    def test_lemma(self):
        w = tb.Word("wolves")
        assert w.lemma == "wolf"
        w = tb.Word("went", "VBD")
        assert w.lemma == "go"

    def test_stem(self):  # only PorterStemmer tested
        w = tb.Word("cars")
        assert w.stem() == "car"
        w = tb.Word("wolves")
        assert w.stem() == "wolv"
        w = tb.Word("went")
        assert w.stem() == "went"

    def test_synsets(self):
        w = tb.Word("car")
        assert isinstance(w.synsets, (list, tuple))
        assert isinstance(w.synsets[0], Synset)

    def test_synsets_with_pos_argument(self):
        w = tb.Word("work")
        noun_syns = w.get_synsets(pos=wn.NOUN)
        for synset in noun_syns:
            assert synset.pos() == wn.NOUN

    def test_definitions(self):
        w = tb.Word("octopus")
        for definition in w.definitions:
            assert isinstance(definition, str)

    def test_define(self):
        w = tb.Word("hack")
        synsets = w.get_synsets(wn.NOUN)
        definitions = w.define(wn.NOUN)
        assert len(synsets) == len(definitions)


class TestWordnetInterface(TestCase):
    def setUp(self):
        pass

    def test_synset(self):
        syn = wn.Synset("dog.n.01")
        word = tb.Word("dog")
        assert word.synsets[0] == syn

    def test_lemma(self):
        lemma = wn.Lemma("eat.v.01.eat")
        word = tb.Word("eat")
        assert word.synsets[0].lemmas()[0] == lemma


class BlobberTest(TestCase):
    def setUp(self):
        self.blobber = tb.Blobber()  # The default blobber

    def test_creates_blobs(self):
        blob1 = self.blobber("this is one blob")
        assert isinstance(blob1, tb.TextBlob)
        blob2 = self.blobber("another blob")
        assert blob1.pos_tagger == blob2.pos_tagger

    def test_default_tagger(self):
        blob = self.blobber("Some text")
        assert isinstance(blob.pos_tagger, NLTKTagger)

    def test_default_np_extractor(self):
        blob = self.blobber("Some text")
        assert isinstance(blob.np_extractor, FastNPExtractor)

    def test_default_tokenizer(self):
        blob = self.blobber("Some text")
        assert isinstance(blob.tokenizer, WordTokenizer)

    def test_str_and_repr(self):
        expected = "Blobber(tokenizer=WordTokenizer(), pos_tagger=NLTKTagger(), np_extractor=FastNPExtractor(), analyzer=PatternAnalyzer(), parser=PatternParser(), classifier=None)"  # noqa: E501
        assert repr(self.blobber) == expected
        assert str(self.blobber) == repr(self.blobber)

    def test_overrides(self):
        b = tb.Blobber(tokenizer=SentenceTokenizer(), np_extractor=ConllExtractor())
        blob = b("How now? Brown cow?")
        assert isinstance(blob.tokenizer, SentenceTokenizer)
        assert blob.tokens == tb.WordList(["How now?", "Brown cow?"])
        blob2 = b("Another blob")
        # blobs have the same tokenizer
        assert blob.tokenizer is blob2.tokenizer
        # but aren't the same object
        assert blob != blob2

    def test_override_analyzer(self):
        b = tb.Blobber(analyzer=NaiveBayesAnalyzer())
        blob = b("How now?")
        blob2 = b("Brown cow")
        assert isinstance(blob.analyzer, NaiveBayesAnalyzer)
        assert blob.analyzer is blob2.analyzer

    def test_overrider_classifier(self):
        b = tb.Blobber(classifier=classifier)
        blob = b("I am so amazing")
        assert blob.classify() == "pos"


def is_blob(obj):
    return isinstance(obj, tb.TextBlob)
