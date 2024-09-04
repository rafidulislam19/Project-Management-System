from django.urls import path
from . import views

app_name = 'todolist'  # Define the app name for URL namespace

urlpatterns = [
    path('add/', views.add, name='add'),
    path('<uuid:pk>/', views.todolist, name='todolist'),
    path('<uuid:pk>/edit/', views.edit, name='edit'),
    path('<uuid:pk>/delet/', views.delete, name='delete'),
]