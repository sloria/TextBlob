"""
Author: Kapil Reddy Sanikommu
Date: 10-13-25
Description:
Implements sentiment classification using SVM and TF-IDF features.
Part of DATA 245 open-source contribution exercise.
"""


"""
svm_sentiment.py
----------------
This script uses Support Vector Machine (SVM) to predict text sentiment
(positive, negative, or neutral). It demonstrates integration with TextBlob
and scikit-learn for open-source contribution practice.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd

# Sample dataset
data = {
    'text': [
        "I love this product, it’s amazing!",
        "This is the worst experience ever.",
        "It’s okay, not too bad but not great.",
        "Absolutely wonderful, I’m so happy!",
        "I hate this item, it’s terrible.",
        "Pretty decent overall, could be better.",
        "Fantastic quality, I’ll buy again!",
        "Awful, I want my money back.",
        "Not bad, but delivery was slow.",
        "Really good and works perfectly.",
        "Terrible experience, not recommended.",
        "Mediocre at best, nothing special.",
        "Excellent! Way better than I expected.",
        "Poor quality, very disappointing.",
        "Just fine, nothing to complain about.",
        "Love it! Worth every penny.",
        "Waste of money, horrible product.",
        "Satisfied overall with this purchase.",
        "Bad packaging but works okay.",
        "Great results, super happy with it!"
    ],
    'sentiment': [
        'positive', 'negative', 'neutral', 'positive', 'negative',
        'neutral', 'positive', 'negative', 'neutral', 'positive',
        'negative', 'neutral', 'positive', 'negative', 'neutral',
        'positive', 'negative', 'positive', 'neutral', 'positive'
    ]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Split data
X_train, X_test, y_train, y_test = train_test_split(df['text'], df['sentiment'], test_size=0.3, random_state=42)

# Create an SVM pipeline
model = make_pipeline(TfidfVectorizer(), SVC(kernel='linear', probability=True))

# Train the model
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("Classification Report:\n")
print(metrics.classification_report(y_test, y_pred, zero_division=1))


# Example predictions
examples = [
    "I really enjoyed using this!",
    "It was a horrible experience.",
    "Nothing special, just average."
]
predictions = model.predict(examples)

print("\nExample predictions:")
for text, pred in zip(examples, predictions):
    print(f"Text: {text}\nPredicted sentiment: {pred}\n")
