from django.shortcuts import render
from .models import CV
from .forms import CVForm
from django.http import HttpResponseRedirect
# Import your ML model here
# from .ml_model import analyze_cv

def home(request):
     return render(request, 'cvapp/home.html')

def upload_cv(request):
    if request.method == 'POST':
        form = CVForm(request.POST, request.FILES)
        if form.is_valid():
            cv_instance = form.save()
            # Analyze the CV using the ML model
            # analysis_result = analyze_cv(cv_instance)
            # Save or process the analysis result as needed
            return HttpResponseRedirect('/thanks/')
    else:
        form = CVForm()
    return render(request, 'cvapp/upload_cv.html', {'form': form})

def dashboard(request):
    # Fetch the analysis results from the database or other storage
    cvs = CV.objects.all()
    return render(request, 'cvapp/dashboard.html', {'cvs': cvs})
# Create your views here.
