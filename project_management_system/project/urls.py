from django.urls import path
from . import views

app_name = 'project'  # Define the app name for URL namespace

urlpatterns = [
    path('', views.projects, name='projects'),
    path('add/', views.add_project, name='add'),
    path('<uuid:pk>/', views.project, name='project'),
    path('<uuid:pk>/edit/', views.edit_project, name='edit'),
    path('<uuid:pk>/delete/', views.delete, name='delete'),
]