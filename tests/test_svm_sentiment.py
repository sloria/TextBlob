import unittest

# Import your newly created analyzer class from your package module
from sentiment_analysis import SVMSentimentAnalyzer


class TestSVMSentimentAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up and train the SVM classifier with a robust sample corpus."""
        self.analyzer = SVMSentimentAnalyzer()

        train_texts = [
            # Positive examples
            "I absolutely love this, it is fantastic and wonderful!",
            "Best experience ever, I highly recommend it.",
            "Truly brilliant, amazing, and outstanding quality.",
            "I am so happy and thrilled with this incredible result.",
            # Negative examples
            "This is terrible, awful, and completely broken.",
            "Worst product ever, a total waste of time and money.",
            "Horrible failure, completely unusable and disappointing.",
            "I hate this experience, it is absolute garbage.",
            # Neutral examples
            "It is okay, just an average, everyday item.",
            "Nothing special here, completely standard and fine.",
            "It meets basic expectations, nothing more or less.",
            "Standard procedure, functioning as normally expected.",
        ]
        train_labels = [
            "positive",
            "positive",
            "positive",
            "positive",
            "negative",
            "negative",
            "negative",
            "negative",
            "neutral",
            "neutral",
            "neutral",
            "neutral",
        ]

        # Train the model
        self.analyzer.train(train_texts, train_labels)

    def test_positive_sentiment(self):
        """Verify that positive text is correctly classified as 'positive'."""
        text = "Truly brilliant and amazing execution!"
        prediction = self.analyzer.analyze(text)
        self.assertEqual(prediction, "positive")

    def test_negative_sentiment(self):
        """Verify that negative text is correctly classified as 'negative'."""
        text = "Horrible failure, completely unusable."
        prediction = self.analyzer.analyze(text)
        self.assertEqual(prediction, "negative")

    def test_neutral_sentiment(self):
        """Verify that neutral text is correctly classified as 'neutral'."""
        text = "It is a standard, normal object."
        prediction = self.analyzer.analyze(text)
        self.assertEqual(prediction, "neutral")


if __name__ == "__main__":
    unittest.main()
