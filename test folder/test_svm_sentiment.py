"""
Unit test sample
"""

import unittest

import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.svm import SVC


class TestSentimentAnalysis(unittest.TestCase):
    def test_sentiment_pipeline(self):
        """Testing the SVM sentiment model trains and predicts correctly"""

        # Loading dataset
        df = pd.read_csv("data/Starbucks_reviews.csv")

        # Map ratings to sentiments labels
        def map_sentiment(rating):
            if rating >= 4:
                return "positive"
            elif rating == 3:
                return "neutral"
            else:
                return "negative"

        df["sentiment"] = df["Rating"].apply(map_sentiment)

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            df["Review"], df["sentiment"], test_size=0.2, random_state=42
        )

        # Model pipeline
        model = make_pipeline(
            TfidfVectorizer(stop_words="english", max_features=3000),
            SVC(kernel="linear"),
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # Evaluate
        accuracy = metrics.accuracy_score(y_test, y_pred)
        print(f"Test Accuracy: {accuracy:.2f}")

        # Assert that accuracy is above a reasonable threshold
        self.assertGreater(accuracy, 0.70)


if __name__ == "__main__":
    unittest.main()
