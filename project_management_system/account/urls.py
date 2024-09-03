from django.urls import path
from . import views

app_name = 'account'  # Define the app name for URL namespace

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
]