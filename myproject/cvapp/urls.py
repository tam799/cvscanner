from django.urls import path
from . import views

app_name = 'cvapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_cv, name='upload_cv'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
