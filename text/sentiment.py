# -*- coding: utf-8 -*-
import types
import os
import re
from xml.etree import cElementTree

try:
    MODULE = os.path.dirname(os.path.abspath(__file__))
except:
    MODULE = ""

#--- LAZY DICTIONARY -------------------------------------------------------------------------------
# A lazy dictionary is empty until one of its methods is called.
# This way many instances (e.g., lexicons) can be created without using memory until used.

class lazydict(dict):

    def load(self):
        # Must be overridden in a subclass.
        # Must load data with dict.__setitem__(self, k, v) instead of lazydict[k] = v.
        pass

    def _lazy(self, method, *args):
        """ If the dictionary is empty, calls lazydict.load().
            Replaces lazydict.method() with dict.method() and calls it.
        """
        if dict.__len__(self) == 0:
            self.load()
            setattr(self, method, types.MethodType(getattr(dict, method), self))
        return getattr(dict, method)(self, *args)

    def __repr__(self):
        return self._lazy("__repr__")
    def __len__(self):
        return self._lazy("__len__")
    def __iter__(self):
        return self._lazy("__iter__")
    def __contains__(self, *args):
        return self._lazy("__contains__", *args)
    def __getitem__(self, *args):
        return self._lazy("__getitem__", *args)
    def __setitem__(self, *args):
        return self._lazy("__setitem__", *args)
    def setdefault(self, *args):
        return self._lazy("setdefault", *args)
    def get(self, *args, **kwargs):
        return self._lazy("get", *args)
    def items(self):
        return self._lazy("items")
    def keys(self):
        return self._lazy("keys")
    def values(self):
        return self._lazy("values")
    def update(self, *args):
        return self._lazy("update", *args)
    def pop(self, *args):
        return self._lazy("pop", *args)
    def popitem(self, *args):
        return self._lazy("popitem", *args)

class lazylist(list):

    def load(self):
        # Must be overridden in a subclass.
        # Must load data with list.append(self, v) instead of lazylist.append(v).
        pass

    def _lazy(self, method, *args):
        """ If the list is empty, calls lazylist.load().
            Replaces lazylist.method() with list.method() and calls it.
        """
        if list.__len__(self) == 0:
            self.load()
            setattr(self, method, types.MethodType(getattr(list, method), self))
        return getattr(list, method)(self, *args)

    def __repr__(self):
        return self._lazy("__repr__")
    def __len__(self):
        return self._lazy("__len__")
    def __iter__(self):
        return self._lazy("__iter__")
    def __contains__(self, *args):
        return self._lazy("__contains__", *args)
    def insert(self, *args):
        return self._lazy("insert", *args)
    def append(self, *args):
        return self._lazy("append", *args)
    def extend(self, *args):
        return self._lazy("extend", *args)
    def remove(self, *args):
        return self._lazy("remove", *args)
    def pop(self, *args):
        return self._lazy("pop", *args)

#--- TOKENIZER -------------------------------------------------------------------------------------

TOKEN = re.compile(r"(\S+)\s")

# Handle common punctuation marks.
PUNCTUATION = \
punctuation = ".,;:!?()[]{}`''\"@#$^&*+-|=~_"

# Handle common abbreviations.
ABBREVIATIONS = abbreviations = set((
    "a.", "adj.", "adv.", "al.", "a.m.", "c.", "cf.", "comp.", "conf.", "def.",
    "ed.", "e.g.", "esp.", "etc.", "ex.", "f.", "fig.", "gen.", "id.", "i.e.",
    "int.", "l.", "m.", "Med.", "Mil.", "Mr.", "n.", "n.q.", "orig.", "pl.",
    "pred.", "pres.", "p.m.", "ref.", "v.", "vs.", "w/"
))

RE_ABBR1 = re.compile("^[A-Za-z]\.$")       # single letter, "T. De Smedt"
RE_ABBR2 = re.compile("^([A-Za-z]\.)+$")    # alternating letters, "U.S."
RE_ABBR3 = re.compile("^[A-Z][" + "|".join( # capital followed by consonants, "Mr."
        "bcdfghjklmnpqrstvwxz") + "]+.$")

RE_SMILEY = (r"[:|8]", r"-?", r"[\)|\(|D|S|o|p|s]") # eyes|nose|mouth :-)
RE_SMILEY = re.compile(r"(%s) ?(%s) ?(%s)" % RE_SMILEY)

# Handle common contractions.
replacements = {
     "'d": " 'd",
     "'m": " 'm",
     "'s": " 's",
    "'ll": " 'll",
    "'re": " 're",
    "'ve": " 've",
    "n't": " n't"
}

# Handle paragraph line breaks (\n\n marks end of sentence).
EOS = "END-OF-SENTENCE"

