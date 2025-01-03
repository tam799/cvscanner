import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Example training data and labels
train_data = ["sample text data", "another sample text"]
train_labels = [0, 1]

# Create and fit the vectorizer
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_data)

# Create and fit the logistic regression model
model = LogisticRegression()
model.fit(X_train, train_labels)

# Save the vectorizer and model
joblib.dump(vectorizer, 'cvapp/ml_models/vectorizer.pkl')
joblib.dump(model, 'cvapp/ml_models/logistic_regression_model.pkl')