from django.shortcuts import render, redirect
from .models import CV
from .forms import CVForm
from django.http import HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage
import os
import joblib
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import chardet
import fitz  # PyMuPDF
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

        # Extract features from the uploaded CV (this is a placeholder, implement your own feature extraction)
        features = extract_features_from_cv(os.path.join(fs.location, filename))

        # Predict using the loaded model
        prediction = model.predict(features)

        # Convert prediction to native Python type
        prediction = int(prediction[0])

        # Store the prediction in the session
        request.session['cv_evaluation'] = prediction

        return redirect('cvapp:dashboard')
    return render(request, 'cvapp/upload_cv.html')

def dashboard(request):
    prediction = request.session.get('cv_evaluation', None)
    if prediction is not None:
        if prediction == 0:
            result_message = "The CV is not suitable for the job."
        else:
            result_message = "The CV is suitable for the job."
    else:
        result_message = "No evaluation result available."
    return render(request, 'cvapp/dashboard.html', {'result_message': result_message})


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
        # Convert features to the appropriate format (e.g., list or numpy array)
        features = [float(x) for x in features.split(',')]
        # Predict using the loaded model
        prediction = model.predict([features])
         # Convert prediction to native Python type
        prediction = int(prediction[0])
        # Return the prediction as a JSON response
        return JsonResponse({'prediction': prediction})
    return render(request, 'cvapp/evaluate_cv.html')