def find_tokens(string, punctuation=PUNCTUATION, abbreviations=ABBREVIATIONS, replace=replacements, linebreak=r"\n{2,}"):
    """ Returns a list of sentences. Each sentence is a space-separated string of tokens (words).
        Handles common cases of abbreviations (e.g., etc., ...).
        Punctuation marks are split from other words. Periods (or ?!) mark the end of a sentence.
        Headings without an ending period are inferred by line breaks.
    """
    # Handle periods separately.
    punctuation = tuple(punctuation.replace(".", ""))
    # Handle replacements (contractions).
    for a, b in replace.items():
        string = re.sub(a, b, string)
    # Handle Unicode quotes.
    if isinstance(string, unicode):
        string = string.replace(u"“", u" “ ")
        string = string.replace(u"”", u" ” ")
        string = string.replace(u"‘", u" ‘ ")
        string = string.replace(u"’", u" ’ ")
    # Collapse whitespace.
    string = re.sub("\r\n", "\n", string)
    string = re.sub(linebreak, " %s " % EOS, string)
    string = re.sub(r"\s+", " ", string)
    tokens = []
    for t in TOKEN.findall(string+" "):
        if len(t) > 0:
            tail = []
            while t.startswith(punctuation) and \
              not t in replace:
                # Split leading punctuation.
                if t.startswith(punctuation):
                    tokens.append(t[0]); t=t[1:]
            while t.endswith(punctuation+(".",)) and \
              not t in replace:
                # Split trailing punctuation.
                if t.endswith(punctuation):
                    tail.append(t[-1]); t=t[:-1]
                # Split ellipsis (...) before splitting period.
                if t.endswith("..."):
                    tail.append("..."); t=t[:-3].rstrip(".")
                # Split period (if not an abbreviation).
                if t.endswith("."):
                    if t in abbreviations or \
                      RE_ABBR1.match(t) is not None or \
                      RE_ABBR2.match(t) is not None or \
                      RE_ABBR3.match(t) is not None:
                        break
                    else:
                        tail.append(t[-1]); t=t[:-1]
            if t != "":
                tokens.append(t)
            tokens.extend(reversed(tail))
    sentences, i, j = [[]], 0, 0
    while j < len(tokens):
        if tokens[j] in ("...", ".", "!", "?", EOS):
            # There may be a trailing parenthesis.
            while j < len(tokens) \
              and tokens[j] in ("...", ".", "!", "?", ")", "'", "\"", u"”", u"’", EOS):
                j += 1
            sentences[-1].extend(t for t in tokens[i:j] if t != EOS)
            sentences.append([])
            i = j
        j += 1
    sentences[-1].extend(tokens[i:j])
    sentences = [" ".join(s) for s in sentences if len(s) > 0]
    sentences = [RE_SMILEY.sub("\\1\\2\\3", s) for s in sentences]
    return sentences

#### LEXICON #######################################################################################

#--- LEXICON ---------------------------------------------------------------------------------------
# Pattern's text parsers are based on Brill's algorithm.
# Brill's algorithm automatically acquires a lexicon of known words,
# and a set of rules for tagging unknown words from a training corpus.
# Lexical rules are used to tag unknown words, based on the word morphology (prefix, suffix, ...).
# Contextual rules are used to tag all words, based on the word's role in the sentence.
# Named entity rules are used to discover proper nouns (NNP's).

def _read(path, encoding="utf-8", comment=";;;"):
    """ Returns an iterator over the lines in the file at the given path,
        strippping comments and decoding each line to Unicode.
    """
    if path:
        if isinstance(path, basestring) and os.path.exists(path):
            # From file path.
            f = open(path)
        elif isinstance(path, basestring):
            # From string.
            f = path.splitlines()
        elif hasattr(path, "read"):
            # From string buffer.
            f = path.read().splitlines()
        else:
            f = path
        for line in f:
            line = decode_utf8(line.strip())
            if comment and line.startswith(comment):
                continue
            yield line
    raise StopIteration

class Lexicon(lazydict):

    def __init__(self, path="", morphology=None, context=None, entities=None, NNP="NNP", language=None):
        """ A dictionary of words and their part-of-speech tags.
            For unknown words, rules for word morphology, context and named entities can be used.
        """
        self._path = path
        self._language  = language
        self.morphology = Morphology(self, path=morphology)
        self.context    = Context(self, path=context)
        self.entities   = Entities(self, path=entities, tag=NNP)

    def load(self):
        # Arnold NNP x
        dict.update(self, (x.split(" ")[:2] for x in _read(self._path) if x.strip()))

    @property
    def path(self):
        return self._path

    @property
    def language(self):
        return self._language


#--- MORPHOLOGICAL RULES ---------------------------------------------------------------------------
# Brill's algorithm generates lexical (i.e., morphological) rules in the following format:
# NN s fhassuf 1 NNS x => unknown words ending in -s and tagged NN change to NNS.
#     ly hassuf 2 RB x => unknown words ending in -ly change to RB.

class Rules:

    def __init__(self, lexicon={}, cmd={}):
        self.lexicon, self.cmd = lexicon, cmd

    def apply(self, x):
        """ Applies the rule to the given token or list of tokens.
        """
        return x

