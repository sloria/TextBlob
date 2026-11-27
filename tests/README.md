## SVM Sentiment Analysis Feature

This repository now includes a Support Vector Machine (SVM) multi-class sentiment classifier powered by `scikit-learn` under the hood. It classifies text into **positive**, **negative**, or **neutral** categories using TF-IDF feature extraction and a Linear Support Vector Classifier (`LinearSVC`).

### Usage Example

You can import and use the `SVMSentimentAnalyzer` as follows:

```python
from TextBlob.sentiment_analysis import SVMSentimentAnalyzer

# 1. Initialize the analyzer
analyzer = SVMSentimentAnalyzer()

# 2. Provide training data (texts and corresponding multi-class labels)
train_texts = [
    "I absolutely love this, it is fantastic and wonderful!", 
    "This is terrible, awful, and completely broken.",
    "It is okay, just an average, everyday item."
]
train_labels = ["positive", "negative", "neutral"]

analyzer.train(train_texts, train_labels)

# 3. Predict sentiment for new text
prediction = analyzer.analyze("Truly brilliant and amazing execution!")
print(prediction)  # Output: positive