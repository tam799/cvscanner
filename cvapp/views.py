import joblib
import os
import chardet
import fitz  # PyMuPDF
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from .utils import load_model_and_vectorizer

# Load the logistic regression model and vectorizer
model, vectorizer = load_model_and_vectorizer()

def home(request):
    return render(request, 'cvapp/home.html')

def upload_cv(request):
    if request.method == 'POST' and request.FILES['cv']:
        cv_file = request.FILES['cv']
        fs = FileSystemStorage()
        filename = fs.save(cv_file.name, cv_file)
        uploaded_file_url = fs.url(filename)

        # Extract features from the uploaded CV
        features = extract_features_from_cv(os.path.join(fs.location, filename))

        # Predict using the loaded model
        prediction = model.predict(features)

        # Store the prediction in the session
        request.session['cv_evaluation'] = prediction[0]

        return redirect('cvapp:dashboard')
    return render(request, 'cvapp/upload_cv.html')

def dashboard(request):
    prediction = request.session.get('cv_evaluation', None)
    return render(request, 'cvapp/dashboard.html', {'prediction': prediction})

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

        # Read the CV file with the detected encoding
        with open(cv_path, 'r', encoding=encoding) as file:
            text = file.read()

    # Preprocess the text
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words]

    # Transform the text using the loaded vectorizer
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

def evaluate_cv(request):
    if request.method == 'POST':
        # Extract features from the request
        features = request.POST.get('features')
        # Preprocess the text
        stop_words = set(stopwords.words('english'))
        lemmatizer = WordNetLemmatizer()
        words = features.split(',')
        words = [lemmatizer.lemmatize(word.lower().strip()) for word in words if word.lower().strip() not in stop_words]

        # Transform the text using the loaded vectorizer
        features_transformed = vectorizer.transform([' '.join(words)]).toarray()

        # Predict using the loaded model
        prediction = model.predict(features_transformed)

        # Store the prediction in the session
        request.session['cv_evaluation'] = prediction[0]

        # Return the prediction as a JSON response
        return JsonResponse({'prediction': prediction[0]})
    return render(request, 'cvapp/evaluate_cv.html')