class Morphology(lazylist, Rules):

    def __init__(self, lexicon={}, path=""):
        """ A list of rules based on word morphology (prefix, suffix).
        """
        cmd = ("char", # Word contains x.
            "haspref", # Word starts with x.
             "hassuf", # Word end with x.
            "addpref", # x + word is in lexicon.
             "addsuf", # Word + x is in lexicon.
         "deletepref", # Word without x at the start is in lexicon.
          "deletesuf", # Word without x at the end is in lexicon.
           "goodleft", # Word preceded by word x.
          "goodright", # Word followed by word x.
        )
        cmd = dict.fromkeys(cmd, True)
        cmd.update(("f" + k, v) for k, v in cmd.items())
        Rules.__init__(self, lexicon, cmd)
        self._path = path

    @property
    def path(self):
        return self._path

    def load(self):
        # ["NN", "s", "fhassuf", "1", "NNS", "x"]
        list.extend(self, (x.split() for x in _read(self._path)))

    def apply(self, token, previous=(None, None), next=(None, None)):
        """ Applies lexical rules to the given token,
            which is a [word, tag] list.
        """
        w = token[0]
        for r in self:
            if r[1] in self.cmd: # Rule = ly hassuf 2 RB x
                f, x, pos, cmd = bool(0), r[0], r[-2], r[1]
            if r[2] in self.cmd: # Rule = NN s fhassuf 1 NNS x
                f, x, pos, cmd = bool(1), r[1], r[-2], r[2].lstrip("f")
            if f and token[1] != r[0]:
                continue
            if (cmd == "char"       and x in w) \
            or (cmd == "haspref"    and w.startswith(x)) \
            or (cmd == "hassuf"     and w.endswith(x)) \
            or (cmd == "addpref"    and x + w in self.lexicon) \
            or (cmd == "addsuf"     and w + x in self.lexicon) \
            or (cmd == "deletepref" and w.startswith(x) and w[len(x):] in self.lexicon) \
            or (cmd == "deletesuf"  and w.endswith(x) and w[:-len(x)] in self.lexicon) \
            or (cmd == "goodleft"   and x == next[0]) \
            or (cmd == "goodright"  and x == previous[0]):
                token[1] = pos
        return token

#--- CONTEXT RULES ---------------------------------------------------------------------------------
# Brill's algorithm generates contextual rules in the following format:
# VBD VB PREVTAG TO => unknown word tagged VBD changes to VB if preceded by a word tagged TO.

