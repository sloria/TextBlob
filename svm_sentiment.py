from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import make_pipeline

class SVMSentimentClassifier:
    def __init__(self):
        self.model = make_pipeline(TfidfVectorizer(), LinearSVC())

    def train(self, texts, labels):
        """Train the classifier with labeled text data"""
        self.model.fit(texts, labels)

    def predict(self, text):
        return self.model.predict([text])[0]


if __name__ == "__main__":
    texts = [
        "I love this movie!",
        "That was terrible.",
        "It's okay, not bad",
        "Absolutely amazing",
        "Worst thing ever.",
        "Fine but forgettable.",
    ]
    labels = ["positive", "negative", "neutral", "positive", "negative", "neutral"]

    clf = SVMSentimentClassifier()
    clf.train(texts, labels)

    test = ["This was awesome!", "I didn't like it.", "It's average."]
    for t in test:
        print(t, "->", clf.predict(t))
        
