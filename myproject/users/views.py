from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('cvapp:home')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

from django.contrib.auth.views import LogoutView

class CustomLogoutView(LogoutView):
    next_page = 'cvapp:home'