class Context(lazylist, Rules):

    def __init__(self, lexicon={}, path=""):
        """ A list of rules based on context (preceding and following words).
        """
        cmd = ("prevtag", # Preceding word is tagged x.
               "nexttag", # Following word is tagged x.
              "prev2tag", # Word 2 before is tagged x.
              "next2tag", # Word 2 after is tagged x.
           "prev1or2tag", # One of 2 preceding words is tagged x.
           "next1or2tag", # One of 2 following words is tagged x.
        "prev1or2or3tag", # One of 3 preceding words is tagged x.
        "next1or2or3tag", # One of 3 following words is tagged x.
           "surroundtag", # Preceding word is tagged x and following word is tagged y.
                 "curwd", # Current word is x.
                "prevwd", # Preceding word is x.
                "nextwd", # Following word is x.
            "prev1or2wd", # One of 2 preceding words is x.
            "next1or2wd", # One of 2 following words is x.
         "next1or2or3wd", # One of 3 preceding words is x.
         "prev1or2or3wd", # One of 3 following words is x.
             "prevwdtag", # Preceding word is x and tagged y.
             "nextwdtag", # Following word is x and tagged y.
              "wdprevwd", # Current word is x and preceding word is y.
              "wdnextwd", # Current word is x and following word is y.
             "wdprevtag", # Current word is x and preceding word is tagged y.
             "wdnexttag", # Current word is x and following word is tagged y.
             "wdand2aft", # Current word is x and word 2 after is y.
          "wdand2tagbfr", # Current word is x and word 2 before is tagged y.
          "wdand2tagaft", # Current word is x and word 2 after is tagged y.
               "lbigram", # Preceding word is x and word before is y.
               "rbigram", # Following word is x and word after is y.
            "prevbigram", # Preceding word is tagged x and word before is tagged y.
            "nextbigram", # Following word is tagged x and word after is tagged y.
        )
        Rules.__init__(self, lexicon, dict.fromkeys(cmd, True))
        self._path = path

    @property
    def path(self):
        return self._path

    def load(self):
        # ["VBD", "VB", "PREVTAG", "TO"]
        list.extend(self, (x.split() for x in _read(self._path)))

    def apply(self, tokens):
        """ Applies contextual rules to the given list of tokens,
            where each token is a [word, tag] list.
        """
        o = [("STAART", "STAART")] * 3 # Empty delimiters for look ahead/back.
        t = o + tokens + o
        for i, token in enumerate(t):
            for r in self:
                if token[1] == "STAART":
                    continue
                if token[1] != r[0] and r[0] != "*":
                    continue
                cmd, x, y = r[2], r[3], r[4] if len(r) > 4 else ""
                cmd = cmd.lower()
                if (cmd == "prevtag"        and x ==  t[i-1][1]) \
                or (cmd == "nexttag"        and x ==  t[i+1][1]) \
                or (cmd == "prev2tag"       and x ==  t[i-2][1]) \
                or (cmd == "next2tag"       and x ==  t[i+2][1]) \
                or (cmd == "prev1or2tag"    and x in (t[i-1][1], t[i-2][1])) \
                or (cmd == "next1or2tag"    and x in (t[i+1][1], t[i+2][1])) \
                or (cmd == "prev1or2or3tag" and x in (t[i-1][1], t[i-2][1], t[i-3][1])) \
                or (cmd == "next1or2or3tag" and x in (t[i+1][1], t[i+2][1], t[i+3][1])) \
                or (cmd == "surroundtag"    and x ==  t[i-1][1] and y == t[i+1][1]) \
                or (cmd == "curwd"          and x ==  t[i+0][0]) \
                or (cmd == "prevwd"         and x ==  t[i-1][0]) \
                or (cmd == "nextwd"         and x ==  t[i+1][0]) \
                or (cmd == "prev1or2wd"     and x in (t[i-1][0], t[i-2][0])) \
                or (cmd == "next1or2wd"     and x in (t[i+1][0], t[i+2][0])) \
                or (cmd == "prevwdtag"      and x ==  t[i-1][0] and y == t[i-1][1]) \
                or (cmd == "nextwdtag"      and x ==  t[i+1][0] and y == t[i+1][1]) \
                or (cmd == "wdprevwd"       and x ==  t[i+0][0] and y == t[i-1][0]) \
                or (cmd == "wdnextwd"       and x ==  t[i+0][0] and y == t[i+1][0]) \
                or (cmd == "wdprevtag"      and x ==  t[i+0][0] and y == t[i-1][1]) \
                or (cmd == "wdnexttag"      and x ==  t[i+0][0] and y == t[i+1][1]) \
                or (cmd == "wdand2aft"      and x ==  t[i+0][0] and y == t[i+2][0]) \
                or (cmd == "wdand2tagbfr"   and x ==  t[i+0][0] and y == t[i-2][1]) \
                or (cmd == "wdand2tagaft"   and x ==  t[i+0][0] and y == t[i+2][1]) \
                or (cmd == "lbigram"        and x ==  t[i-1][0] and y == t[i][0]) \
                or (cmd == "rbigram"        and x ==  t[i+0][0] and y == t[i+1][0]) \
                or (cmd == "prevbigram"     and x ==  t[i-2][1] and y == t[i-1][1]) \
                or (cmd == "nextbigram"     and x ==  t[i+1][1] and y == t[i+2][1]):
                    tokens[i-len(o)] = [tokens[i-len(o)][0], r[1]]
        return tokens

#--- NAMED ENTITY RECOGNIZER -----------------------------------------------------------------------

RE_ENTITY1 = re.compile(r"^http://")                            # http://www.domain.com/path
RE_ENTITY2 = re.compile(r"^www\..*?\.[com|org|net|edu|de|uk]$") # www.domain.com
RE_ENTITY3 = re.compile(r"^[\w\-\.\+]+@(\w[\w\-]+\.)+[\w\-]+$") # name@domain.com

class Entities(lazydict, Rules):

    def __init__(self, lexicon={}, path="", tag="NNP"):
        """ A dictionary of named entities and their labels.
            For domain names and e-mail adresses, regular expressions are used.
        """
        cmd = (
            "pers", # Persons: George/NNP-PERS
             "loc", # Locations: Washington/NNP-LOC
             "org", # Organizations: Google/NNP-ORG
        )
        Rules.__init__(self, lexicon, cmd)
        self._path = path
        self.tag   = tag

    @property
    def path(self):
        return self._path

    def load(self):
        # ["Alexander", "the", "Great", "PERS"]
        # {"alexander": [["alexander", "the", "great", "pers"], ...]}
        for x in _read(self.path):
            x = [x.lower() for x in x.split()]
            dict.setdefault(self, x[0], []).append(x)

    def apply(self, tokens):
        """ Applies the named entity recognizer to the given list of tokens,
            where each token is a [word, tag] list.
        """
        # Note: we could also scan for patterns, e.g.,
        # "my|his|her name is|was *" => NNP-PERS.
        i = 0
        while i < len(tokens):
            w = tokens[i][0].lower()
            if RE_ENTITY1.match(w) \
            or RE_ENTITY2.match(w) \
            or RE_ENTITY3.match(w):
                tokens[i][1] = self.tag
            if w in self:
                for e in self[w]:
                    # Look ahead to see if successive words match the named entity.
                    e, tag = (e[:-1], "-"+e[-1].upper()) if e[-1] in self.cmd else (e, "")
                    b = True
                    for j, e in enumerate(e):
                        if i + j >= len(tokens) or tokens[i+j][0].lower() != e:
                            b = False; break
                    if b:
                        for token in tokens[i:i+j+1]:
                            token[1] = (token[1] == "NNPS" and token[1] or self.tag) + tag
                        i += j
                        break
            i += 1
        return tokens

