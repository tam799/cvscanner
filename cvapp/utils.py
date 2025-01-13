import joblib
import chardet
import fitz  # PyMuPDF
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def load_model_and_vectorizer():
    model = joblib.load('cvapp/ml_models/logistic_regression_model.pkl')
    vectorizer = joblib.load('cvapp/ml_models/vectorizer.pkl')
    return model, vectorizer

def extract_features_from_cv(cv_path):
    # Check if the file is a PDF
    if cv_path.lower().endswith('.pdf'):
        # Extract text from PDF
        text = extract_text_from_pdf(cv_path)
    else:
        # Detect the encoding of the file
        with open(cv_path, 'rb') as file:
            raw_data = file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']

        with open(cv_path, 'r', encoding=encoding) as file:
            text = file.read()

    # Preprocess the text
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words]

    # Transform the text using the loaded vectorizer
    model, vectorizer = load_model_and_vectorizer()
    features = vectorizer.transform([' '.join(words)]).toarray()

    return features

def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    text = ""
    # Iterate through the pages and extract text
    for page in doc:
        text += page.get_text()
    return text
