from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'cvapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_cv, name='upload_cv'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', auth_views.LogoutView.as_view(next_page='cvapp:home'), name='logout'),
    path('evaluate/', views.evaluate_cv, name='evaluate_cv'),
]
