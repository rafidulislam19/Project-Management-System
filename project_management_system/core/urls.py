from django.urls import path
from . import views

app_name = 'core'  # Define the app name for URL namespace

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]