import joblib


def load_model_and_vectorizer():
    model = joblib.load('cvapp/ml_models/logistic_regression_model.pkl')
    vectorizer = joblib.load('cvapp/ml_models/vectorizer.pkl')
    return model, vectorizer