### SENTIMENT POLARITY LEXICON #####################################################################
# A sentiment lexicon can be used to discern objective facts from subjective opinions in text.
# Each word in the lexicon has scores for:
# 1)     polarity: negative vs. positive    (-1.0 => +1.0)
# 2) subjectivity: objective vs. subjective (+0.0 => +1.0)
# 3)    intensity: modifies next word?   (x0.5 => x2.0)

# For English, adverbs are used as modifiers.
# For Dutch, adverbial adjectives are used as modifiers
# ("hopeloos voorspelbaar", "ontzettend spannend", "verschrikkelijk goed").
# Negation words (e.g., "not") reverse the polarity of the following word.

NOUN, VERB, ADJECTIVE, ADVERB = \
    "NN", "VB", "JJ", "RB"

RE_SYNSET = re.compile(r"^[acdnrv][-_][0-9]+$")

def avg(list):
    return sum(list) / float(len(list) or 1)

class Score(tuple):

    def __new__(self, polarity, subjectivity, assessments=[]):
        """ A (polarity, subjectivity)-tuple with an assessments property.
        """
        return tuple.__new__(self, [polarity, subjectivity])

    def __init__(self, polarity, subjectivity, assessments=[]):
        self.assessments = assessments

class Sentiment(lazydict):

    def __init__(self, path="", language=None, synset=None, confidence=None, **kwargs):
        """ A dictionary of words (adjectives) and polarity scores (positive/negative).
            The value for each word is a dictionary of part-of-speech tags.
            The value for each word POS-tag is a tuple with values for
            polarity (-1.0-1.0), subjectivity (0.0-1.0) and intensity (0.5-2.0).
        """
        self._path       = path
        self._language   = None
        self._confidence = None
        self._synset     = synset
        self._synsets    = {}
        self.tokenizer   = kwargs.get("tokenizer", find_tokens)
        self.negations   = kwargs.get("negations", ("no", "not", "n't", "never"))
        self.modifiers   = kwargs.get("modifiers", ("RB",))
        self.modifier    = kwargs.get("modifier" , lambda w: w.endswith("ly"))

    @property
    def path(self):
        return self._path

    @property
    def language(self):
        return self._language

    @property
    def confidence(self):
        return self._confidence

    def load(self):
        # <word form="great" wordnet_id="a-01123879" pos="JJ" polarity="1.0" subjectivity="1.0" intensity="1.0" />
        if not os.path.exists(self._path):
            return
        words, synsets = {}, {}
        xml = cElementTree.parse(self._path)
        xml = xml.getroot()
        for w in xml.findall("word"):
            if self._confidence is None \
            or self._confidence <= float(w.attrib.get("confidence", 0.0)):
                w, pos, p, s, i, synset = (
                    w.attrib.get("form"),
                    w.attrib.get("pos"),
                    w.attrib.get("polarity", 0.0),
                    w.attrib.get("subjectivity", 0.0),
                    w.attrib.get("intensity", 1.0),
                    w.attrib.get(self._synset) # wordnet_id, cornetto_id, ...
                )
                psi = (float(p), float(s), float(i))
                if w:
                    words.setdefault(w, {}).setdefault(pos, []).append(psi)
                if synset:
                    synsets.setdefault(synset, []).append(psi)
        self._language = xml.attrib.get("language", self._language)
        # Average scores of all word senses per part-of-speech tag.
        for w in words:
            words[w] = dict((pos, map(avg, zip(*psi))) for pos, psi in words[w].items())
        # Average scores of all part-of-speech tags.
        for w, pos in words.items():
            words[w][None] = map(avg, zip(*pos.values()))
        # Average scores of all synonyms per synset.
        for id, psi in synsets.items():
            synsets[id] = map(avg, zip(*psi))
        dict.update(self, words)
        dict.update(self._synsets, synsets)

    def synset(self, id, pos=ADJECTIVE):
        """ Returns a (polarity, subjectivity)-tuple for the given synset id.
            For example, the adjective "horrible" has id 193480 in WordNet:
            Sentiment.synset(193480, pos="JJ") => (-0.6, 1.0, 1.0).
        """
        id = str(id).zfill(8)
        if not id.startswith(("n-", "v-", "a-", "r-")):
            if pos == NOUN:
                id = "n-" + id
            if pos == VERB:
                id = "v-" + id
            if pos == ADJECTIVE:
                id = "a-" + id
            if pos == ADVERB:
                id = "r-" + id
        if dict.__len__(self) == 0:
            self.load()
        return tuple(self._synsets.get(id, (0.0, 0.0))[:2])

    def __call__(self, s, negation=True, **kwargs):
        """ Returns a (polarity, subjectivity)-tuple for the given sentence,
            with polarity between -1.0 and 1.0 and subjectivity between 0.0 and 1.0.
            The sentence can be a string, Synset, Text, Sentence, Chunk, Word, Document, Vector.
            An optional weight parameter can be given,
            as a function that takes a list of words and returns a weight.
        """
        def avg(assessments, weighted=lambda w: 1):
            s, n = 0, 0
            for words, score in assessments:
                w = weighted(words)
                s += w * score
                n += w
            return s / float(n or 1)
        # A pattern.en.wordnet.Synset.
        # Sentiment(synsets("horrible", "JJ")[0]) => (-0.6, 1.0)
        if hasattr(s, "gloss"):
            a = [(s.synonyms[0],) + self.synset(s.id, pos=s.pos)]
        # A synset id.
        # Sentiment("a-00193480") => horrible => (-0.6, 1.0)   (English WordNet)
        # Sentiment("c_267") => verschrikkelijk => (-0.9, 1.0) (Dutch Cornetto)
        elif isinstance(s, basestring) and RE_SYNSET.match(s):
            a = [(s.synonyms[0],) + self.synset(s.id, pos=s.pos)]
        # A string of words.
        # Sentiment("a horrible movie") => (-0.6, 1.0)
        elif isinstance(s, basestring):
            a = self.assessments(((w.lower(), None) for w in " ".join(self.tokenizer(s)).split()), negation)
        # A pattern.en.Text.
        elif hasattr(s, "sentences"):
            a = self.assessments(((w.lemma or w.string.lower(), w.pos[:2]) for w in chain(*s)), negation)
        # A pattern.en.Sentence or pattern.en.Chunk.
        elif hasattr(s, "lemmata"):
            a = self.assessments(((w.lemma or w.string.lower(), w.pos[:2]) for w in s.words), negation)
        # A pattern.en.Word.
        elif hasattr(s, "lemma"):
            a = self.assessments(((s.lemma or s.string.lower(), s.pos[:2]),), negation)
        # A pattern.vector.Document.
        # Average score = weighted average using feature weights.
        elif hasattr(s, "terms"):
            a = self.assessments(((w, None) for w in s.terms), negation)
            kwargs.setdefault("weight", lambda w: s.terms[w[0]])
        # A dict of (word, weight)-items.
        elif isinstance(s, dict):
            a = self.assessments(((w, None) for w in s), negation)
            kwargs.setdefault("weight", lambda w: s[w[0]])
        # A list of words.
        elif isinstance(s, list):
            a = self.assessments(((w, None) for w in s), negation)
        else:
            a = []
        weight = kwargs.get("weight", lambda w: 1)
        return Score(polarity = avg(map(lambda (w, p, s): (w, p), a), weight),
                 subjectivity = avg(map(lambda (w, p, s): (w, s), a), weight),
                  assessments = a)

    def assessments(self, words=[], negation=True):
        """ Returns a list of (chunk, polarity, subjectivity)-tuples for the given list of words,
            where chunk is a list of successive words: a known word optionally
            preceded by a modifier ("very good") or a negation ("not good").
        """
        a = []
        m = None # Preceding modifier (i.e., adverb or adjective).
        n = None # Preceding negation (e.g., "not beautiful").
        for w, pos in words:
            # Only assess known words, preferably by part-of-speech tag.
            # Including unknown words (polarity 0.0 and subjectivity 0.0) lowers the average.
            if w in self and pos in self[w]:
                p, s, i = self[w][pos]
                # Known word not preceded by a modifier ("good").
                if m is None:
                    a.append(dict(w=[w], p=p, s=s, i=i, n=1))
                # Known word preceded by a modifier ("really good").
                if m is not None:
                    a[-1]["w"].append(w)
                    a[-1]["p"] = min(p * a[-1]["i"], 1.0)
                    a[-1]["s"] = min(p * a[-1]["i"], 1.0)
                    a[-1]["i"] = i
                # Known word preceded by a negation ("not really good").
                if n is not None:
                    a[-1]["w"].insert(0, n)
                    a[-1]["i"] = 1.0 / a[-1]["i"]
                    a[-1]["n"] = -1
                # Known word may be a negation.
                # Known word may be modifying the next word (i.e., it is a known adverb).
                m = None
                n = None
                if pos and pos in self.modifiers or any(map(self[w].__contains__, self.modifiers)):
                    m = (w, pos)
                if negation and w in self.negations:
                    n = w
            else:
                # Unknown word may be a negation ("not good").
                if negation and w in self.negations:
                    n = w
                # Unknown word. Retain negation across small words ("not a good").
                elif n and len(w.strip("'")) > 1:
                    n = None
                # Unknown word may be a negation preceded by a modifier ("really not good").
                if n is not None and m is not None and (pos in self.modifiers or self.modifier(m[0])):
                    a[-1]["w"].append(n)
                    a[-1]["n"] = -1
                    n = None
                # Unknown word. Retain modifier across small words ("really is a good").
                elif m and len(w) > 2:
                    m = None
                # Exclamation marks boost previous words.
                if w == "!" and len(a) > 0:
                    for x in a[-3:]: x["p"] = min(x["p"] * 1.25, 1.0)
                # Emoticon (happy).
                if w in (":)", ":-)", ":-d", "<3", u"♥"):
                    a.append(dict(w=[w], p=+1.0, s=1.0, i=1.0, n=1))
                # Emoticon (sad).
                if w in (":(", ":-(", ":-s"):
                    a.append(dict(w=[w], p=-1.0, s=1.0, i=1.0, n=1))
        for i in range(len(a)):
            w = a[i]["w"]
            p = a[i]["p"]
            s = a[i]["s"]
            n = a[i]["n"]
            # "not good" = slightly bad, "not bad" = slightly good.
            a[i] = (w, p * -0.5 if n < 0 else p, s)
        return a


