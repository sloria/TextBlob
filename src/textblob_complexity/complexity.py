# textblob-complexity/complexity.py
import nltk

# Set the NLTK data path explicitly
# nltk.data.path.append('/Users/rahulkailasa/Documents/GitHub/TextBlob/env/nltk_data/')
nltk.data.path.append('/Users/rahulkailasa/nltk_data')
from textblob import TextBlob
import math

class TextComplexityScorer:
    """
    A class to compute various text complexity scores.

    Methods:
    --------
    ari():
        Computes the Automated Readability Index (ARI) for the text.
    
    flesch_kincaid_grade():
        Computes the Flesch-Kincaid Grade Level for the text.
    
    gunning_fog():
        Computes the Gunning Fog Index for the text.
    
    smog_index():
        Computes the SMOG Index for the text.
    
    compute_scores():
        Returns a dictionary containing all complexity scores.
    """

    def __init__(self, text):
        self.text = text
        self.blob = TextBlob(text)
        self.sentences = self.blob.sentences
        self.words = self.blob.words
        self.total_words = len(self.words)
        self.total_sentences = len(self.sentences)

    def count_syllables(self, word):
        """Count syllables in a word."""
        vowels = "aeiouy"
        word = word.lower()
        count = 0
        if word[0] in vowels:
            count += 1
        for i in range(1, len(word)):
            if word[i] in vowels and word[i - 1] not in vowels:
                count += 1
        if word.endswith("e"):
            count -= 1
        if count == 0:
            count += 1
        return count

    def flesch_kincaid_grade(self):
        total_syllables = sum(self.count_syllables(word) for word in self.words)
        return 0.39 * (self.total_words / self.total_sentences) + 11.8 * (total_syllables / self.total_words) - 15.59

    def gunning_fog(self):
        complex_words = [word for word in self.words if self.count_syllables(word) > 2]
        return 0.4 * ((self.total_words / self.total_sentences) + 100 * (len(complex_words) / self.total_words))

    def smog_index(self):
        complex_words = [word for word in self.words if self.count_syllables(word) > 2]
        return 1.0430 * math.sqrt(len(complex_words) * (30 / self.total_sentences)) + 3.1291

    def ari(self):
        total_characters = sum(len(word) for word in self.words)
        return 4.71 * (total_characters / self.total_words) + 0.5 * (self.total_words / self.total_sentences) - 21.43

    def compute_scores(self):
        """
        Computes and returns a dictionary of all text complexity scores.

        Returns:
        -------
        dict
            A dictionary with keys as score names and values as the computed scores.
        """
        return {
            "Flesch-Kincaid Grade Level": self.flesch_kincaid_grade(),
            "Gunning Fog Index": self.gunning_fog(),
            "SMOG Index": self.smog_index(),
            "Automated Readability Index": self.ari()
        }
