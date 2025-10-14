import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn import metrics

# Loading dataset
df = pd.read_csv("data/Starbucks_reviews.csv")

# Mapping ratings to sentiment labels

def map_sentiment(rating):
    """Convert numerical ratings into categorical sentiments."""

    if rating >= 4:
        return "positive"
    elif rating == 3:
        return "neutral"
    else:
        return "negative"
    
df['sentiment'] = df['Rating'].apply(map_sentiment)

# Preparing features and target
X = df['Review']
Y = df['sentiment']

# Splitting data into training set and testing set
X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y, test_size = 0.2, random_state = 42
)

# Building and training SVM model pipeline

model = make_pipeline(
    TfidfVectorizer(stop_words="english", max_features=3000),
    SVC(kernel = 'linear')
)

print("Training the model...")
model.fit(X_train, Y_train)

# Evaluating model performance
print("Evaluating model...")
Y_pred = model.predict(X_test)

print(metrics.classification_report(Y_test, Y_pred))

# Manual testing (optional)

if __name__ == "__main__":
    print(metrics.classification_report(Y_test, Y_pred))

    while True:
        text = input("\nEnter a review or 'exit' to quite: \n")
        if text.lower() == 'exit':
            break
        
        pred = model.predict([text])[0]

        print(f"Predicted sentiment: {pred}")