#### PARSER ########################################################################################

#--- PARSER ----------------------------------------------------------------------------------------
# A shallow parser can be used to retrieve syntactic-semantic information from text
# in an efficient way (usually at the expense of deeper configurational syntactic information).
# The shallow parser in Pattern is meant to handle the following tasks:
# 1)  Tokenization: split punctuation marks from words and find sentence periods.
# 2)       Tagging: find the part-of-speech tag of each word (noun, verb, ...) in a sentence.
# 3)      Chunking: find words that belong together in a phrase.
# 4) Role labeling: find the subject and object of the sentence.
# 5) Lemmatization: find the base form of each word ("was" => "is").

#    WORD     TAG     CHUNK      PNP        ROLE        LEMMA
#------------------------------------------------------------------
#     The      DT      B-NP        O        NP-SBJ-1      the
#   black      JJ      I-NP        O        NP-SBJ-1      black
#     cat      NN      I-NP        O        NP-SBJ-1      cat
#     sat      VB      B-VP        O        VP-1          sit
#      on      IN      B-PP      B-PNP      PP-LOC        on
#     the      DT      B-NP      I-PNP      NP-OBJ-1      the
#     mat      NN      I-NP      I-PNP      NP-OBJ-1      mat
#       .      .        O          O          O           .

# The example demonstrates what information can be retrieved:
#
# - the period is split from "mat." = the end of the sentence,
# - the words are annotated: NN (noun), VB (verb), JJ (adjective), DT (determiner), ...
# - the phrases are annotated: NP (noun phrase), VP (verb phrase), PNP (preposition), ...
# - the phrases are labeled: SBJ (subject), OBJ (object), LOC (location), ...
# - the phrase start is marked: B (begin), I (inside), O (outside),
# - the past tense "sat" is lemmatized => "sit".

