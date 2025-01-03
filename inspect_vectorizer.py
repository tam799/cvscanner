import joblib

# Load the vectorizer
vectorizer = joblib.load('cvapp/ml_models/vectorizer.pkl')

# Print the feature names
print(vectorizer.get_feature_names_out())