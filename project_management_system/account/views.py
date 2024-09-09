from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import User
# Create your views here.

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if email and password:
            user = authenticate(request, email=email, password=password)

            if user is not None:
                auth_login(request, user)
            # print('User:', user)
            # print(request.user)
            # print(request.user.is_authenticated)
            return redirect('/')

    return render(request, 'account/login.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        pin = request.POST.get('pin', '')
        team = request.POST.get('team', '')
        is_manager = request.POST.get('is_manager', '')
        department = request.POST.get('department', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if name and email and password1 and password2:
            user = User.objects.create_user(name, email,  pin, team, is_manager, department, password1)

            print('User created:', user)

            return redirect('/login/')
        else:
            print('Something went wrong!')
    else:
        print('Just show the form!')

    return render(request, 'account/signup.html')

def logout_page(request):

    logout(request)
    return redirect('/login/')