class _Parser:

    def __init__(self, lexicon={}, default=("NN", "NNP", "CD"), language=None):
        """ A simple shallow parser using a Brill-based part-of-speech tagger.
            The given lexicon is a dictionary of known words and their part-of-speech tag.
            The given default tags are used for unknown words.
            Unknown words that start with a capital letter are tagged NNP (except for German).
            Unknown words that contain only digits and punctuation are tagged CD.
            The given language can be used to discern between
            Germanic and Romance languages for phrase chunking.
        """
        self.lexicon  = lexicon
        self.default  = default
        self.language = language

    def find_tokens(self, string, **kwargs):
        """ Returns a list of sentences from the given string.
            Punctuation marks are separated from each word by a space.
        """
        # "The cat purs." => ["The cat purs ."]
        return find_tokens(string,
                punctuation = kwargs.get(  "punctuation", PUNCTUATION),
              abbreviations = kwargs.get("abbreviations", ABBREVIATIONS),
                    replace = kwargs.get(      "replace", replacements),
                  linebreak = r"\n{2,}")

    def find_tags(self, tokens, **kwargs):
        """ Annotates the given list of tokens with part-of-speech tags.
            Returns a list of tokens, where each token is now a [word, tag]-list.
        """
        # ["The", "cat", "purs"] => [["The", "DT"], ["cat", "NN"], ["purs", "VB"]]
        return find_tags(tokens,
                   language = kwargs.get("language", self.language),
                    lexicon = kwargs.get( "lexicon", self.lexicon),
                    default = kwargs.get( "default", self.default),
                        map = kwargs.get(     "map", None))

    def find_chunks(self, tokens, **kwargs):
        """ Annotates the given list of tokens with chunk tags.
            Several tags can be added, for example chunk + preposition tags.
        """
        # [["The", "DT"], ["cat", "NN"], ["purs", "VB"]] =>
        # [["The", "DT", "B-NP"], ["cat", "NN", "I-NP"], ["purs", "VB", "B-VP"]]
        return find_prepositions(
               find_chunks(tokens,
                   language = kwargs.get("language", self.language)))

    def find_prepositions(self, tokens, **kwargs):
        """ Annotates the given list of tokens with prepositional noun phrase tags.
        """
        return find_prepositions(tokens) # See also Parser.find_chunks().

    def find_labels(self, tokens, **kwargs):
        """ Annotates the given list of tokens with verb/predicate tags.
        """
        return find_relations(tokens)

    def find_lemmata(self, tokens, **kwargs):
        """ Annotates the given list of tokens with word lemmata.
        """
        return [token + [token[0].lower()] for token in tokens]

    def parse(self, s, tokenize=True, tags=True, chunks=True, relations=False, lemmata=False, encoding="utf-8", **kwargs):
        """ Takes a string (sentences) and returns a tagged Unicode string (TaggedString).
            Sentences in the output are separated by newlines.
            With tokenize=True, punctuation is split from words and sentences are separated by \n.
            With tags=True, part-of-speech tags are parsed (NN, VB, IN, ...).
            With chunks=True, phrase chunk tags are parsed (NP, VP, PP, PNP, ...).
            With relations=True, semantic role labels are parsed (SBJ, OBJ).
            With lemmata=True, word lemmata are parsed.
            Optional parameters are passed to
            the tokenizer, tagger, chunker, labeler and lemmatizer.
        """
        # Tokenizer.
        if tokenize is True:
            s = self.find_tokens(s)
        if isinstance(s, (list, tuple)):
            s = [isinstance(s, basestring) and s.split(" ") or s for s in s]
        if isinstance(s, basestring):
            s = [s.split(" ") for s in s.split("\n")]
        # Unicode.
        for i in range(len(s)):
            for j in range(len(s[i])):
                if isinstance(s[i][j], str):
                    s[i][j] = decode_string(s[i][j], encoding)
            # Tagger (required by chunker, labeler & lemmatizer).
            if tags or chunks or relations or lemmata:
                s[i] = self.find_tags(s[i], **kwargs)
            else:
                s[i] = [[w] for w in s[i]]
            # Chunker.
            if chunks or relations:
                s[i] = self.find_chunks(s[i], **kwargs)
            # Labeler.
            if relations:
                s[i] = self.find_labels(s[i], **kwargs)
            # Lemmatizer.
            if lemmata:
                s[i] = self.find_lemmata(s[i], **kwargs)
        # Slash-formatted tagged string.
        # With collapse=False (or split=True), returns raw list
        # (this output is not usable by tree.Text).
        if not kwargs.get("collapse", True) \
            or kwargs.get("split", False):
            return s
        # Construct TaggedString.format.
        # (this output is usable by tree.Text).
        format = ["word"]
        if tags:
            format.append("part-of-speech")
        if chunks:
            format.extend(("chunk", "preposition"))
        if relations:
            format.append("relation")
        if lemmata:
            format.append("lemma")
        # Collapse raw list.
        # Sentences are separated by newlines, tokens by spaces, tags by slashes.
        # Slashes in words are encoded with &slash;
        for i in range(len(s)):
            for j in range(len(s[i])):
                s[i][j][0] = s[i][j][0].replace("/", "&slash;")
                s[i][j] = "/".join(s[i][j])
            s[i] = " ".join(s[i])
        s = "\n".join(s)
        s = TaggedString(s, format, language=kwargs.get("language", self.language))
        return s


