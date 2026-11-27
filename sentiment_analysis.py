# textblob/sentiments.py (or a new module)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC


class SVMSentimentAnalyzer:
    def __init__(self):
        # Initialize an SVM Pipeline with TF-IDF vectorization
        self.pipeline = Pipeline([("tfidf", TfidfVectorizer()), ("clf", LinearSVC())])

    def train(self, train_texts, train_labels):
        # Trains the SVM classifier on the provided training data
        self.pipeline.fit(train_texts, train_labels)

    def analyze(self, text):
        # Predicts the sentiment of the given text
        prediction = self.pipeline.predict([text])[0]
        return prediction