#--- ENGLISH PARSER --------------------------------------------------------------------------------

def find_lemmata(tokens):
    """ Annotates the tokens with lemmata for plural nouns and conjugated verbs,
        where each token is a [word, part-of-speech] list.
    """
    for token in tokens:
        word, pos, lemma = token[0], token[1], token[0]
        # cats => cat
        if pos == "NNS":
            lemma = singularize(word)
        # sat => sit
        if pos.startswith(("VB", "MD")):
            lemma = conjugate(word, INFINITIVE) or word
        token.append(lemma.lower())
    return tokens

class Parser(_Parser):

    def find_lemmata(self, tokens, **kwargs):
        return find_lemmata(tokens)

lexicon = Lexicon(
        path = os.path.join(MODULE, "en-lexicon.txt"),
  morphology = os.path.join(MODULE, "en-morphology.txt"),
     context = os.path.join(MODULE, "en-context.txt"),
    entities = os.path.join(MODULE, "en-entities.txt"),
    language = "en"
)
parser = Parser(
     lexicon = lexicon,
     default = ("NN", "NNP", "CD"),
    language = "en"
)

sentiment = Sentiment(
        path = os.path.join(MODULE, "en-sentiment.xml"),
      synset = "wordnet_id",
   negations = ("no", "not", "n't", "never"),
   modifiers = ("RB",),
   modifier  = lambda w: w.endswith("ly"),
   tokenizer = parser.find_tokens,
    language = "en"
)
